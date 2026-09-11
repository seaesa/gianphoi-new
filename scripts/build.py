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


GROUP_ANCHORS = {
    "Giàn phơi": ("gian-phoi", "Ba kiểu nâng hạ cho ba kiểu không gian."),
    "An toàn ban công": (
        "an-toan-ban-cong",
        "Chắn côn trùng và bảo vệ trẻ nhỏ mà vẫn thoáng gió.",
    ),
    "Che chắn": ("che-chan", "Giữ nhiệt, chắn nắng và chắn mưa cho ban công, sân thượng."),
}


def _service_group_sections(site: SiteData) -> str:
    """Ba nhóm dịch vụ, mỗi nhóm một section có anchor riêng (sửa lỗi C6)."""
    from scripts.sitedata import service_groups

    blocks = []
    for index, (group, services) in enumerate(service_groups(site)):
        anchor, blurb = GROUP_ANCHORS[group]
        band = "band--paper" if index % 2 == 0 else "band--surface"
        cards = "\n".join(
            components.service_card(s, svg_inline=read_svg(s.svg)) for s in services
        )
        blocks.append(
            f'  <section class="band {band}" id="{anchor}">\n'
            f'    <div class="container">\n'
            f'      <div class="section-head">\n'
            f'        <span class="eyebrow">Nhóm {index + 1} / 3</span>\n'
            f"        <h2>{group}</h2>\n"
            f"        <p>{blurb}</p>\n"
            f"      </div>\n"
            f'      <div class="grid grid--3">\n'
            f"{cards}\n"
            f"      </div>\n"
            f"    </div>\n"
            f"  </section>"
        )
    return "\n\n".join(blocks)


def build_services(site: SiteData) -> str:
    crumbs = [("Trang chủ", "/"), ("Dịch vụ & Bảng giá", "/dich-vu.html")]
    jsonld = schema.to_jsonld(
        schema.local_business(site),
        *[schema.service_schema(site, s) for s in site.services],
        schema.faq_page(site.faqs),
        schema.breadcrumb_list(crumbs),
    )
    return render_page(
        site,
        template="dich-vu.html",
        out="dich-vu.html",
        page_id="services",
        title=f"Dịch vụ & Bảng giá | {site.business.name}",
        description=(
            "Bảng giá lắp đặt giàn phơi thông minh, lưới cáp ban công, cửa lưới chống "
            "muỗi, vách ngăn lạnh, mái hiên và bạt che nắng mưa tại TP.HCM & Bình Dương."
        ),
        path="/dich-vu.html",
        jsonld=jsonld,
        main_context={
            "groups": _service_group_sections(site),
            "comparison": components.comparison_table(site),
            "stepper": components.stepper(PROCESS_STEPS),
            "faqs": components.faq_list(site.faqs),
        },
    )


def build_areas(site: SiteData) -> str:
    import urllib.parse

    crumbs = [("Trang chủ", "/"), ("Khu vực phục vụ", "/khu-vuc.html")]
    query = urllib.parse.quote(site.business.maps_query)
    return render_page(
        site,
        template="khu-vuc.html",
        out="khu-vuc.html",
        page_id="areas",
        title=f"Khu vực phục vụ | {site.business.name}",
        description=(
            "Khu vực nhận khảo sát và thi công giàn phơi thông minh, lưới cáp ban công "
            "tại TP.HCM và Bình Dương."
        ),
        path="/khu-vuc.html",
        jsonld=schema.to_jsonld(
            schema.local_business(site), schema.breadcrumb_list(crumbs)
        ),
        main_context={
            "areas": components.area_list(site.areas),
            "map_src": f"https://www.google.com/maps?q={query}&output=embed",
        },
    )


def build_about(site: SiteData) -> str:
    crumbs = [("Trang chủ", "/"), ("Giới thiệu", "/gioi-thieu.html")]
    usecases = "\n".join(
        components.usecase_card(
            title, body, find_service(site, slug), svg_inline=read_svg(f"{slug}.svg")
        )
        for title, body, slug in USE_CASES
    )
    return render_page(
        site,
        template="gioi-thieu.html",
        out="gioi-thieu.html",
        page_id="about",
        title=f"Giới thiệu | {site.business.name}",
        description=(
            "Hơn 10 năm kinh nghiệm lắp đặt và sửa chữa giàn phơi thông minh, lưới cáp "
            "ban công tại TP.HCM và Bình Dương."
        ),
        path="/gioi-thieu.html",
        jsonld=schema.to_jsonld(
            schema.local_business(site), schema.breadcrumb_list(crumbs)
        ),
        main_context={
            "rail": components.numeric_rail(site.facts),
            "usecases": usecases,
        },
    )


