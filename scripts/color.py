"""Tính tương phản màu theo WCAG 2.1."""
from __future__ import annotations

import re

_HEX_TOKEN = re.compile(r"(--[a-z0-9-]+)\s*:\s*(#[0-9a-fA-F]{6})\s*;")

AA_NORMAL = 4.5
AA_LARGE = 3.0


def _channel(value: int) -> float:
    c = value / 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def relative_luminance(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    if len(h) != 6:
        raise ValueError(f"Màu hex phải có 6 ký tự: {hex_color!r}")
    r, g, b = (int(h[i : i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _channel(r) + 0.7152 * _channel(g) + 0.0722 * _channel(b)


def contrast_ratio(fg: str, bg: str) -> float:
    a, b = relative_luminance(fg), relative_luminance(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


def passes_aa(fg: str, bg: str, large: bool = False) -> bool:
    return contrast_ratio(fg, bg) >= (AA_LARGE if large else AA_NORMAL)


def parse_css_tokens(css_text: str) -> dict[str, str]:
    """Trích mọi token CSS có giá trị là màu hex 6 ký tự."""
    return {name: value.upper() for name, value in _HEX_TOKEN.findall(css_text)}
