import unittest

from scripts.components import (
    area_list,
    comparison_table,
    faq_list,
    icon,
    numeric_rail,
    post_card,
    service_card,
    service_options,
    spec_line,
    stepper,
)
from scripts.sitedata import find_service, load_site

SITE = load_site()


class TestSpecLine(unittest.TestCase):
    def test_renders_definition_list_with_three_rows(self):
        html = spec_line(find_service(SITE, "gian-phoi-treo-tran"))
        self.assertIn('class="spec-line"', html)
        self.assertEqual(html.count("<dt>"), 3)
        self.assertEqual(html.count("<dd>"), 3)

    def test_includes_warranty_value(self):
        html = spec_line(find_service(SITE, "gian-phoi-dieu-khien"))
        self.assertIn("Bảo hành", html)


class TestServiceCard(unittest.TestCase):
    def test_has_id_price_and_quote_link(self):
        service = find_service(SITE, "luoi-cap-ban-cong")
        html = service_card(service, svg_inline="<svg></svg>")
        self.assertIn('id="luoi-cap-ban-cong"', html)
        self.assertIn("180.000 – 250.000đ/m²", html)
        self.assertIn("/lien-he.html", html)

    def test_popular_service_gets_badge(self):
        popular = next(s for s in SITE.services if s.popular)
        html = service_card(popular, svg_inline="<svg></svg>")
        self.assertIn("Phổ biến nhất", html)

    def test_ordinary_service_has_no_badge(self):
        plain = next(s for s in SITE.services if not s.popular)
        html = service_card(plain, svg_inline="<svg></svg>")
        self.assertNotIn("Phổ biến nhất", html)

    def test_never_emits_inline_style(self):
        for service in SITE.services:
            with self.subTest(service=service.slug):
                self.assertNotIn("style=", service_card(service, svg_inline="<svg></svg>"))

    def test_quote_link_carries_service_slug(self):
        service = find_service(SITE, "mai-hien-quay-tay")
        html = service_card(service, svg_inline="<svg></svg>")
        self.assertIn("dich-vu=mai-hien-quay-tay", html)


class TestNumericRail(unittest.TestCase):
    def test_renders_every_fact(self):
        html = numeric_rail(SITE.facts)
        self.assertEqual(html.count('class="rail__item"'), 5)
        self.assertIn("1000+", html)

    def test_uses_list_semantics(self):
        self.assertIn("<ul", numeric_rail(SITE.facts))


class TestStepper(unittest.TestCase):
    def test_numbers_steps_from_one(self):
        html = stepper([("Tiếp nhận", "x"), ("Khảo sát", "y")])
        self.assertIn(">1<", html)
        self.assertIn(">2<", html)

    def test_uses_ordered_list_for_semantics(self):
        self.assertIn("<ol", stepper([("A", "x")]))


class TestFaqList(unittest.TestCase):
    def test_button_carries_aria_attributes(self):
        html = faq_list(SITE.faqs[:2])
        self.assertIn('aria-expanded="false"', html)
        self.assertIn("aria-controls=", html)

    def test_panel_is_hidden_by_default(self):
        self.assertIn("hidden", faq_list(SITE.faqs[:1]))

    def test_ids_are_unique_across_items(self):
        html = faq_list(SITE.faqs)
        ids = [chunk.split('"')[0] for chunk in html.split('id="')[1:]]
        self.assertEqual(len(ids), len(set(ids)))

    def test_prefix_isolates_two_lists_on_one_page(self):
        b = faq_list(SITE.faqs[:2], id_prefix="faq-b")
        self.assertNotIn("faq-a", b)


class TestServiceOptions(unittest.TestCase):
    def test_lists_all_eight_real_services(self):
        # Sửa lỗi C4: dropdown cũ chỉ có 4 loại cửa lưới.
        html = service_options(SITE)
        self.assertEqual(html.count("<option"), 9)  # 8 dịch vụ + 1 placeholder
        for service in SITE.services:
            with self.subTest(service=service.slug):
                self.assertIn(service.name, html)

    def test_values_are_slugs(self):
        html = service_options(SITE)
        for service in SITE.services:
            with self.subTest(service=service.slug):
                self.assertIn(f'value="{service.slug}"', html)


class TestComparisonTable(unittest.TestCase):
    def test_covers_the_three_drying_racks(self):
        html = comparison_table(SITE)
        for slug in ("gian-phoi-dieu-khien", "gian-phoi-treo-tran", "gian-phoi-xep-tuong"):
            with self.subTest(slug=slug):
                self.assertIn(find_service(SITE, slug).name, html)

    def test_has_scope_attributes_for_screen_readers(self):
        self.assertIn('scope="col"', comparison_table(SITE))
        self.assertIn('scope="row"', comparison_table(SITE))

    def test_wrapped_in_scroll_container(self):
        self.assertIn("table-scroll", comparison_table(SITE))

    def test_has_caption(self):
        self.assertIn("<caption", comparison_table(SITE))


class TestPostCard(unittest.TestCase):
    def test_carries_category_for_filtering(self):
        html = post_card(SITE.posts[0])
        self.assertIn("data-category=", html)

    def test_uses_machine_readable_time(self):
        html = post_card(SITE.posts[0])
        self.assertIn("<time datetime=", html)

    def test_image_has_dimensions(self):
        html = post_card(SITE.posts[0])
        self.assertIn("width=", html)
        self.assertIn("height=", html)

    def test_image_is_lazy(self):
        self.assertIn('loading="lazy"', post_card(SITE.posts[0]))


class TestAreaList(unittest.TestCase):
    def test_renders_every_area(self):
        html = area_list(SITE.areas)
        for area in SITE.areas:
            with self.subTest(area=area):
                self.assertIn(area, html)


class TestIcon(unittest.TestCase):
    def test_known_icons_render_svg(self):
        for name in ("phone", "zalo", "quote"):
            with self.subTest(name=name):
                svg = icon(name)
                self.assertTrue(svg.startswith("<svg"))
                self.assertIn('stroke="currentColor"', svg)

    def test_icons_are_decorative_by_default(self):
        self.assertIn('aria-hidden="true"', icon("phone"))

    def test_icons_carry_no_hardcoded_colour(self):
        for name in ("phone", "zalo", "quote"):
            with self.subTest(name=name):
                self.assertNotIn("#", icon(name))

    def test_unknown_icon_raises(self):
        with self.assertRaises(KeyError):
            icon("khong-co-icon-nay")
