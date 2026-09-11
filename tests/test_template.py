import os
import tempfile
import unittest

from scripts.template import TemplateError, escape, render, render_file


class TestEscape(unittest.TestCase):
    def test_escapes_the_five_entities(self):
        self.assertEqual(
            escape('<a href="x">&\'</a>'),
            "&lt;a href=&quot;x&quot;&gt;&amp;&#39;&lt;/a&gt;",
        )


class TestRender(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.partials = self.tmp.name
        self.addCleanup(self.tmp.cleanup)

    def write_partial(self, name: str, content: str) -> None:
        with open(os.path.join(self.partials, f"{name}.html"), "w", encoding="utf-8") as handle:
            handle.write(content)

    def test_substitutes_variable(self):
        out = render("Xin chào {{ name }}", {"name": "An"}, partials_dir=self.partials)
        self.assertEqual(out, "Xin chào An")

    def test_escapes_by_default(self):
        out = render("{{ v }}", {"v": "<b>x</b>"}, partials_dir=self.partials)
        self.assertEqual(out, "&lt;b&gt;x&lt;/b&gt;")

    def test_triple_brace_is_raw(self):
        out = render("{{{ v }}}", {"v": "<b>x</b>"}, partials_dir=self.partials)
        self.assertEqual(out, "<b>x</b>")

    def test_tolerates_whitespace_in_tag(self):
        self.assertEqual(render("{{name}}", {"name": "An"}, partials_dir=self.partials), "An")

    def test_includes_partial(self):
        self.write_partial("hello", "<p>{{ name }}</p>")
        out = render("{{> hello }}", {"name": "An"}, partials_dir=self.partials)
        self.assertEqual(out, "<p>An</p>")

    def test_partial_can_include_partial(self):
        self.write_partial("inner", "<i>{{ name }}</i>")
        self.write_partial("outer", "<b>{{> inner }}</b>")
        out = render("{{> outer }}", {"name": "An"}, partials_dir=self.partials)
        self.assertEqual(out, "<b><i>An</i></b>")

    def test_missing_variable_raises(self):
        with self.assertRaises(TemplateError) as ctx:
            render("{{ vang_mat }}", {}, partials_dir=self.partials)
        self.assertIn("vang_mat", str(ctx.exception))

    def test_missing_partial_raises(self):
        with self.assertRaises(TemplateError) as ctx:
            render("{{> khong-co }}", {}, partials_dir=self.partials)
        self.assertIn("khong-co", str(ctx.exception))

    def test_non_string_values_are_stringified(self):
        self.assertEqual(render("{{ n }}", {"n": 8}, partials_dir=self.partials), "8")

    def test_raw_value_is_not_rescanned_for_tags(self):
        """HTML do component sinh ra có thể chứa {{ — không được coi là biến."""
        out = render("{{{ body }}}", {"body": "<p>{{ khong_phai_bien }}</p>"}, partials_dir=self.partials)
        self.assertEqual(out, "<p>{{ khong_phai_bien }}</p>")

    def test_circular_partial_raises(self):
        self.write_partial("a", "{{> b }}")
        self.write_partial("b", "{{> a }}")
        with self.assertRaises(TemplateError):
            render("{{> a }}", {}, partials_dir=self.partials)


class TestRenderFile(unittest.TestCase):
    def test_reads_and_renders(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "page.html")
            with open(path, "w", encoding="utf-8") as handle:
                handle.write("<h1>{{ title }}</h1>")
            out = render_file(path, {"title": "Trang chủ"}, partials_dir=tmp)
            self.assertEqual(out, "<h1>Trang chủ</h1>")
