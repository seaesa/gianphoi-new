"""Sinh ảnh WebP đã tối ưu từ assets/images/_src/site/ sang cây deploy.

Chạy lại được bất cứ lúc nào:

    python -m scripts.optimize_images

Ảnh gốc nằm trong _src/ và không được deploy (đã chặn trong robots.txt).
Mỗi ảnh sinh hai bản 480w và 960w; bản nào vượt ngân sách byte sẽ tự động
được mã hoá lại ở chất lượng thấp hơn — xem scripts/images.py.
"""
from __future__ import annotations

import glob
import os

from scripts.images import make_variants
from scripts.sitedata import ROOT

SRC = os.path.join(ROOT, "assets", "images", "_src", "site")
OUT = os.path.join(ROOT, "assets", "images")

WIDTHS = (480, 960)

# thư mục nguồn -> thư mục đích trong cây deploy
FOLDERS = {
    "services": "services",
    "projects": "projects",
    "blog": "blog",
    "": "",  # hero.jpg, team.jpg nằm ngay gốc
}


def optimize() -> list[str]:
    written: list[str] = []
    for src_folder, out_folder in FOLDERS.items():
        src_dir = os.path.join(SRC, src_folder) if src_folder else SRC
        out_dir = os.path.join(OUT, out_folder) if out_folder else OUT
        pattern = os.path.join(src_dir, "*.*")
        for path in sorted(glob.glob(pattern)):
            if os.path.isdir(path):
                continue
            for variant in make_variants(path, out_dir, widths=WIDTHS):
                written.append(variant.path)
    return written


def main() -> None:
    written = optimize()
    total = sum(os.path.getsize(p) for p in written)
    print(f"đã sinh {len(written)} file, tổng {total // 1024} KB")
    for path in written:
        print(" ", os.path.relpath(path, ROOT), f"{os.path.getsize(path) // 1024}KB")


if __name__ == "__main__":
    main()
