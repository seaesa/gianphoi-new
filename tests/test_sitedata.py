import unittest

from scripts.sitedata import (
    SiteDataError,
    find_service,
    format_price,
    load_site,
    service_groups,
)

SITE = load_site()


class TestBusiness(unittest.TestCase):
    def test_phone_is_e164(self):
        self.assertTrue(SITE.business.phone.startswith("+84"))
        self.assertTrue(SITE.business.phone[1:].isdigit())

    def test_zalo_url_present(self):
        self.assertIn("zalo.me", SITE.business.zalo_url)

    def test_email_present(self):
        self.assertIn("@", SITE.business.email)


class TestServices(unittest.TestCase):
    def test_exactly_eight_services(self):
        self.assertEqual(len(SITE.services), 8)

    def test_slugs_are_unique(self):
        slugs = [s.slug for s in SITE.services]
        self.assertEqual(len(slugs), len(set(slugs)))

    def test_every_service_has_three_specs(self):
        for service in SITE.services:
            with self.subTest(service=service.slug):
                self.assertEqual(len(service.specs), 3)

    def test_every_service_has_warranty_spec(self):
        for service in SITE.services:
            with self.subTest(service=service.slug):
                labels = [spec.label for spec in service.specs]
                self.assertIn("Bảo hành", labels)

    def test_price_range_is_ordered(self):
        for service in SITE.services:
            with self.subTest(service=service.slug):
                self.assertLess(service.price_from, service.price_to)

    def test_exactly_one_popular_service(self):
        self.assertEqual(sum(1 for s in SITE.services if s.popular), 1)

    def test_groups_are_the_three_from_spec(self):
        groups = [name for name, _ in service_groups(SITE)]
        self.assertEqual(groups, ["Giàn phơi", "An toàn ban công", "Che chắn"])

    def test_every_service_belongs_to_a_known_group(self):
        grouped = sum(len(items) for _, items in service_groups(SITE))
        self.assertEqual(grouped, 8)

    def test_every_service_references_an_svg(self):
        for service in SITE.services:
            with self.subTest(service=service.slug):
                self.assertTrue(service.svg.endswith(".svg"))


class TestFormatPrice(unittest.TestCase):
    def test_formats_with_dot_separators_and_en_dash(self):
        service = find_service(SITE, "gian-phoi-dieu-khien")
        self.assertEqual(format_price(service), "3.200.000 – 4.500.000đ/bộ")

    def test_per_square_metre_unit(self):
        service = find_service(SITE, "luoi-cap-ban-cong")
        self.assertEqual(format_price(service), "180.000 – 250.000đ/m²")


class TestFaqs(unittest.TestCase):
    def test_ten_faqs(self):
        self.assertEqual(len(SITE.faqs), 10)

    def test_four_marked_for_contact_page(self):
        # Spec §4.2: trang Liên hệ giữ 4 câu về đặt lịch và báo giá.
        self.assertEqual(sum(1 for f in SITE.faqs if f.contact_page), 4)

    def test_questions_carry_no_manual_numbering(self):
        # Bản cũ nhúng "1. ", "2. " vào câu hỏi — số thứ tự thuộc về CSS.
        for faq in SITE.faqs:
            with self.subTest(question=faq.question):
                self.assertFalse(faq.question[0].isdigit())


class TestPosts(unittest.TestCase):
    def test_twelve_posts(self):
        self.assertEqual(len(SITE.posts), 12)

    def test_iso_dates_are_sortable(self):
        for post in SITE.posts:
            with self.subTest(post=post.slug):
                self.assertRegex(post.iso_date, r"^\d{4}-\d{2}-\d{2}$")

    def test_source_files_exist(self):
        import os

        for post in SITE.posts:
            with self.subTest(post=post.slug):
                self.assertTrue(os.path.exists(post.source), post.source)

    def test_every_post_has_a_category(self):
        allowed = {"Khu vực", "Kiến thức", "So sánh"}
        for post in SITE.posts:
            with self.subTest(post=post.slug):
                self.assertIn(post.category, allowed)


class TestFacts(unittest.TestCase):
    def test_five_facts_for_numeric_rail(self):
        # Spec §3.6: numeric rail có đúng 5 số liệu.
        self.assertEqual(len(SITE.facts), 5)


class TestValidation(unittest.TestCase):
    def test_missing_file_raises(self):
        with self.assertRaises(SiteDataError):
            load_site("khong-ton-tai.json")

    def test_malformed_service_raises(self):
        import json
        import os
        import tempfile

        bad = {
            "business": {},
            "services": [{"slug": "x"}],
            "faqs": [],
            "areas": [],
            "posts": [],
            "facts": [],
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "bad.json")
            with open(path, "w", encoding="utf-8") as handle:
                json.dump(bad, handle)
            with self.assertRaises(SiteDataError):
                load_site(path)

    def test_unknown_service_slug_raises(self):
        with self.assertRaises(SiteDataError):
            find_service(SITE, "khong-co-dich-vu-nay")
