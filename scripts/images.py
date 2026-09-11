"""Tối ưu ảnh: WebP, srcset, kích thước tường minh chống CLS."""
from __future__ import annotations

import os
from dataclasses import dataclass

from PIL import Image

from scripts.sitedata import ROOT
from scripts.template import escape

DEFAULT_WIDTHS = (480, 960, 1440)
WEBP_QUALITY = 78
# Ngân sách mỗi file. Ảnh nào vượt sẽ được mã hoá lại ở chất lượng thấp hơn
# cho tới khi lọt ngưỡng — không ảnh nào được phép làm chậm trang.
MAX_BYTES = 200 * 1024
MIN_QUALITY = 55


@dataclass(frozen=True)
class ImageInfo:
    path: str
    width: int
    height: int


def resolve(path: str) -> str:
    """Đổi đường dẫn kiểu URL (/assets/...) thành đường dẫn hệ thống tệp."""
    if os.path.isabs(path) and os.path.exists(path):
        return path
    return os.path.join(ROOT, path.lstrip("/").replace("/", os.sep))


def probe(path: str) -> ImageInfo:
    full = resolve(path)
    with Image.open(full) as img:
        return ImageInfo(path, img.width, img.height)


def make_variants(
    src: str, out_dir: str, widths: tuple[int, ...] = DEFAULT_WIDTHS
) -> list[ImageInfo]:
    """Sinh các bản WebP theo chiều rộng. Bỏ qua bản rộng hơn ảnh gốc."""
    os.makedirs(out_dir, exist_ok=True)
    stem = os.path.splitext(os.path.basename(src))[0]
    out: list[ImageInfo] = []
    with Image.open(resolve(src)) as img:
        img = img.convert("RGB")
        for width in widths:
            if width > img.width:
                continue
            height = round(img.height * width / img.width)
            resized = img.resize((width, height), Image.LANCZOS)
            path = os.path.join(out_dir, f"{stem}-{width}.webp")
            quality = WEBP_QUALITY
            while True:
                resized.save(path, "WEBP", quality=quality, method=6)
                if os.path.getsize(path) <= MAX_BYTES or quality <= MIN_QUALITY:
                    break
                quality -= 6
            out.append(ImageInfo(path, width, height))
    return out


def srcset_attr(variants: list[ImageInfo]) -> str:
    return ", ".join(f"{v.path} {v.width}w" for v in variants)


def image_tag(
    src: str,
    alt: str,
    *,
    sizes: str,
    lazy: bool = True,
    variants: list[ImageInfo] | None = None,
    decorative: bool = False,
    classes: str = "",
) -> str:
    if not alt and not decorative:
        raise ValueError(
            f"Ảnh {src!r} thiếu alt — truyền decorative=True nếu là ảnh trang trí"
        )
    info = probe(src)
    attrs = [f'src="{src}"', f'alt="{escape(alt)}"']
    if classes:
        attrs.insert(0, f'class="{classes}"')
    attrs += [f'width="{info.width}"', f'height="{info.height}"']
    if variants:
        attrs.append(f'srcset="{srcset_attr(variants)}"')
        attrs.append(f'sizes="{sizes}"')
    if lazy:
        attrs += ['loading="lazy"', 'decoding="async"']
    return "<img " + " ".join(attrs) + ">"
