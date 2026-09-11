import os
import re
import unittest

from scripts.build import ROOT
from scripts.sitedata import format_price, load_site
from tests.build_fixture import ensure_built, read_output

SITE = load_site()


class TestBuildRuns(unittest.TestCase):
    def test_writes_expected_pages(self):
        written = {os.path.relpath(p, ROOT).replace("\\", "/") for p in ensure_built()}
        self.assertIn("index.html", written)

    def test_include_js_is_gone(self):
        ensure_built()
        self.assertFalse(os.path.exists(os.path.join(ROOT, "assets", "js", "include.js")))


class TestHomepageShell(unittest.TestCase):
    def setUp(self):
        self.html = read_output("index.html")

    def test_header_is_inlined_not_fetched(self):
        # Sửa §2.7: bản cũ nạp header bằng fetch nên Google không thấy.
        self.assertNotIn("data-include", self.html)
        self.assertIn('class="site-header"', self.html)
        self.assertIn("Trang chủ", self.html)

    def test_footer_is_inlined(self):
        self.assertIn('class="site-footer"', self.html)
        self.assertIn(SITE.business.email, self.html)

    def test_no_inline_style_attributes(self):
        self.assertEqual(re.findall(r'\sstyle="', self.html), [])

    def test_has_skip_link_to_main(self):
        self.assertIn('class="skip-link"', self.html)
        self.assertIn('id="main"', self.html)

    def test_declares_vietnamese_language(self):
        self.assertIn('<html lang="vi">', self.html)

    def test_loads_both_fonts(self):
        self.assertIn("Be+Vietnam+Pro", self.html)
        self.assertIn("Inter", self.html)

    def test_marks_current_nav_item(self):
        self.assertIn('aria-current="page"', self.html)


class TestHotlineAlwaysReachable(unittest.TestCase):
    """Sửa lỗi C1 + C3."""

    def setUp(self):
        self.html = read_output("index.html")

    def test_header_shows_phone_number_as_text(self):
        self.assertIn(SITE.business.phone_display, self.html)

    def test_tel_link_uses_e164(self):
        self.assertIn(f'href="tel:{SITE.business.phone}"', self.html)

    def test_zalo_link_present(self):
        self.assertIn(SITE.business.zalo_url, self.html)

    def test_sticky_bar_has_three_actions(self):
        self.assertIn('class="sticky-bar"', self.html)
        self.assertEqual(self.html.count('class="sticky-bar__action'), 3)


class TestHomepageSections(unittest.TestCase):
    """Thứ tự 8 khối theo spec §4.1."""

    def setUp(self):
        self.html = read_output("index.html")

    def test_hero_has_no_stock_photo(self):
        self.assertNotIn("hero-banner", self.html)

    def test_hero_uses_line_drawing(self):
        hero = self.html.split('class="hero"')[1].split("</section>")[0]
        self.assertIn("<svg", hero)

    def test_numeric_rail_present_with_five_facts(self):
        self.assertEqual(self.html.count('class="rail__item"'), 5)

    def test_decision_layer_offers_three_use_cases(self):
        # Sửa lỗi C6 — tầng quyết định đang thiếu hoàn toàn.
        self.assertIn("Chọn loại giàn phù hợp", self.html)
        self.assertEqual(self.html.count('class="card card--usecase"'), 3)

    def test_price_preview_shows_four_services_with_specs(self):
        self.assertEqual(self.html.count('class="card card--service"'), 4)
        self.assertEqual(self.html.count('class="spec-line"'), 4)

    def test_popular_badge_appears_once(self):
        self.assertEqual(self.html.count("Phổ biến nhất"), 1)

    def test_process_has_five_steps(self):
        self.assertEqual(self.html.count('class="stepper__num"'), 5)

    def test_trust_band_lists_service_areas(self):
        for area in SITE.areas:
            with self.subTest(area=area):
                self.assertIn(area, self.html)

    def test_shows_three_latest_posts(self):
        self.assertEqual(self.html.count('class="card card--post"'), 3)

    def test_prices_come_from_site_json(self):
        for service in SITE.services[:4]:
            with self.subTest(service=service.slug):
                self.assertIn(format_price(service), self.html)


class TestHomepageSeo(unittest.TestCase):
    def setUp(self):
        self.html = read_output("index.html")

    def test_has_canonical(self):
        self.assertIn('rel="canonical"', self.html)

    def test_has_open_graph(self):
        for prop in ('property="og:title"', 'property="og:description"',
                     'property="og:image"'):
            with self.subTest(prop=prop):
                self.assertIn(prop, self.html)

    def test_has_local_business_jsonld(self):
        self.assertIn('type="application/ld+json"', self.html)
        self.assertIn("LocalBusiness", self.html)

    def test_exactly_one_h1(self):
        self.assertEqual(len(re.findall(r"<h1[\s>]", self.html)), 1)


class TestHomepageImages(unittest.TestCase):
    def test_every_img_has_explicit_dimensions(self):
        html = read_output("index.html")
        for tag in re.findall(r"<img[^>]*>", html):
            with self.subTest(tag=tag[:70]):
                self.assertIn("width=", tag)
                self.assertIn("height=", tag)

    def test_below_fold_images_are_lazy(self):
        html = read_output("index.html")
        tags = re.findall(r"<img[^>]*>", html)
        for tag in tags[1:]:
            with self.subTest(tag=tag[:70]):
                self.assertIn('loading="lazy"', tag)
