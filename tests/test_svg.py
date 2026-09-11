import os
import unittest
import xml.etree.ElementTree as ET

from scripts.sitedata import load_site

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SVG_DIR = os.path.join(ROOT, "assets", "svg")
SITE = load_site()

SVG_NS = "{http://www.w3.org/2000/svg}"


def read(service) -> str:
    with open(os.path.join(SVG_DIR, service.svg), encoding="utf-8") as handle:
        return handle.read()


class TestProductLineDrawings(unittest.TestCase):
    def test_one_svg_per_service(self):
        for service in SITE.services:
            with self.subTest(service=service.slug):
                self.assertTrue(os.path.exists(os.path.join(SVG_DIR, service.svg)))

    def test_all_share_the_same_viewbox(self):
        for service in SITE.services:
            with self.subTest(service=service.slug):
                root = ET.parse(os.path.join(SVG_DIR, service.svg)).getroot()
                self.assertEqual(root.get("viewBox"), "0 0 240 180")

    def test_stroke_style_is_consistent(self):
        for service in SITE.services:
            with self.subTest(service=service.slug):
                text = read(service)
                self.assertIn('stroke-width="1.5"', text)
                self.assertIn('stroke="currentColor"', text)
                self.assertIn('fill="none"', text)

    def test_no_hardcoded_colour(self):
        """Màu đến từ CSS qua currentColor — SVG không được ghim hex."""
        for service in SITE.services:
            with self.subTest(service=service.slug):
                self.assertNotIn("#", read(service))

    def test_has_accessible_title(self):
        for service in SITE.services:
            with self.subTest(service=service.slug):
                root = ET.parse(os.path.join(SVG_DIR, service.svg)).getroot()
                title = root.find(f"{SVG_NS}title")
                self.assertIsNotNone(title, "SVG thiếu <title>")
                self.assertTrue(title.text.strip())

    def test_drawing_is_not_trivially_empty(self):
        for service in SITE.services:
            with self.subTest(service=service.slug):
                text = read(service)
                marks = sum(
                    text.count(f"<{tag}")
                    for tag in ("path", "line", "rect", "circle", "polyline")
                )
                self.assertGreaterEqual(marks, 4, "Hình quá sơ sài, cần ít nhất 4 nét")

    def test_marks_stay_inside_the_safe_margin(self):
        """Mọi toạ độ nằm trong 16..224 (x) và 16..164 (y) để có lề đều."""
        for service in SITE.services:
            with self.subTest(service=service.slug):
                root = ET.parse(os.path.join(SVG_DIR, service.svg)).getroot()
                for element in root.iter():
                    for attr, lo, hi in (
                        ("x1", 16, 224), ("x2", 16, 224),
                        ("y1", 16, 164), ("y2", 16, 164),
                    ):
                        raw = element.get(attr)
                        if raw is None:
                            continue
                        value = float(raw)
                        self.assertGreaterEqual(value, lo, f"{attr}={value}")
                        self.assertLessEqual(value, hi, f"{attr}={value}")
