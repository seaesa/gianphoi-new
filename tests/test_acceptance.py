"""Tiêu chí nghiệm thu — spec §7. Mỗi class là một dòng trong bảng tiêu chí.

Chạy trên HTML đã build thật, không phải trên template.
"""
import glob
import os
import re
import unittest

from scripts.build import ROOT
from scripts.color import contrast_ratio, parse_css_tokens
from scripts.sitedata import load_site
from tests.build_fixture import ensure_built

SITE = load_site()
CSS_PATH = os.path.join(ROOT, "assets", "css", "main.css")


def all_pages() -> list[str]:
    ensure_built()
    return sorted(
        glob.glob(os.path.join(ROOT, "*.html"))
        + glob.glob(os.path.join(ROOT, "blog", "*.html"))
    )


def read(path: str) -> str:
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def visible(path: str) -> str:
    """Bỏ comment HTML — comment không render nên không tính là nội dung.
    khu-vuc.html cố ý chứa markup mẫu trong comment để hướng dẫn thêm ảnh."""
    return re.sub(r"<!--.*?-->", "", read(path), flags=re.DOTALL)


def css() -> str:
    return read(CSS_PATH)


class Criterion01NoInlineStyle(unittest.TestCase):
    def test_no_style_attribute_on_any_page(self):
        for path in all_pages():
            with self.subTest(page=os.path.basename(path)):
                self.assertEqual(re.findall(r'\sstyle="', read(path)), [])


class Criterion02Contrast(unittest.TestCase):
    def test_every_text_pair_meets_aa(self):
        tokens = parse_css_tokens(css())
        pairs = [
            ("--ink", "--paper"), ("--muted", "--paper"), ("--muted", "--surface"),
            ("--ink-soft", "--paper"), ("--amber", "--paper"),
            ("--amber-ink", "--amber-tint"),
        ]
        for fg, bg in pairs:
            with self.subTest(pair=f"{fg} on {bg}"):
                self.assertGreaterEqual(contrast_ratio(tokens[fg], tokens[bg]), 4.5)

    def test_white_on_filled_surfaces(self):
        tokens = parse_css_tokens(css())
        for bg in ("--amber", "--steel", "--steel-deep"):
            with self.subTest(bg=bg):
                self.assertGreaterEqual(contrast_ratio("#FFFFFF", tokens[bg]), 4.5)

    def test_amber_bright_restricted_to_large_text(self):
        tokens = parse_css_tokens(css())
        ratio = contrast_ratio(tokens["--amber-bright"], tokens["--steel"])
        self.assertGreaterEqual(ratio, 3.0)


class Criterion03ContactReachable(unittest.TestCase):
    def test_every_page_exposes_phone_and_zalo(self):
        for path in all_pages():
            html = read(path)
            with self.subTest(page=os.path.basename(path)):
                self.assertIn(SITE.business.phone_display, html)
                self.assertIn(SITE.business.zalo_url, html)

    def test_no_css_rule_hides_the_header_phone_number(self):
        """Lỗi C1: bản cũ ẩn hẳn hotline ở breakpoint 768px."""
        for block in re.findall(r"\.header__phone-number[^{]*\{([^}]*)\}", css()):
            with self.subTest(block=block[:60]):
                self.assertNotIn("display: none", block)
                self.assertNotIn("display:none", block)

    def test_sticky_bar_present_on_every_page(self):
        for path in all_pages():
            with self.subTest(page=os.path.basename(path)):
                self.assertIn('class="sticky-bar"', read(path))


class Criterion04ServiceDropdown(unittest.TestCase):
    def test_contact_form_lists_all_eight_services(self):
        html = read(os.path.join(ROOT, "lien-he.html"))
        for service in SITE.services:
            with self.subTest(service=service.slug):
                self.assertIn(f'value="{service.slug}"', html)


class Criterion05NoJsRequiredForShell(unittest.TestCase):
    def test_header_footer_jsonld_present_without_javascript(self):
        for path in all_pages():
            html = read(path)
            with self.subTest(page=os.path.basename(path)):
                self.assertIn('class="site-header"', html)
                self.assertIn('class="site-footer"', html)
                self.assertIn('type="application/ld+json"', html)
                self.assertNotIn("data-include", html)

    def test_every_page_has_canonical_and_og(self):
        for path in all_pages():
            html = read(path)
            with self.subTest(page=os.path.basename(path)):
                self.assertIn('rel="canonical"', html)
                self.assertIn('property="og:title"', html)


