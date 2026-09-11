"""Sinh chuỗi HTML cho các component tái dùng.

Mọi hàm nhận dataclass từ scripts.sitedata và trả về chuỗi HTML.
Không hàm nào được sinh thuộc tính style= (ràng buộc toàn cục #1).
"""
from __future__ import annotations

from scripts.sitedata import Faq, Post, Service, SiteData, format_price
from scripts.template import escape

# ---------------------------------------------------------------- icons

_ICON_PATHS = {
    # Ống nghe điện thoại
    "phone": '<path d="M18.5 14.1v2.5a1.7 1.7 0 0 1-1.8 1.7 16.5 16.5 0 0 1-7.2-2.6 16.3 16.3 0 0 1-5-5A16.5 16.5 0 0 1 1.9 3.5 1.7 1.7 0 0 1 3.6 1.7h2.5a1.7 1.7 0 0 1 1.7 1.4c.1.8.3 1.6.6 2.3a1.7 1.7 0 0 1-.4 1.8L7 8.3a13.3 13.3 0 0 0 5 5l1.1-1.1a1.7 1.7 0 0 1 1.8-.4c.7.3 1.5.5 2.3.6a1.7 1.7 0 0 1 1.4 1.7z"/>',
    # Bong bóng chat — đại diện kênh nhắn tin
    "zalo": '<path d="M17.5 12.5a1.7 1.7 0 0 1-1.7 1.7H6.7L3.3 17.5V4.2a1.7 1.7 0 0 1 1.7-1.7h10.8a1.7 1.7 0 0 1 1.7 1.7z"/><path d="M7.1 6.7h5.8L7.1 11.3h5.8"/>',
    # Tờ báo giá
    "quote": '<path d="M11.7 1.7H5a1.7 1.7 0 0 0-1.7 1.7v13.3A1.7 1.7 0 0 0 5 18.3h10a1.7 1.7 0 0 0 1.7-1.7V6.7z"/><path d="M11.7 1.7v5h5"/><path d="M6.7 10.8h6.6M6.7 14.2h6.6"/>',
}


def icon(name: str) -> str:
    """SVG inline 20×20, nét 1.5px, màu thừa hưởng từ CSS qua currentColor."""
    if name not in _ICON_PATHS:
        raise KeyError(f"Không có icon {name!r}; hiện có: {sorted(_ICON_PATHS)}")
    return (
        '<svg class="icon" viewBox="0 0 20 20" width="20" height="20" '
        'fill="none" stroke="currentColor" stroke-width="1.5" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        f"{_ICON_PATHS[name]}</svg>"
    )


# ---------------------------------------------------------------- spec-line


def spec_line(service: Service) -> str:
    """Chữ ký thị giác của hệ thống — spec §3.6 yếu tố 1."""
    rows = "\n".join(
        f'        <div class="spec-line__row">'
        f"<dt>{escape(spec.label)}</dt><dd>{escape(spec.value)}</dd></div>"
        for spec in service.specs
    )
    return f'      <dl class="spec-line">\n{rows}\n      </dl>'


# ---------------------------------------------------------------- cards


CARD_SIZES = "(min-width: 1024px) 380px, (min-width: 640px) 45vw, 92vw"
COVER_SIZES = "(min-width: 1024px) 700px, 92vw"
PROJECT_SIZES = "(min-width: 640px) 50vw, 92vw"


def photo(stem: str, alt: str, *, folder: str = "", sizes: str,
          lazy: bool = True, classes: str = "", decorative: bool = False) -> str:
    """Ảnh thật kèm srcset 480w/960w và width/height chống CLS.

    `stem` là tên file không đuôi; scripts/optimize_images.py sinh ra
    <stem>-480.webp và <stem>-960.webp từ ảnh gốc trong _src/site/.
    """
    from scripts import images

    base = f"/assets/images/{folder}/{stem}" if folder else f"/assets/images/{stem}"
    variants = images.find_variants(base)
    return images.image_tag(
        variants[0].path,
        alt,
        sizes=sizes,
        lazy=lazy,
        variants=variants,
        classes=classes,
        decorative=decorative,
    )


