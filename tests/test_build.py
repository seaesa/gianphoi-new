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


class TestServicesPage(unittest.TestCase):
    def setUp(self):
        self.html = read_output("dich-vu.html")

    def test_all_eight_services_rendered(self):
        self.assertEqual(self.html.count('class="card card--service"'), 8)

    def test_grouped_into_the_three_categories(self):
        # Sửa lỗi C6.
        for group in ("Giàn phơi", "An toàn ban công", "Che chắn"):
            with self.subTest(group=group):
                self.assertIn(group, self.html)

    def test_each_service_anchor_is_reachable(self):
        for service in SITE.services:
            with self.subTest(service=service.slug):
                self.assertIn(f'id="{service.slug}"', self.html)

    def test_has_comparison_table_in_scroll_container(self):
        self.assertIn("table-scroll", self.html)
        self.assertIn("<table", self.html)

    def test_all_ten_faqs_live_here(self):
        self.assertEqual(self.html.count('class="faq__question"'), 10)

    def test_faq_page_schema_present(self):
        self.assertIn("FAQPage", self.html)

    def test_service_schema_for_every_service(self):
        self.assertEqual(self.html.count('"@type": "Service"'), 8)

    def test_breadcrumb_schema_present(self):
        self.assertIn("BreadcrumbList", self.html)

    def test_no_inline_style(self):
        self.assertEqual(re.findall(r'\sstyle="', self.html), [])


class TestAreasPage(unittest.TestCase):
    """Thay du-an.html — spec §4.6."""

    def setUp(self):
        self.html = read_output("khu-vuc.html")

    def test_old_projects_page_is_gone(self):
        self.assertFalse(os.path.exists(os.path.join(ROOT, "du-an.html")))

    def test_does_not_claim_stock_photos_are_completed_projects(self):
        # Spec §2.2 — đây là lý do trang cũ bị đổi mục đích.
        self.assertNotIn("Dự án đã thi công", self.html)
        for stock in ("projects/thu-duc.jpg", "projects/quan-1.jpg",
                      "projects/quan-7.jpg", "projects/thu-dau-mot.jpg"):
            with self.subTest(stock=stock):
                self.assertNotIn(stock, self.html)

    def test_no_tel_link_on_project_cards(self):
        # Sửa lỗi C5: thẻ dự án cũ link tới tel:.
        for tag in re.findall(r'<a[^>]*href="tel:[^"]*"[^>]*>', self.html):
            with self.subTest(tag=tag[:80]):
                self.assertNotIn("card--project", tag)

    def test_lists_every_service_area(self):
        for area in SITE.areas:
            with self.subTest(area=area):
                self.assertIn(area, self.html)

    def test_has_empty_project_grid_awaiting_real_photos(self):
        self.assertIn('class="project-grid"', self.html)
        self.assertIn("ảnh công trình thật", self.html.lower())

    def test_no_inline_style(self):
        self.assertEqual(re.findall(r'\sstyle="', self.html), [])


class TestAboutPage(unittest.TestCase):
    def setUp(self):
        self.html = read_output("gioi-thieu.html")

    def test_has_numeric_rail(self):
        self.assertEqual(self.html.count('class="rail__item"'), 5)

    def test_alt_text_describes_actual_image_content(self):
        # Spec §2.2: bản cũ ghi "kỹ thuật viên lắp đặt" cho ảnh thợ mộc dùng MacBook.
        self.assertNotIn("Kỹ thuật viên đang thao tác lắp đặt", self.html)

    def test_no_inline_style(self):
        self.assertEqual(re.findall(r'\sstyle="', self.html), [])


