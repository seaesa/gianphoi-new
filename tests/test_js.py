import os
import re
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JS_PATH = os.path.join(ROOT, "assets", "js", "main.js")

with open(JS_PATH, encoding="utf-8") as handle:
    JS = handle.read()


class TestNoLegacyCode(unittest.TestCase):
    def test_include_loader_is_gone(self):
        self.assertNotIn("data-include", JS)
        self.assertNotIn("includes:loaded", JS)

    def test_faq_no_longer_uses_max_height_hack(self):
        self.assertNotIn("scrollHeight", JS)

    def test_no_references_to_removed_class_names(self):
        for dead in (".faq-item", ".nav-list", "#contact-form", "nav-open"):
            with self.subTest(selector=dead):
                self.assertNotIn(dead, JS)


class TestAccessibility(unittest.TestCase):
    def test_nav_toggle_updates_aria_expanded(self):
        self.assertIn("aria-expanded", JS)

    def test_faq_updates_aria_expanded(self):
        self.assertGreaterEqual(JS.count("aria-expanded"), 2)

    def test_escape_closes_mobile_nav(self):
        self.assertIn("Escape", JS)

    def test_respects_reduced_motion(self):
        self.assertIn("prefers-reduced-motion", JS)


class TestFeatures(unittest.TestCase):
    def test_has_sticky_bar_scroll_behaviour(self):
        self.assertIn("sticky-bar", JS)

    def test_has_chip_filtering(self):
        self.assertIn("data-filter", JS)

    def test_has_inline_form_validation(self):
        self.assertIn("field__error", JS)

    def test_form_submission_is_flagged_as_placeholder(self):
        self.assertIn("TODO", JS)
        self.assertRegex(JS, r"TODO[^\n]*(endpoint|backend|Formspree|Zalo)")

    def test_preselects_service_from_query_string(self):
        # Link "Nhận báo giá" trên card mang ?dich-vu=<slug>.
        self.assertIn("dich-vu", JS)


class TestRobustness(unittest.TestCase):
    def test_guards_every_query_selector_result(self):
        """Script chạy trên mọi trang — phần tử vắng mặt không được ném lỗi."""
        self.assertNotRegex(JS, r"querySelector\([^)]*\)\.\w+\s*=")

    def test_uses_event_listeners_not_inline_handlers(self):
        self.assertIn("addEventListener", JS)
