"""Sinh toàn bộ HTML tĩnh từ site.json + templates/.

Chạy: python -m scripts.build

Header, footer và JSON-LD được ghi thẳng vào từng file HTML tại thời điểm
build — không còn nạp bằng fetch như bản cũ, nên Google đọc được và trang
không bị nháy khi tải.
"""
from __future__ import annotations

import datetime
import os

from scripts import components, schema
from scripts.sitedata import ROOT, SiteData, find_service, load_site
from scripts.template import render_file

TEMPLATES = os.path.join(ROOT, "templates")
SVG_DIR = os.path.join(ROOT, "assets", "svg")

# Năm bước quy trình — lấy nguyên văn từ dich-vu.html bản cũ.
PROCESS_STEPS = [
    ("Tiếp nhận yêu cầu",
     "Khách hàng liên hệ qua hotline, Zalo hoặc form website để được tư vấn miễn phí."),
    ("Khảo sát thực tế",
     "Kỹ thuật viên đến tận nơi đo đạc, tư vấn loại phù hợp cho từng không gian."),
    ("Báo giá chi tiết",
     "Gửi báo giá minh bạch từng hạng mục, vật liệu và chi phí thi công."),
    ("Thi công lắp đặt",
     "Đội ngũ kỹ thuật lắp đặt nhanh gọn, đúng tiến độ, dọn dẹp sạch sẽ."),
    ("Bảo hành & chăm sóc",
     "Hỗ trợ bảo hành, bảo trì định kỳ giúp sản phẩm luôn hoạt động tốt."),
]

# Ba tình huống ở tầng quyết định trên trang chủ (sửa lỗi C6).
USE_CASES = [
    ("Ban công chung cư nhỏ",
     "Gấp gọn sát tường, trả lại lối đi khi không dùng.",
     "gian-phoi-xep-tuong"),
    ("Sân thượng, nhà phố",
     "Hai thanh phơi inox 304, tải trọng tới 70 kg cho cả gia đình.",
     "gian-phoi-treo-tran"),
    ("Muốn nâng hạ tự động",
     "Điều khiển bằng remote, không cần quay tay.",
     "gian-phoi-dieu-khien"),
]

HOURS_DISPLAY = "08:00 – 18:00, tất cả các ngày"


def read_svg(name: str) -> str:
    with open(os.path.join(SVG_DIR, name), encoding="utf-8") as handle:
        return handle.read()


def _write(path: str, html: str) -> str:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(html)
    return path


def shell_context(site: SiteData, *, page_id: str, **extra) -> dict:
    """Context mà mọi trang đều cần (header, footer, sticky bar)."""
    business = site.business
    return {
        "page_id": page_id,
        "business_name": business.name,
        "tagline": business.tagline,
        "phone": business.phone,
        "phone_display": business.phone_display,
        "zalo_url": business.zalo_url,
        "email": business.email,
        "street": business.street,
        "city": business.city,
        "hours_display": HOURS_DISPLAY,
        "year": datetime.date.today().year,
        "nav_list": components.nav_list(page_id),
        "footer_services": components.footer_services(site),
        "icon_phone": components.icon("phone"),
        "icon_zalo": components.icon("zalo"),
        "icon_quote": components.icon("quote"),
        **extra,
    }


def render_page(
    site: SiteData,
    *,
    template: str,
    out: str,
    page_id: str,
    title: str,
    description: str,
    path: str,
    jsonld: str,
    main_context: dict | None = None,
) -> str:
    main = render_file(
        os.path.join(TEMPLATES, template),
        shell_context(site, page_id=page_id, **(main_context or {})),
        partials_dir=TEMPLATES,
    )
    html = render_file(
        os.path.join(TEMPLATES, "_base.html"),
        shell_context(
            site,
            page_id=page_id,
            main=main,
            title=title,
            description=description,
            canonical=f"{schema.BASE_URL}{path}",
            og_image=f"{schema.BASE_URL}/assets/images/logo.png",
            jsonld=jsonld,
        ),
        partials_dir=TEMPLATES,
    )
    return _write(os.path.join(ROOT, out), html)


def build_home(site: SiteData) -> str:
    featured = site.services[:4]
    usecases = "\n".join(
        components.usecase_card(
            title, body, find_service(site, slug), svg_inline=read_svg(f"{slug}.svg")
        )
        for title, body, slug in USE_CASES
    )
    cards = "\n".join(
        components.service_card(s, svg_inline=read_svg(s.svg)) for s in featured
    )
    posts = "\n".join(components.post_card(p) for p in site.posts[:3])

    return render_page(
        site,
        template="index.html",
        out="index.html",
        page_id="home",
        title=f"{site.business.name} | Lắp đặt chính hãng",
        description=site.business.tagline,
        path="/",
        jsonld=schema.to_jsonld(schema.local_business(site)),
        main_context={
            "hero_svg": read_svg("gian-phoi-dieu-khien.svg"),
            "rail": components.numeric_rail(site.facts),
            "usecases": usecases,
            "service_cards": cards,
            "stepper": components.stepper(PROCESS_STEPS),
            "areas": components.area_list(site.areas),
            "posts": posts,
        },
    )


def build(root: str = ROOT) -> list[str]:
    site = load_site()
    return [build_home(site)]


def main() -> None:
    for path in build():
        print("wrote", os.path.relpath(path, ROOT))


if __name__ == "__main__":
    main()
