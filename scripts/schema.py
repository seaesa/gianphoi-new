"""Sinh JSON-LD structured data cho SEO local.

Site này sống bằng tìm kiếm local ("giàn phơi quận 1", "Dĩ An"...), nên
LocalBusiness + Service + FAQPage là phần bắt buộc, không phải tùy chọn.
"""
from __future__ import annotations

import json
import os

from scripts.sitedata import Faq, Post, Service, SiteData, format_price

BASE_URL = os.environ.get("SITE_BASE_URL", "https://gianphoithongminh.vn").rstrip("/")


def _abs(path: str) -> str:
    return f"{BASE_URL}/{path.lstrip('/')}"


def _publisher(site: SiteData) -> dict:
    return {
        "@type": "Organization",
        "name": site.business.name,
        "logo": {"@type": "ImageObject", "url": _abs("/assets/images/logo.png")},
    }


def local_business(site: SiteData) -> dict:
    business = site.business
    return {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": business.name,
        "description": business.tagline,
        "url": _abs("/"),
        "telephone": business.phone,
        "email": business.email,
        "image": _abs("/assets/images/logo.png"),
        "logo": _abs("/assets/images/logo.png"),
        "address": {
            "@type": "PostalAddress",
            "streetAddress": business.street,
            "addressLocality": business.city,
            "addressCountry": "VN",
        },
        "openingHours": business.hours,
        "areaServed": [{"@type": "Place", "name": area} for area in site.areas],
    }


def service_schema(site: SiteData, service: Service) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": service.name,
        "description": service.blurb,
        "serviceType": service.group,
        "url": _abs(f"/dich-vu.html#{service.slug}"),
        "provider": {
            "@type": "LocalBusiness",
            "name": site.business.name,
            "telephone": site.business.phone,
        },
        "areaServed": [{"@type": "Place", "name": area} for area in site.areas],
        "offers": {
            "@type": "Offer",
            "priceCurrency": "VND",
            "priceRange": format_price(service),
            "availability": "https://schema.org/InStock",
        },
    }


def faq_page(faqs: tuple[Faq, ...]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": faq.question,
                "acceptedAnswer": {"@type": "Answer", "text": faq.answer},
            }
            for faq in faqs
        ],
    }


def breadcrumb_list(crumbs: list[tuple[str, str]]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": position,
                "name": name,
                "item": _abs(path),
            }
            for position, (name, path) in enumerate(crumbs, start=1)
        ],
    }


def blog_posting(site: SiteData, post: Post) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": post.title,
        "description": post.desc,
        "image": _abs(f"/assets/images/blog/{post.img}"),
        "datePublished": post.iso_date,
        "dateModified": post.iso_date,
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": _abs(f"/blog/{post.slug}.html"),
        },
        "author": _publisher(site),
        "publisher": _publisher(site),
    }


def to_jsonld(*objects: dict) -> str:
    """Bọc trong thẻ script. Thoát < > để dữ liệu không phá được thẻ."""
    payload = objects[0] if len(objects) == 1 else list(objects)
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    text = text.replace("<", "\\u003c").replace(">", "\\u003e")
    return f'<script type="application/ld+json">\n{text}\n</script>'
