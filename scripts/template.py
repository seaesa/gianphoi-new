"""Template engine tối giản cho site tĩnh. Không dependency.

Cú pháp:
    {{ name }}      chèn giá trị, có escape HTML
    {{{ name }}}    chèn thô (dùng cho HTML do component sinh ra)
    {{> partial }}  nạp partials_dir/partial.html rồi mở rộng đệ quy

Biến được thay trong MỘT lượt duy nhất, nên HTML chèn thô không bị quét lại —
nếu không, nội dung bài viết chứa "{{" sẽ bị hiểu nhầm là biến.
"""
from __future__ import annotations

import os
import re

_PARTIAL = re.compile(r"\{\{>\s*([a-z0-9_-]+)\s*\}\}")
_TAG = re.compile(
    r"\{\{\{\s*([a-zA-Z0-9_]+)\s*\}\}\}"  # group 1: chèn thô
    r"|\{\{\s*([a-zA-Z0-9_]+)\s*\}\}"  # group 2: chèn có escape
)

MAX_DEPTH = 10


class TemplateError(ValueError):
    """Template tham chiếu biến hoặc partial không tồn tại."""


def escape(text: object) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def _expand_partials(text: str, partials_dir: str, depth: int = 0) -> str:
    if depth > MAX_DEPTH:
        raise TemplateError("Partial lồng nhau quá sâu — có thể bị vòng lặp")

    def replace(match: re.Match) -> str:
        name = match.group(1)
        path = os.path.join(partials_dir, f"{name}.html")
        if not os.path.exists(path):
            raise TemplateError(f"Không tìm thấy partial {name!r} tại {path}")
        with open(path, encoding="utf-8") as handle:
            return _expand_partials(handle.read(), partials_dir, depth + 1)

    return _PARTIAL.sub(replace, text)


def render(template_str: str, context: dict, *, partials_dir: str) -> str:
    text = _expand_partials(template_str, partials_dir)

    def replace(match: re.Match) -> str:
        raw_name, esc_name = match.group(1), match.group(2)
        name = raw_name or esc_name
        if name not in context:
            raise TemplateError(f"Template dùng biến {name!r} nhưng context không có")
        value = context[name]
        return str(value) if raw_name else escape(value)

    return _TAG.sub(replace, text)


def render_file(path: str, context: dict, *, partials_dir: str) -> str:
    with open(path, encoding="utf-8") as handle:
        return render(handle.read(), context, partials_dir=partials_dir)