def service_card(service: Service, *, svg_inline: str | None = None) -> str:
    """Card dịch vụ. Dùng ảnh sản phẩm thật; `svg_inline` chỉ là phương án
    dự phòng khi một dịch vụ chưa có ảnh."""
    badge = (
        '        <span class="badge badge--popular">Phổ biến nhất</span>\n'
        if service.popular
        else ""
    )
    figure = (
        photo(service.photo, service.photo_alt, folder="services", sizes=CARD_SIZES)
        if service.photo
        else (svg_inline or "")
    )
    return (
        f'    <article class="card card--service" id="{escape(service.slug)}">\n'
        f'      <div class="card__figure card__figure--photo">{figure}</div>\n'
        f'      <div class="card__body">\n'
        f"{badge}"
        f"        <h3>{escape(service.name)}</h3>\n"
        f'        <p class="card__price">{escape(format_price(service))}</p>\n'
        f'        <p class="card__blurb">{escape(service.blurb)}</p>\n'
        f"{spec_line(service)}\n"
        f'        <a class="btn btn--primary" '
        f'href="/lien-he.html?dich-vu={escape(service.slug)}">'
        f"Nhận báo giá</a>\n"
        f"      </div>\n"
        f"    </article>"
    )


def post_card(post: Post) -> str:
    """Card bài viết.

    Ảnh là thumbnail thật của chính bài đó. Thumbnail để alt rỗng vì tiêu đề
    nằm ngay trong cùng thẻ <a> — nếu đặt alt trùng tiêu đề thì trình đọc màn
    hình sẽ đọc hai lần.
    """
    thumb = photo(
        post.img, "", folder="blog", sizes=CARD_SIZES, decorative=True
    )
    return (
        f'    <a class="card card--post" href="/blog/{escape(post.slug)}.html" '
        f'data-category="{escape(post.category)}">\n'
        f'      <div class="card__thumb">{thumb}</div>\n'
        f'      <div class="card__body">\n'
        f'        <p class="card__meta">'
        f'<span class="badge">{escape(post.category)}</span>'
        f'<time datetime="{escape(post.iso_date)}">{escape(post.date)}</time></p>\n'
        f"        <h3>{escape(post.title)}</h3>\n"
        f'        <span class="card__more">Đọc tiếp</span>\n'
        f"      </div>\n"
        f"    </a>"
    )


# ---------------------------------------------------------------- rail, stepper


def numeric_rail(facts: tuple[tuple[str, str], ...]) -> str:
    """Spec §3.6 yếu tố 3 — dải số liệu trên nền thép."""
    items = "\n".join(
        f'      <li class="rail__item">'
        f'<span class="rail__value">{escape(value)}</span>'
        f'<span class="rail__label">{escape(label)}</span></li>'
        for value, label in facts
    )
    return f'    <ul class="rail">\n{items}\n    </ul>'


def stepper(steps: list[tuple[str, str]]) -> str:
    items = "\n".join(
        f'      <li class="stepper__step">\n'
        f'        <span class="stepper__num" aria-hidden="true">{index}</span>\n'
        f"        <h3>{escape(title)}</h3>\n"
        f"        <p>{escape(body)}</p>\n"
        f"      </li>"
        for index, (title, body) in enumerate(steps, start=1)
    )
    return f'    <ol class="stepper">\n{items}\n    </ol>'


# ---------------------------------------------------------------- faq


def faq_list(faqs, *, id_prefix: str = "faq") -> str:
    items = []
    for index, faq in enumerate(faqs, start=1):
        btn_id = f"{id_prefix}-{index}-btn"
        panel_id = f"{id_prefix}-{index}-panel"
        items.append(
            f'      <div class="faq__item">\n'
            f'        <h3 class="faq__heading">\n'
            f'          <button class="faq__question" type="button" id="{btn_id}" '
            f'aria-expanded="false" aria-controls="{panel_id}">\n'
            f"            <span>{escape(faq.question)}</span>\n"
            f'            <span class="faq__mark" aria-hidden="true"></span>\n'
            f"          </button>\n"
            f"        </h3>\n"
            f'        <div class="faq__panel" id="{panel_id}" role="region" '
            f'aria-labelledby="{btn_id}" hidden>\n'
            f"          <p>{escape(faq.answer)}</p>\n"
            f"        </div>\n"
            f"      </div>"
        )
    return '    <div class="faq">\n' + "\n".join(items) + "\n    </div>"


# ---------------------------------------------------------------- form, table


def service_options(site: SiteData) -> str:
    """Sửa lỗi C4 — dropdown phải khớp đúng 8 dịch vụ đang bán."""
    options = ['        <option value="">Chọn dịch vụ cần báo giá</option>']
    options += [
        f'        <option value="{escape(s.slug)}">{escape(s.name)}</option>'
        for s in site.services
    ]
    return "\n".join(options)


