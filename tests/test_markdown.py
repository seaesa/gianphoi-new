import unittest

from scripts.markdown import (
    add_heading_anchors,
    md_to_html,
    slugify,
    strip_front_matter,
)


class TestMdToHtml(unittest.TestCase):
    def test_paragraph(self):
        self.assertEqual(md_to_html("Xin chào."), "<p>Xin chào.</p>")

    def test_headings(self):
        self.assertEqual(md_to_html("## Lợi ích"), "<h2>Lợi ích</h2>")
        self.assertEqual(md_to_html("### Chi tiết"), "<h3>Chi tiết</h3>")

    def test_unordered_list(self):
        self.assertEqual(
            md_to_html("- Một\n- Hai"),
            "<ul>\n<li>Một</li>\n<li>Hai</li>\n</ul>",
        )

    def test_ordered_list(self):
        self.assertEqual(
            md_to_html("1. Khảo sát\n2. Báo giá"),
            "<ol>\n<li>Khảo sát</li>\n<li>Báo giá</li>\n</ol>",
        )

    def test_bold_inline(self):
        self.assertEqual(
            md_to_html("Giá **rẻ** nhất"), "<p>Giá <strong>rẻ</strong> nhất</p>"
        )

    def test_escapes_html_entities(self):
        self.assertIn("&amp;", md_to_html("TP.HCM & Bình Dương"))
        self.assertIn("&lt;script&gt;", md_to_html("<script>"))

    def test_table_first_row_is_header(self):
        html = md_to_html("| A | B |\n| --- | --- |\n| 1 | 2 |")
        self.assertIn("<th>A</th>", html)
        self.assertIn("<td>1</td>", html)
        self.assertNotIn("---", html)


class TestStripFrontMatter(unittest.TestCase):
    def test_removes_metadata_block(self):
        raw = "URL: https://x\nTitle: Y\nDate: 1/1/2025\n\n## Nội dung"
        self.assertEqual(strip_front_matter(raw), "## Nội dung")

    def test_leaves_plain_markdown_untouched(self):
        self.assertEqual(strip_front_matter("## Nội dung"), "## Nội dung")


class TestSlugify(unittest.TestCase):
    def test_strips_vietnamese_diacritics(self):
        self.assertEqual(slugify("Lợi ích nổi bật"), "loi-ich-noi-bat")

    def test_handles_d_with_stroke(self):
        self.assertEqual(slugify("Đặc điểm"), "dac-diem")

    def test_drops_punctuation(self):
        self.assertEqual(slugify("Giá bao nhiêu?"), "gia-bao-nhieu")


class TestAddHeadingAnchors(unittest.TestCase):
    def test_adds_ids_and_returns_outline(self):
        html, outline = add_heading_anchors(
            "<h2>Lợi ích</h2>\n<p>x</p>\n<h3>Chi tiết</h3>"
        )
        self.assertIn('<h2 id="loi-ich">', html)
        self.assertIn('<h3 id="chi-tiet">', html)
        self.assertEqual(outline, [(2, "Lợi ích", "loi-ich"), (3, "Chi tiết", "chi-tiet")])

    def test_deduplicates_repeated_headings(self):
        html, outline = add_heading_anchors("<h2>Giá</h2><h2>Giá</h2>")
        self.assertEqual([a for _, _, a in outline], ["gia", "gia-2"])
        self.assertIn('id="gia-2"', html)

    def test_leaves_other_tags_alone(self):
        html, outline = add_heading_anchors("<p>Không phải heading</p>")
        self.assertEqual(html, "<p>Không phải heading</p>")
        self.assertEqual(outline, [])