class Criterion06ImageDimensions(unittest.TestCase):
    def test_every_img_declares_width_and_height(self):
        for path in all_pages():
            for tag in re.findall(r"<img[^>]*>", visible(path)):
                with self.subTest(page=os.path.basename(path), tag=tag[:60]):
                    self.assertIn("width=", tag)
                    self.assertIn("height=", tag)

    def test_every_img_has_alt(self):
        for path in all_pages():
            for tag in re.findall(r"<img[^>]*>", visible(path)):
                with self.subTest(page=os.path.basename(path), tag=tag[:60]):
                    self.assertIn("alt=", tag)


class Criterion07NoThreePixelAccents(unittest.TestCase):
    def test_css_has_no_three_pixel_borders(self):
        self.assertEqual(re.findall(r"border[a-z-]*:\s*3px", css()), [])


class Criterion08KeyboardNavigable(unittest.TestCase):
    def test_focus_visible_defined(self):
        self.assertIn(":focus-visible", css())

    def test_no_outline_none_without_replacement(self):
        for block in re.findall(r"\{[^{}]*outline:\s*none[^{}]*\}", css()):
            with self.subTest(block=block[:60]):
                self.assertIn("box-shadow", block)

    def test_interactive_elements_are_not_divs(self):
        for path in all_pages():
            with self.subTest(page=os.path.basename(path)):
                self.assertEqual(re.findall(r"<div[^>]*onclick", read(path)), [])

    def test_skip_link_on_every_page(self):
        for path in all_pages():
            with self.subTest(page=os.path.basename(path)):
                self.assertIn('class="skip-link"', read(path))

    def test_accordion_buttons_expose_state(self):
        """Soi trực tiếp từng nút FAQ thay vì đếm tổng aria-expanded trên
        trang — nav cũng có aria-expanded nên phép trừ là sai cách."""
        for path in all_pages():
            html = read(path)
            buttons = re.findall(r"<button[^>]*faq__question[^>]*>", html)
            if not buttons:
                continue
            for button in buttons:
                with self.subTest(page=os.path.basename(path)):
                    self.assertIn("aria-expanded=", button)
                    self.assertIn("aria-controls=", button)


class Criterion09NoHorizontalScroll(unittest.TestCase):
    def test_no_element_forces_width_beyond_viewport(self):
        """Chỉ soi thuộc tính `width` thật; `max-width`/`min-width` trong
        media query là hợp lệ nên phải loại bằng lookbehind."""
        self.assertEqual(re.findall(r"(?<![a-z-])width:\s*\d{4,}px", css()), [])

    def test_wide_content_is_wrapped_in_scroll_containers(self):
        for path in all_pages():
            html = read(path)
            if "<table" in html:
                with self.subTest(page=os.path.basename(path)):
                    self.assertIn("table-scroll", html)

    def test_viewport_meta_allows_zoom(self):
        for path in all_pages():
            html = read(path)
            with self.subTest(page=os.path.basename(path)):
                self.assertIn('name="viewport"', html)
                self.assertNotIn("user-scalable=no", html)
                self.assertNotIn("maximum-scale=1", html)


class Criterion10TelLinksOnlyOnCallActions(unittest.TestCase):
    def test_every_tel_link_is_declared_a_call_action(self):
        """Lỗi C5: thẻ ảnh dự án cũ link tới tel: — bấm xem ảnh thì máy gọi."""
        found = 0
        for path in all_pages():
            for tag in re.findall(r'<a[^>]*href="tel:[^"]*"[^>]*>', read(path)):
                found += 1
                with self.subTest(page=os.path.basename(path), tag=tag[:80]):
                    self.assertIn('data-action="call"', tag)
        self.assertGreater(found, 0, "Không tìm thấy link gọi điện nào")