class TestContactPage(unittest.TestCase):
    def setUp(self):
        self.html = read_output("lien-he.html")

    def test_dropdown_lists_the_eight_real_services(self):
        """Sửa lỗi C4: bản cũ chỉ liệt kê 4 loại cửa lưới."""
        for service in SITE.services:
            with self.subTest(service=service.slug):
                self.assertIn(f'value="{service.slug}"', self.html)

    def test_dropdown_has_no_orphan_cua_luoi_options(self):
        for dead in ("Cửa lưới xếp gọn", "Cửa lưới cố định",
                     "Cửa lưới inox, nhôm cao cấp"):
            with self.subTest(option=dead):
                self.assertNotIn(dead, self.html)

    def test_form_has_exactly_four_fields(self):
        # Spec §4.3: Tên, SĐT, Khu vực, Dịch vụ.
        self.assertEqual(self.html.count('class="field"'), 4)

    def test_every_field_has_a_visible_label(self):
        labels = re.findall(r'<label[^>]*for="([^"]+)"', self.html)
        inputs = re.findall(r'<(?:input|select|textarea)[^>]*id="([^"]+)"', self.html)
        self.assertEqual(sorted(labels), sorted(inputs))

    def test_phone_field_uses_tel_input_mode(self):
        field = re.search(r'<input[^>]*id="phone"[^>]*>', self.html).group(0)
        self.assertIn('type="tel"', field)
        self.assertIn('inputmode="numeric"', field)

    def test_each_field_has_an_error_container(self):
        self.assertEqual(self.html.count('class="field__error"'), 4)

    def test_error_containers_are_live_regions(self):
        self.assertEqual(self.html.count('aria-live="polite"'), 4)

    def test_contact_channels_appear_before_the_form(self):
        # Spec §4.3: Zalo và hotline đặt phía trên form.
        self.assertLess(self.html.index("zalo.me"), self.html.index("<form"))

    def test_only_four_faqs_here(self):
        self.assertEqual(self.html.count('class="faq__question"'), 4)

    def test_links_to_full_faq_list(self):
        self.assertIn("/dich-vu.html#faq", self.html)

    def test_submission_is_marked_as_not_wired_up(self):
        # Spec §6: giữ giả lập, phải có TODO rõ ràng.
        js = read_output("assets/js/main.js")
        self.assertIn("TODO", js)

    def test_no_inline_style(self):
        self.assertEqual(re.findall(r'\sstyle="', self.html), [])


class TestBlogIndex(unittest.TestCase):
    def setUp(self):
        self.html = read_output("blog.html")

    def test_lists_every_post(self):
        self.assertEqual(self.html.count('class="card card--post"'), 12)

    def test_has_category_filter_chips(self):
        self.assertEqual(self.html.count('class="chip"'), 4)

    def test_chips_are_real_buttons(self):
        chips = re.findall(r'<(\w+)[^>]*class="chip"', self.html)
        self.assertTrue(all(tag == "button" for tag in chips), chips)

    def test_chips_expose_pressed_state(self):
        self.assertIn('aria-pressed="true"', self.html)

    def test_no_inline_style(self):
        self.assertEqual(re.findall(r'\sstyle="', self.html), [])


class TestBlogPost(unittest.TestCase):
    def setUp(self):
        self.html = read_output("blog/quan-1.html")

    def test_has_conversion_sidebar(self):
        # Sửa lỗi C7.
        self.assertIn('class="quote-aside"', self.html)
        self.assertIn(SITE.business.phone_display, self.html)

    def test_sidebar_links_to_a_related_service(self):
        aside = self.html.split('class="quote-aside"')[1].split("</aside>")[0]
        self.assertIn("/dich-vu.html#", aside)

    def test_has_table_of_contents(self):
        self.assertIn('class="toc"', self.html)

    def test_headings_have_anchor_ids(self):
        self.assertRegex(self.html, r'<h2 id="[a-z0-9-]+">')

    def test_has_blogposting_schema(self):
        self.assertIn("BlogPosting", self.html)

    def test_no_inline_style(self):
        # Bản cũ có style="max-width:760px" ngay trong PAGE_TMPL.
        self.assertEqual(re.findall(r'\sstyle="', self.html), [])

    def test_tables_are_wrapped_for_horizontal_scroll(self):
        if "<table" in self.html:
            self.assertIn("table-scroll", self.html)

    def test_no_stock_cover_photo(self):
        """Ảnh minh hoạ bài viết là stock sai chủ đề nên đã bị loại (spec §2.2)."""
        self.assertNotIn("/assets/images/blog/", self.html)


class TestAllPostsBuild(unittest.TestCase):
    def test_every_post_file_exists(self):
        ensure_built()
        for post in SITE.posts:
            with self.subTest(post=post.slug):
                path = os.path.join(ROOT, "blog", f"{post.slug}.html")
                self.assertTrue(os.path.exists(path))

    def test_old_build_script_removed(self):
        self.assertFalse(os.path.exists(os.path.join(ROOT, "scripts", "build_blog.py")))
