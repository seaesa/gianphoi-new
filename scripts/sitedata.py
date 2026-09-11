"""Đọc và kiểm tra site.json — nguồn chân lý duy nhất của site."""
from __future__ import annotations

import json
import os
from dataclasses import dataclass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GROUP_ORDER = ("Giàn phơi", "An toàn ban công", "Che chắn")


class SiteDataError(ValueError):
    """site.json thiếu trường bắt buộc hoặc sai định dạng."""


@dataclass(frozen=True)
class Spec:
    label: str
    value: str


@dataclass(frozen=True)
class Service:
    slug: str
    name: str
    group: str
    price_from: int
    price_to: int
    unit: str
    blurb: str
    specs: tuple[Spec, ...]
    svg: str
    popular: bool
    photo: str
    photo_alt: str
    intro: str

    @property
    def url(self) -> str:
        """Trang riêng của dịch vụ, đặt ở thư mục gốc."""
        return f"/{self.slug}.html"


@dataclass(frozen=True)
class Project:
    """Công trình thật. Chỉ ghi thông tin suy ra được từ chính tấm ảnh."""

    img: str
    location: str
    work: str
    duration: str
    alt: str


@dataclass(frozen=True)
class Faq:
    question: str
    answer: str
    contact_page: bool


@dataclass(frozen=True)
class Post:
    slug: str
    title: str
    date: str
    iso_date: str
    img: str
    img_alt: str
    desc: str
    category: str
    source: str
    url_slug: str

    @property
    def url(self) -> str:
        """Giữ nguyên URL như site đang chạy để không mất thứ hạng tìm kiếm."""
        return f"/{self.url_slug}.html"


@dataclass(frozen=True)
class Business:
    name: str
    tagline: str
    phone: str
    phone_display: str
    zalo_url: str
    email: str
    street: str
    city: str
    hours: str
    maps_query: str


@dataclass(frozen=True)
class SiteData:
    business: Business
    services: tuple[Service, ...]
    faqs: tuple[Faq, ...]
    areas: tuple[str, ...]
    posts: tuple[Post, ...]
    facts: tuple[tuple[str, str], ...]
    projects: tuple[Project, ...]


def _require(mapping: dict, key: str, where: str):
    if key not in mapping:
        raise SiteDataError(f"{where}: thiếu trường bắt buộc {key!r}")
    return mapping[key]


def load_site(path: str = "site.json") -> SiteData:
    full = path if os.path.isabs(path) else os.path.join(ROOT, path)
    try:
        with open(full, encoding="utf-8") as handle:
            data = json.load(handle)
    except FileNotFoundError as exc:
        raise SiteDataError(f"Không tìm thấy {full}") from exc
    except json.JSONDecodeError as exc:
        raise SiteDataError(f"{full} không phải JSON hợp lệ: {exc}") from exc

    try:
        business = Business(**_require(data, "business", full))
    except TypeError as exc:
        raise SiteDataError(f"{full}: khối 'business' sai trường — {exc}") from exc

    services = []
    for raw in _require(data, "services", full):
        slug = raw.get("slug", "<không rõ>")
        try:
            specs = tuple(Spec(**s) for s in _require(raw, "specs", f"service {slug}"))
            services.append(Service(**{**raw, "specs": specs}))
        except TypeError as exc:
            raise SiteDataError(f"service {slug!r} sai trường — {exc}") from exc

    for service in services:
        if service.group not in GROUP_ORDER:
            raise SiteDataError(
                f"service {service.slug!r} thuộc nhóm lạ {service.group!r}; "
                f"chỉ chấp nhận {GROUP_ORDER}"
            )

    try:
        faqs = tuple(Faq(**f) for f in _require(data, "faqs", full))
        posts = tuple(
            Post(**{**p, "source": os.path.join(ROOT, p["source"])})
            for p in _require(data, "posts", full)
        )
    except TypeError as exc:
        raise SiteDataError(f"{full}: khối 'faqs' hoặc 'posts' sai trường — {exc}") from exc

    try:
        projects = tuple(Project(**p) for p in _require(data, "projects", full))
    except TypeError as exc:
        raise SiteDataError(f"{full}: khối 'projects' sai trường — {exc}") from exc

    facts = tuple((str(a), str(b)) for a, b in _require(data, "facts", full))
    areas = tuple(_require(data, "areas", full))

    return SiteData(business, tuple(services), faqs, areas, posts, facts, projects)


def format_price(service: Service) -> str:
    def vnd(amount: int) -> str:
        return f"{amount:,}".replace(",", ".")

    return f"{vnd(service.price_from)} – {vnd(service.price_to)}đ/{service.unit}"


def service_groups(site: SiteData) -> list[tuple[str, list[Service]]]:
    return [
        (group, [s for s in site.services if s.group == group])
        for group in GROUP_ORDER
    ]


def find_service(site: SiteData, slug: str) -> Service:
    for service in site.services:
        if service.slug == slug:
            return service
    raise SiteDataError(f"Không có dịch vụ {slug!r} trong site.json")