def build_contact(site: SiteData) -> str:
    import urllib.parse

    crumbs = [("Trang chủ", "/"), ("Liên hệ", "/lien-he.html")]
    query = urllib.parse.quote(site.business.maps_query)
    contact_faqs = tuple(f for f in site.faqs if f.contact_page)
    return render_page(
        site,
        template="lien-he.html",
        out="lien-he.html",
        page_id="contact",
        title=f"Liên hệ & nhận báo giá | {site.business.name}",
        description=(
            "Gọi hotline, nhắn Zalo hoặc để lại thông tin để nhận báo giá lắp đặt giàn "
            "phơi thông minh, lưới cáp ban công tại TP.HCM và Bình Dương."
        ),
        path="/lien-he.html",
        jsonld=schema.to_jsonld(
            schema.local_business(site), schema.breadcrumb_list(crumbs)
        ),
        main_context={
            "service_options": components.service_options(site),
            "faqs": components.faq_list(contact_faqs, id_prefix="faq-lien-he"),
            "map_src": f"https://www.google.com/maps?q={query}&output=embed",
        },
    )


def build_blog_index(site: SiteData) -> str:
    crumbs = [("Trang chủ", "/"), ("Blog", "/blog.html")]
    return render_page(
        site,
        template="blog.html",
        out="blog.html",
        page_id="blog",
        title=f"Blog | {site.business.name}",
        description=(
            "Kinh nghiệm chọn mua giàn phơi thông minh, so sánh thương hiệu và hướng "
            "dẫn lắp đặt theo từng khu vực tại TP.HCM và Bình Dương."
        ),
        path="/blog.html",
        jsonld=schema.to_jsonld(
            schema.local_business(site), schema.breadcrumb_list(crumbs)
        ),
        main_context={
            "posts": "\n".join(components.post_card(p) for p in site.posts),
        },
    )


# Ánh xạ bài viết sang dịch vụ liên quan cho sidebar chuyển đổi.
POST_SERVICE_HINTS = (
    ("vach-lanh", "vach-ngan-lanh"),
    ("mua-mua", "bat-che-nang-mua"),
    ("mui-hoi", "gian-phoi-dieu-khien"),
    ("chung-cu", "gian-phoi-xep-tuong"),
    ("giai-phap-khong-gian", "gian-phoi-xep-tuong"),
)


def _related_service(site: SiteData, slug: str):
    for needle, service_slug in POST_SERVICE_HINTS:
        if needle in slug:
            return find_service(site, service_slug)
    return next(s for s in site.services if s.popular)


def _wrap_tables(html: str) -> str:
    """Bảng trong bài viết phải cuộn ngang được, không làm vỡ trang ở mobile."""
    return html.replace(
        "<table>", '<div class="table-scroll"><table>'
    ).replace("</table>", "</table></div>")


def _render_toc(outline: list[tuple[int, str, str]]) -> str:
    if len(outline) < 3:
        return ""
    items = "\n".join(
        f'            <li data-level="{level}">'
        f'<a href="#{anchor}">{text}</a></li>'
        for level, text, anchor in outline
    )
    return (
        '        <nav class="toc" aria-labelledby="toc-heading">\n'
        '          <h2 id="toc-heading">Nội dung bài viết</h2>\n'
        "          <ol>\n"
        f"{items}\n"
        "          </ol>\n"
        "        </nav>"
    )


def build_posts(site: SiteData) -> list[str]:
    from scripts.markdown import add_heading_anchors, md_to_html, strip_front_matter
    from scripts.sitedata import format_price

    written = []
    for index, post in enumerate(site.posts):
        with open(post.source, encoding="utf-8") as handle:
            raw = handle.read()
        body_html, outline = add_heading_anchors(
            md_to_html(strip_front_matter(raw))
        )
        body_html = _wrap_tables(body_html)

        related = _related_service(site, post.slug)
        others = [p for i, p in enumerate(site.posts) if i != index][:3]
        crumbs = [
            ("Trang chủ", "/"),
            ("Blog", "/blog.html"),
            (post.title, f"/blog/{post.slug}.html"),
        ]

        written.append(
            render_page(
                site,
                template="post.html",
                out=os.path.join("blog", f"{post.slug}.html"),
                page_id="blog",
                title=f"{post.title} | Blog {site.business.name}",
                description=post.desc,
                path=f"/blog/{post.slug}.html",
                jsonld=schema.to_jsonld(
                    schema.blog_posting(site, post), schema.breadcrumb_list(crumbs)
                ),
                main_context={
                    "post_title": post.title,
                    "date": post.date,
                    "iso_date": post.iso_date,
                    "category": post.category,
                    "img": post.img,
                    "toc": _render_toc(outline),
                    "body": body_html,
                    "related_name": related.name,
                    "related_price": format_price(related),
                    "related_slug": related.slug,
                    "related_specs": components.spec_line(related),
                    "related_posts": "\n".join(
                        components.post_card(p) for p in others
                    ),
                },
            )
        )
    return written


def build(root: str = ROOT) -> list[str]:
    site = load_site()
    return [
        build_home(site),
        build_services(site),
        build_areas(site),
        build_about(site),
        build_contact(site),
        build_blog_index(site),
        *build_posts(site),
    ]


def main() -> None:
    for path in build():
        print("wrote", os.path.relpath(path, ROOT))


if __name__ == "__main__":
    main()
