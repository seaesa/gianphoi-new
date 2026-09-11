import unittest

from scripts.color import (
    contrast_ratio,
    parse_css_tokens,
    passes_aa,
    relative_luminance,
)


class TestRelativeLuminance(unittest.TestCase):
    def test_white_is_one(self):
        self.assertAlmostEqual(relative_luminance("#FFFFFF"), 1.0, places=4)

    def test_black_is_zero(self):
        self.assertAlmostEqual(relative_luminance("#000000"), 0.0, places=4)

    def test_accepts_lowercase_and_no_hash(self):
        self.assertAlmostEqual(
            relative_luminance("ffffff"), relative_luminance("#FFFFFF"), places=6
        )


class TestContrastRatio(unittest.TestCase):
    def test_black_on_white_is_21(self):
        self.assertAlmostEqual(contrast_ratio("#000000", "#FFFFFF"), 21.0, places=2)

    def test_is_symmetric(self):
        self.assertAlmostEqual(
            contrast_ratio("#0F1C26", "#FBFAF8"),
            contrast_ratio("#FBFAF8", "#0F1C26"),
            places=6,
        )

    def test_white_on_amber_passes_aa(self):
        # Token --amber #B4530A, nền nút CTA chính. Spec §3.3 ghi 5.02:1.
        self.assertAlmostEqual(contrast_ratio("#FFFFFF", "#B4530A"), 5.02, places=2)

    def test_old_accent_failed_aa(self):
        # Màu cũ #C5652B chỉ đạt 3.98:1 — đây là lý do phải đổi.
        self.assertLess(contrast_ratio("#FFFFFF", "#C5652B"), 4.5)


class TestPassesAA(unittest.TestCase):
    def test_normal_text_threshold(self):
        self.assertTrue(passes_aa("#0F1C26", "#FBFAF8"))
        self.assertFalse(passes_aa("#E07A1F", "#1E3446"))

    def test_large_text_threshold(self):
        # --amber-bright chỉ hợp lệ ở chữ lớn: 4.27:1 >= 3.0
        self.assertTrue(passes_aa("#E07A1F", "#1E3446", large=True))


class TestParseCssTokens(unittest.TestCase):
    def test_extracts_hex_tokens_from_root(self):
        css = """
        @layer tokens {
          :root {
            --ink: #0F1C26;
            --paper: #FBFAF8;
            --r: 10px;
          }
        }
        """
        tokens = parse_css_tokens(css)
        self.assertEqual(tokens["--ink"], "#0F1C26")
        self.assertEqual(tokens["--paper"], "#FBFAF8")

    def test_ignores_non_hex_values(self):
        css = ":root { --r: 10px; --container: 1200px; }"
        self.assertEqual(parse_css_tokens(css), {})