class Criterion11NoFakeProjectClaims(unittest.TestCase):
    def test_completed_work_claims_are_backed_by_real_photos(self):
        """Nhãn "đã thi công" chỉ được xuất hiện trên trang có ảnh công
        trình thật. Bản cũ gắn nhãn này lên ảnh stock nước ngoài."""
        for path in all_pages():
            html = read(path)
            if "Dự án đã thi công" not in html:
                continue
            with self.subTest(page=os.path.basename(path)):
                self.assertIn("/assets/images/projects/", html)
                self.assertIn('class="card card--project"', html)

    def test_every_project_photo_has_a_descriptive_alt(self):
        html = read(os.path.join(ROOT, "du-an.html"))
        for project in SITE.projects:
            with self.subTest(project=project.img):
                self.assertIn(project.alt, html)

    def test_no_page_references_removed_stock_photos(self):
        for path in all_pages():
            html = read(path)
            with self.subTest(page=os.path.basename(path)):
                for stock in ("hero-banner", "about-thi-cong",
                              "nhan-vien-huong-dan", "thi-cong.jpeg"):
                    self.assertNotIn(stock, html)


class Criterion12IllustrationsAreRealPhotos(unittest.TestCase):
    """Mọi hình minh hoạ là ảnh chụp thật; SVG chỉ còn dùng làm icon."""

    def test_every_inline_svg_is_an_icon(self):
        for path in all_pages():
            html = visible(path)
            with self.subTest(page=os.path.basename(path)):
                self.assertEqual(
                    html.count("<svg"), html.count('class="icon"'),
                    "Còn SVG không phải icon — hình minh hoạ phải là ảnh thật",
                )

    def test_pages_with_illustrations_use_photos(self):
        for name in ("index.html", "gioi-thieu.html", "dich-vu.html"):
            html = visible(os.path.join(ROOT, name))
            with self.subTest(page=name):
                self.assertIn("/assets/images/", html)
                self.assertIn("srcset=", html)


class Criterion13NoBrokenInternalLinks(unittest.TestCase):
    """Mọi link nội bộ phải trỏ tới file có thật, và mọi neo #id phải tồn tại
    trên đúng trang đó. Lỗi loại này từng lọt: sau khi đổi khu-vuc.html thành
    du-an.html, trang chủ và footer vẫn trỏ tới trang đã xoá."""

    def _targets(self):
        seen = {}
        for path in all_pages():
            html = visible(path)
            for href in re.findall(r'href="(/[^"]*)"', html):
                seen.setdefault(href, set()).add(os.path.basename(path))
        return seen

    def test_every_internal_link_resolves_to_a_built_file(self):
        missing = []
        for href, pages in self._targets().items():
            target = href.split("#")[0].split("?")[0]
            if target in ("", "/"):
                continue
            full = os.path.join(ROOT, target.lstrip("/").replace("/", os.sep))
            if not os.path.exists(full):
                missing.append((href, sorted(pages)))
        self.assertEqual(missing, [], f"Link nội bộ hỏng: {missing}")

    def test_every_fragment_target_exists_on_its_page(self):
        missing = []
        for href in self._targets():
            if "#" not in href:
                continue
            target, _, frag = href.partition("#")
            if not frag:
                continue
            target = target or "/index.html"
            if target == "/":
                target = "/index.html"
            full = os.path.join(ROOT, target.lstrip("/").replace("/", os.sep))
            if not os.path.exists(full):
                continue
            if f'id="{frag}"' not in read(full):
                missing.append(href)
        self.assertEqual(missing, [], f"Neo không tồn tại: {missing}")

    def test_no_page_still_references_removed_pages(self):
        """Chỉ soi link trang; `/assets/images/blog/` là thư mục ảnh hợp lệ
        nên không được tính là URL bài viết cũ."""
        for path in all_pages():
            with self.subTest(page=os.path.basename(path)):
                self.assertNotIn("khu-vuc.html", read(path))
                self.assertEqual(re.findall(r'href="/blog/', read(path)), [])


class TestSitemapAndRobots(unittest.TestCase):
    def test_sitemap_lists_every_page(self):
        ensure_built()
        sitemap = read(os.path.join(ROOT, "sitemap.xml"))
        for path in all_pages():
            rel = os.path.relpath(path, ROOT).replace("\\", "/")
            with self.subTest(page=rel):
                self.assertIn(rel, sitemap)

    def test_robots_points_at_sitemap(self):
        ensure_built()
        robots = read(os.path.join(ROOT, "robots.txt"))
        self.assertIn("Sitemap:", robots)
        self.assertIn("sitemap.xml", robots)

    def test_robots_hides_the_source_image_folder(self):
        ensure_built()
        self.assertIn("_src", read(os.path.join(ROOT, "robots.txt")))