def comparison_table(site: SiteData) -> str:
    """So sánh ba loại giàn phơi. Chỉ dùng dữ liệu có thật trong site.json."""
    racks = [s for s in site.services if s.group == "Giàn phơi"]
    rows = []
    for service in racks:
        warranty = next(
            (sp.value for sp in service.specs if sp.label == "Bảo hành"), "Liên hệ"
        )
        features = " · ".join(
            f"{sp.label}: {sp.value}" for sp in service.specs if sp.label != "Bảo hành"
        )
        rows.append(
            f"        <tr>\n"
            f'          <th scope="row">{escape(service.name)}</th>\n'
            f"          <td>{escape(format_price(service))}</td>\n"
            f"          <td>{escape(features)}</td>\n"
            f"          <td>{escape(warranty)}</td>\n"
            f"        </tr>"
        )
    body = "\n".join(rows)
    return (
        '    <div class="table-scroll">\n'
        '      <table class="compare">\n'
        "        <caption>So sánh ba loại giàn phơi đang lắp đặt</caption>\n"
        "        <thead>\n"
        "          <tr>\n"
        '            <th scope="col">Loại giàn phơi</th>\n'
        '            <th scope="col">Giá tham khảo</th>\n'
        '            <th scope="col">Đặc điểm chính</th>\n'
        '            <th scope="col">Bảo hành</th>\n'
        "          </tr>\n"
        "        </thead>\n"
        "        <tbody>\n"
        f"{body}\n"
        "        </tbody>\n"
        "      </table>\n"
        "    </div>"
    )


def area_list(areas: tuple[str, ...]) -> str:
    items = "\n".join(
        f'      <li class="area-list__item">{escape(area)}</li>' for area in areas
    )
    return f'    <ul class="area-list">\n{items}\n    </ul>'


# ---------------------------------------------------------------- navigation

NAV_ITEMS = (
    ("home", "Trang chủ", "/index.html"),
    ("about", "Giới thiệu", "/gioi-thieu.html"),
    ("services", "Dịch vụ", "/dich-vu.html"),
    ("areas", "Khu vực", "/khu-vuc.html"),
    ("blog", "Blog", "/blog.html"),
    ("contact", "Liên hệ", "/lien-he.html"),
)


def nav_list(current: str) -> str:
    items = []
    for page_id, label, href in NAV_ITEMS:
        marker = ' aria-current="page"' if page_id == current else ""
        items.append(
            f'        <li><a class="nav__link" href="{href}"{marker}>'
            f"{escape(label)}</a></li>"
        )
    body = "\n".join(items)
    return f'      <ul class="nav__list" id="nav-list">\n{body}\n      </ul>'


def footer_services(site: SiteData) -> str:
    return "\n".join(
        f'          <li><a href="/dich-vu.html#{escape(s.slug)}">'
        f"{escape(s.name)}</a></li>"
        for s in site.services
    )


# ---------------------------------------------------------------- use cases


def usecase_card(title: str, body: str, service: Service, *, svg_inline: str) -> str:
    """Tầng quyết định trên trang chủ — sửa lỗi C6."""
    return (
        f'    <article class="card card--usecase">\n'
        f'      <div class="card__figure">{svg_inline}</div>\n'
        f'      <div class="card__body">\n'
        f"        <h3>{escape(title)}</h3>\n"
        f"        <p>{escape(body)}</p>\n"
        f'        <p class="card__price">{escape(format_price(service))}</p>\n'
        f'        <a class="btn btn--ghost" href="/dich-vu.html#{escape(service.slug)}">'
        f"Xem {escape(service.name)}</a>\n"
        f"      </div>\n"
        f"    </article>"
    )


def project_card(project) -> str:
    """Công trình thật cho trang Khu vực. Không phải link, không gắn tel:
    (lỗi C5 của bản cũ) — đây là ảnh tư liệu, không phải nút hành động."""
    return (
        f'      <figure class="card card--project">\n'
        f"        "
        + photo(project.img, project.alt, folder="projects", sizes=PROJECT_SIZES)
        + "\n"
        f'        <figcaption class="card__body">\n'
        f'          <span class="badge">{escape(project.location)}</span>\n'
        f"          <p>{escape(project.work)}</p>\n"
        f"        </figcaption>\n"
        f"      </figure>"
    )


def project_grid(projects) -> str:
    if not projects:
        return ('    <div class="project-grid" '
                'data-empty="Chưa có ảnh công trình thật để đăng."></div>')
    body = "\n".join(project_card(p) for p in projects)
    return f'    <div class="project-grid">\n{body}\n    </div>'
