"""Chuyển markdown rút gọn của blog sang HTML.

Phần `inline` và `md_to_html` chuyển nguyên từ scripts/build_blog.py — chúng đã
sinh đúng 12 bài hiện có, không viết lại. Phần anchor/slug là bổ sung mới cho
mục lục bài viết.
"""
from __future__ import annotations

import re
import unicodedata

_D_STROKE = str.maketrans({"đ": "d", "Đ": "D"})
_HEADING = re.compile(r"<(h[23])>(.*?)</\1>")


def inline(text: str) -> str:
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    return text


def md_to_html(md: str) -> str:
    lines = md.strip("\n").split("\n")
    html: list[str] = []
    i = 0

    def flush_list(buf: list[str], tag: str) -> None:
        if buf:
            html.append(f"<{tag}>")
            for item in buf:
                html.append(f"<li>{inline(item)}</li>")
            html.append(f"</{tag}>")
            buf.clear()

    ul_buf: list[str] = []
    ol_buf: list[str] = []
    table_buf: list[str] = []

    def flush_table() -> None:
        if not table_buf:
            return
        rows = [r for r in table_buf if not re.match(r"^\|[\s\-|]+\|$", r)]
        html.append("<table>")
        for idx, row in enumerate(rows):
            cells = [c.strip() for c in row.strip("|").split("|")]
            tag = "th" if idx == 0 else "td"
            html.append(
                "<tr>" + "".join(f"<{tag}>{inline(c)}</{tag}>" for c in cells) + "</tr>"
            )
        html.append("</table>")
        table_buf.clear()

    while i < len(lines):
        line = lines[i].strip()
        if not line:
            flush_list(ul_buf, "ul")
            flush_list(ol_buf, "ol")
            flush_table()
            i += 1
            continue
        if line.startswith("### "):
            flush_list(ul_buf, "ul")
            flush_list(ol_buf, "ol")
            flush_table()
            html.append(f"<h3>{inline(line[4:])}</h3>")
        elif line.startswith("## "):
            flush_list(ul_buf, "ul")
            flush_list(ol_buf, "ol")
            flush_table()
            html.append(f"<h2>{inline(line[3:])}</h2>")
        elif line.startswith("|"):
            table_buf.append(line)
        elif line.startswith("- "):
            flush_list(ol_buf, "ol")
            flush_table()
            ul_buf.append(line[2:])
        elif re.match(r"^\d+\.\s", line):
            flush_list(ul_buf, "ul")
            flush_table()
            ol_buf.append(re.sub(r"^\d+\.\s", "", line))
        else:
            flush_list(ul_buf, "ul")
            flush_list(ol_buf, "ol")
            flush_table()
            html.append(f"<p>{inline(line)}</p>")
        i += 1

    flush_list(ul_buf, "ul")
    flush_list(ol_buf, "ol")
    flush_table()
    return "\n".join(html)


def strip_front_matter(raw: str) -> str:
    """Bỏ khối metadata URL/Thumb/Title/Date ở đầu file raw."""
    if raw.startswith("URL:"):
        return re.split(r"\n\n", raw, maxsplit=1)[1].strip("\n")
    return raw


def slugify(text: str) -> str:
    """Bỏ dấu tiếng Việt, trả chuỗi an toàn cho thuộc tính id."""
    text = text.translate(_D_STROKE)
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    return re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()


def add_heading_anchors(html: str) -> tuple[str, list[tuple[int, str, str]]]:
    """Gắn id vào h2/h3 và trả về outline để dựng mục lục."""
    outline: list[tuple[int, str, str]] = []
    seen: dict[str, int] = {}

    def replace(match: re.Match) -> str:
        tag, text = match.group(1), match.group(2)
        base = slugify(re.sub(r"<[^>]+>", "", text))
        seen[base] = seen.get(base, 0) + 1
        anchor = base if seen[base] == 1 else f"{base}-{seen[base]}"
        outline.append((int(tag[1]), text, anchor))
        return f'<{tag} id="{anchor}">{text}</{tag}>'

    return _HEADING.sub(replace, html), outline
