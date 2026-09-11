import glob
import os
import unittest

from scripts.images import ImageInfo, image_tag, probe, srcset_attr

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(ROOT, "assets", "images")

MAX_BYTES = 200 * 1024


class TestProbe(unittest.TestCase):
    def test_returns_real_dimensions(self):
        info = probe(os.path.join(IMG_DIR, "logo.png"))
        self.assertGreater(info.width, 0)
        self.assertGreater(info.height, 0)

    def test_accepts_site_root_url(self):
        info = probe("/assets/images/logo.png")
        self.assertGreater(info.width, 0)


class TestSrcsetAttr(unittest.TestCase):
    def test_formats_width_descriptors(self):
        variants = [
            ImageInfo("/assets/images/x-480.webp", 480, 320),
            ImageInfo("/assets/images/x-960.webp", 960, 640),
        ]
        self.assertEqual(
            srcset_attr(variants),
            "/assets/images/x-480.webp 480w, /assets/images/x-960.webp 960w",
        )


class TestImageTag(unittest.TestCase):
    def test_always_emits_dimensions(self):
        tag = image_tag("/assets/images/logo.png", "Logo", sizes="40px")
        self.assertIn("width=", tag)
        self.assertIn("height=", tag)

    def test_lazy_by_default(self):
        tag = image_tag("/assets/images/logo.png", "Logo", sizes="40px")
        self.assertIn('loading="lazy"', tag)
        self.assertIn('decoding="async"', tag)

    def test_eager_when_requested(self):
        tag = image_tag("/assets/images/logo.png", "Logo", sizes="40px", lazy=False)
        self.assertNotIn("lazy", tag)

    def test_escapes_alt_text(self):
        tag = image_tag("/assets/images/logo.png", 'Giàn "A" & B', sizes="40px")
        self.assertIn("&quot;", tag)
        self.assertIn("&amp;", tag)

    def test_rejects_empty_alt_without_explicit_decorative_flag(self):
        with self.assertRaises(ValueError):
            image_tag("/assets/images/logo.png", "", sizes="40px")

    def test_emits_srcset_when_variants_given(self):
        variants = [ImageInfo("/assets/images/x-480.webp", 480, 320)]
        tag = image_tag(
            "/assets/images/logo.png", "Logo", sizes="40px", variants=variants
        )
        self.assertIn("srcset=", tag)
        self.assertIn('sizes="40px"', tag)


class TestOptimisedAssets(unittest.TestCase):
    def test_no_shipped_image_exceeds_budget(self):
        oversized = []
        for dirpath, _dirnames, filenames in os.walk(IMG_DIR):
            if "_src" in dirpath:
                continue
            for name in filenames:
                path = os.path.join(dirpath, name)
                if os.path.getsize(path) > MAX_BYTES:
                    oversized.append(
                        (os.path.relpath(path, ROOT), os.path.getsize(path) // 1024)
                    )
        self.assertEqual(oversized, [], f"Ảnh quá nặng (KB): {oversized}")

    def test_originals_are_kept_out_of_the_shipped_tree(self):
        self.assertTrue(os.path.isdir(os.path.join(IMG_DIR, "_src")))

    def test_unused_stock_photos_are_not_shipped(self):
        """Ảnh stock sai chủ đề đã bị thay bằng hình vẽ nét — không ship nữa."""
        for name in ("hero-banner.jpg", "about-thi-cong.jpg",
                     "nhan-vien-huong-dan.jpg", "thi-cong.jpeg"):
            with self.subTest(name=name):
                self.assertFalse(os.path.exists(os.path.join(IMG_DIR, name)))

    def test_unused_service_and_project_photos_are_not_shipped(self):
        for folder in ("services", "projects"):
            with self.subTest(folder=folder):
                self.assertFalse(os.path.isdir(os.path.join(IMG_DIR, folder)))


class TestAltTextHonesty(unittest.TestCase):
    """Spec §2.2 — alt text phải mô tả đúng nội dung ảnh."""

    FORBIDDEN = [
        "Khách hàng vui vẻ trên ban công căn hộ hiện đại tại Việt Nam",
        "Kỹ thuật viên đang thao tác lắp đặt, thi công thực tế",
        "Thủ Đức – Giàn phơi thông minh gắn tường",
        "Quận 7 – Giàn phơi điều khiển từ xa",
    ]

    def test_no_page_reuses_the_false_alt_text(self):
        pages = glob.glob(os.path.join(ROOT, "*.html")) + glob.glob(
            os.path.join(ROOT, "blog", "*.html")
        )
        self.assertTrue(pages)
        for path in pages:
            with open(path, encoding="utf-8") as handle:
                html = handle.read()
            for phrase in self.FORBIDDEN:
                with self.subTest(page=os.path.basename(path), phrase=phrase[:30]):
                    self.assertNotIn(phrase, html)
