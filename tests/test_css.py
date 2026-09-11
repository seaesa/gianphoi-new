import os
import re
import unittest

from scripts.color import contrast_ratio, parse_css_tokens

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSS_PATH = os.path.join(ROOT, "assets", "css", "main.css")

with open(CSS_PATH, encoding="utf-8") as handle:
    CSS = handle.read()

TOKENS = parse_css_tokens(CSS)

REQUIRED_COLOR_TOKENS = [
    "--ink", "--ink-soft", "--muted", "--steel", "--steel-deep",
    "--paper", "--surface", "--hairline",
    "--amber", "--amber-bright", "--amber-tint", "--amber-ink",
]

EXPECTED = {
    "--ink": "#0F1C26", "--ink-soft": "#33506A", "--muted": "#5A6873",
    "--steel": "#1E3446", "--steel-deep": "#162836",
    "--paper": "#FBFAF8", "--surface": "#FFFFFF", "--hairline": "#E3E0DA",
    "--amber": "#B4530A", "--amber-bright": "#E07A1F",
    "--amber-tint": "#FDF1E3", "--amber-ink": "#8A3D06",
}


class TestTokens(unittest.TestCase):
    def test_all_required_tokens_defined(self):
        for name in REQUIRED_COLOR_TOKENS:
            with self.subTest(token=name):
                self.assertIn(name, TOKENS)

    def test_token_values_match_spec_exactly(self):
        for name, value in EXPECTED.items():
            with self.subTest(token=name):
                self.assertEqual(TOKENS[name], value)

    def test_legacy_tokens_are_gone(self):
        for dead in ("--color-primary", "--color-accent", "--color-ink",
                     "--radius-sm", "--radius-md", "--radius-lg", "--radius-pill"):
            with self.subTest(token=dead):
                self.assertNotIn(dead, CSS)

    def test_only_three_radius_tokens(self):
        radii = set(re.findall(r"--r(?:-sm|-pill)?\s*:", CSS))
        self.assertEqual(len(radii), 3)

    def test_spacing_scale_present(self):
        for i in range(1, 11):
            with self.subTest(step=i):
                self.assertIn(f"--space-{i}:", CSS)


class TestContrastOfRealTokens(unittest.TestCase):
    """Đọc màu thật trong CSS — test không thể trôi khỏi implementation."""

    def test_body_text_on_page_background(self):
        self.assertGreaterEqual(contrast_ratio(TOKENS["--ink"], TOKENS["--paper"]), 4.5)

    def test_muted_text_on_both_surfaces(self):
        for bg in ("--paper", "--surface"):
            with self.subTest(bg=bg):
                self.assertGreaterEqual(contrast_ratio(TOKENS["--muted"], TOKENS[bg]), 4.5)

    def test_white_on_primary_cta(self):
        self.assertGreaterEqual(contrast_ratio("#FFFFFF", TOKENS["--amber"]), 4.5)

    def test_white_on_steel_band(self):
        self.assertGreaterEqual(contrast_ratio("#FFFFFF", TOKENS["--steel"]), 4.5)

    def test_amber_link_on_paper(self):
        self.assertGreaterEqual(contrast_ratio(TOKENS["--amber"], TOKENS["--paper"]), 4.5)

    def test_badge_pair(self):
        self.assertGreaterEqual(
            contrast_ratio(TOKENS["--amber-ink"], TOKENS["--amber-tint"]), 4.5
        )

    def test_ink_soft_on_paper(self):
        self.assertGreaterEqual(
            contrast_ratio(TOKENS["--ink-soft"], TOKENS["--paper"]), 4.5
        )

    def test_amber_bright_is_large_text_only(self):
        ratio = contrast_ratio(TOKENS["--amber-bright"], TOKENS["--steel"])
        self.assertGreaterEqual(ratio, 3.0)
        self.assertLess(ratio, 4.5, "Nếu đạt 4.5 thì bỏ được giới hạn chữ lớn")


class TestStructure(unittest.TestCase):
    def test_declares_layer_order_first(self):
        first = next(
            line for line in CSS.splitlines()
            if line.strip() and not line.strip().startswith("/*")
        )
        self.assertEqual(
            first.strip(), "@layer tokens, base, layout, components, utilities;"
        )

    def test_has_focus_visible(self):
        self.assertIn(":focus-visible", CSS)

    def test_has_reduced_motion_guard(self):
        self.assertIn("prefers-reduced-motion", CSS)

    def test_no_three_pixel_accent_borders(self):
        # Spec §3.2 quy tắc 2 — bản cũ có 5 kiểu viền 3px khác nhau.
        self.assertEqual(re.findall(r"border[a-z-]*:\s*3px", CSS), [])

    def test_declares_both_font_families(self):
        self.assertIn("Be Vietnam Pro", CSS)
        self.assertIn("Inter", CSS)

    def test_uses_tabular_numerals_for_figures(self):
        self.assertIn("tabular-nums", CSS)

    def test_has_skip_link(self):
        self.assertIn(".skip-link", CSS)
