import json
import unittest

from scripts.schema import (
    blog_posting,
    breadcrumb_list,
    faq_page,
    local_business,
    service_schema,
    to_jsonld,
)
from scripts.sitedata import find_service, load_site

SITE = load_site()


class TestLocalBusiness(unittest.TestCase):
    def setUp(self):
        self.data = local_business(SITE)

    def test_type_and_context(self):
        self.assertEqual(self.data["@context"], "https://schema.org")
        self.assertEqual(self.data["@type"], "LocalBusiness")

    def test_phone_matches_site_data(self):
        self.assertEqual(self.data["telephone"], SITE.business.phone)

    def test_address_is_postal_address(self):
        self.assertEqual(self.data["address"]["@type"], "PostalAddress")
        self.assertEqual(self.data["address"]["addressCountry"], "VN")

    def test_area_served_lists_every_area(self):
        served = {a["name"] for a in self.data["areaServed"]}
        self.assertEqual(served, set(SITE.areas))

    def test_has_opening_hours(self):
        self.assertIn("openingHours", self.data)


class TestServiceSchema(unittest.TestCase):
    def test_carries_price_range_and_provider(self):
        data = service_schema(SITE, find_service(SITE, "gian-phoi-dieu-khien"))
        self.assertEqual(data["@type"], "Service")
        self.assertIn("3.200.000", data["offers"]["priceRange"])
        self.assertEqual(data["provider"]["name"], SITE.business.name)

    def test_offer_currency_is_vnd(self):
        data = service_schema(SITE, find_service(SITE, "luoi-cap-ban-cong"))
        self.assertEqual(data["offers"]["priceCurrency"], "VND")

    def test_area_served_present(self):
        data = service_schema(SITE, find_service(SITE, "luoi-cap-ban-cong"))
        self.assertIn("areaServed", data)


class TestFaqPage(unittest.TestCase):
    def test_maps_every_faq_to_a_question(self):
        data = faq_page(SITE.faqs)
        self.assertEqual(data["@type"], "FAQPage")
        self.assertEqual(len(data["mainEntity"]), 10)
        self.assertEqual(data["mainEntity"][0]["@type"], "Question")
        self.assertEqual(data["mainEntity"][0]["acceptedAnswer"]["@type"], "Answer")


class TestBreadcrumbList(unittest.TestCase):
    def test_positions_start_at_one_and_are_absolute(self):
        data = breadcrumb_list([("Trang chủ", "/"), ("Dịch vụ", "/dich-vu.html")])
        self.assertEqual(data["itemListElement"][0]["position"], 1)
        self.assertEqual(data["itemListElement"][1]["position"], 2)
        self.assertTrue(data["itemListElement"][1]["item"].startswith("https://"))


class TestBlogPosting(unittest.TestCase):
    def test_uses_iso_date_and_absolute_image(self):
        data = blog_posting(SITE, SITE.posts[0])
        self.assertEqual(data["datePublished"], SITE.posts[0].iso_date)
        self.assertTrue(data["image"].startswith("https://"))

    def test_publisher_is_the_business(self):
        data = blog_posting(SITE, SITE.posts[0])
        self.assertEqual(data["publisher"]["name"], SITE.business.name)


class TestToJsonld(unittest.TestCase):
    def test_wraps_in_script_tag_with_valid_json(self):
        out = to_jsonld(local_business(SITE))
        self.assertTrue(out.startswith('<script type="application/ld+json">'))
        self.assertTrue(out.rstrip().endswith("</script>"))
        payload = out.split(">", 1)[1].rsplit("<", 1)[0]
        json.loads(payload)

    def test_multiple_objects_become_a_json_array(self):
        out = to_jsonld(local_business(SITE), faq_page(SITE.faqs))
        payload = json.loads(out.split(">", 1)[1].rsplit("<", 1)[0])
        self.assertIsInstance(payload, list)
        self.assertEqual(len(payload), 2)

    def test_output_cannot_break_out_of_script_tag(self):
        # Bảo vệ XSS: "</script>" trong dữ liệu phải được thoát.
        out = to_jsonld({"name": "</script><img onerror=alert(1)>"})
        self.assertNotIn("</script><img", out)

    def test_escaped_payload_still_decodes_to_original_text(self):
        out = to_jsonld({"name": "a<b>c"})
        payload = json.loads(out.split(">", 1)[1].rsplit("<", 1)[0])
        self.assertEqual(payload["name"], "a<b>c")

    def test_keeps_vietnamese_characters_unescaped(self):
        out = to_jsonld({"name": "Giàn phơi"})
        self.assertIn("Giàn phơi", out)
