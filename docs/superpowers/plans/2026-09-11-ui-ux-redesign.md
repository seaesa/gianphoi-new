# Thiết kế lại UI/UX "Thép & Nắng" — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Thay toàn bộ UI/UX của site giàn phơi thông minh bằng design system "Thép & Nắng" — catalogue kỹ thuật dựa trên số liệu và hình vẽ nét — đồng thời sinh HTML tĩnh có sẵn header/footer/JSON-LD từ một nguồn dữ liệu duy nhất.

**Architecture:** Một file dữ liệu `site.json` là nguồn chân lý duy nhất. Các module Python thuần trong `scripts/` đọc dữ liệu đó, sinh chuỗi HTML cho từng component, rồi ghép vào template trong `templates/` để xuất ra HTML tĩnh ở thư mục gốc. CSS gom về một file dùng `@layer`. Bộ test `unittest` chạy trên output đã build, biến 11 tiêu chí nghiệm thu của spec thành assertion tự động.

**Tech Stack:** Python 3.13 (stdlib + Pillow 12.3), `unittest` (stdlib — **không dùng pytest**, máy không cài), HTML/CSS/JS thuần không framework, Google Fonts (Be Vietnam Pro + Inter).

**Spec:** `docs/superpowers/specs/2026-09-11-ui-ux-redesign-design.md`

---

## Global Constraints

Mọi task đều phải tuân thủ, không cần nhắc lại trong từng task:

**Token màu** (spec §3.3) — giá trị chính xác, không được đổi:
```
--ink: #0F1C26        --ink-soft: #33506A     --muted: #5A6873
--steel: #1E3446      --steel-deep: #162836
--paper: #FBFAF8      --surface: #FFFFFF      --hairline: #E3E0DA
--amber: #B4530A      --amber-bright: #E07A1F
--amber-tint: #FDF1E3 --amber-ink: #8A3D06
```

**Token hình khối** (spec §3.5):
```
--space-1..10: 4 8 12 16 24 32 48 64 96 128 (px)
--r-sm: 6px   --r: 10px   --r-pill: 999px
--container: 1200px   --gutter: 24px
```
Chỉ tồn tại ba token bo góc. `--radius-sm`, `--radius-md`, `--radius-lg`, `--radius-pill` cũ phải bị xóa hoàn toàn.

**Chữ** (spec §3.4): display = `Be Vietnam Pro` (600/700/800), body = `Inter` (400/500/600). `line-height` 1.15 cho display, 1.65 cho thân bài. Bảng giá và bảng thông số dùng `font-variant-numeric: tabular-nums`.

**Chuyển động** (spec §3.7): chỉ hai thời lượng 150ms và 250ms, easing `cubic-bezier(0.2, 0, 0, 1)`, chỉ animate `transform` và `opacity`, toàn bộ nằm trong `@media (prefers-reduced-motion: no-preference)`.

**Quy tắc tuyệt đối** (spec §3.2, §7):
1. Không có thuộc tính `style=` trong bất kỳ file HTML nào.
2. Không có viền `3px` accent nào trong CSS.
3. Hổ phách chỉ dùng cho hành động và số liệu, không làm trang trí.
4. `--amber-bright` chỉ được dùng cho chữ `font-size` ≥ 24px và `font-weight` ≥ 700 (tương phản 4.27:1 trên `--steel`).
5. Mọi cặp màu chữ/nền khác phải đạt ≥ 4.5:1.
6. Mọi `<img>` phải có `width` và `height` tường minh.
7. Không có `tel:` trên phần tử không phải hành động gọi điện.
8. Mọi số liệu phải lấy từ `site.json` — không hardcode, không bịa.

**Lệnh test** (dùng ở mọi task):
```bash
python -m unittest discover -s tests -t . -v
```
Chạy một test cụ thể:
```bash
python -m unittest tests.test_color.TestContrastRatio.test_white_on_amber -v
```

**Commit**: mỗi task kết thúc bằng đúng một commit. Message tiếng Việt, prefix `feat:` / `test:` / `refactor:` / `style:`.

---

## File Structure

**Tạo mới:**

| File | Trách nhiệm |
|---|---|
| `site.json` | Nguồn chân lý duy nhất: doanh nghiệp, 8 dịch vụ + thông số, 10 FAQ, khu vực phục vụ, 12 bài blog |
| `scripts/color.py` | Tính tương phản WCAG, đọc token từ CSS |
| `scripts/sitedata.py` | Dataclass + loader + validate cho `site.json` |
| `scripts/markdown.py` | `md_to_html` (tách từ `build_blog.py`) + trích heading cho mục lục |
| `scripts/template.py` | Render engine tối giản: `{{ var }}`, `{{{ raw }}}`, `{{> partial }}` |
| `scripts/components.py` | Sinh chuỗi HTML cho từng component (spec-line, card, rail, stepper, faq...) |
| `scripts/schema.py` | Sinh JSON-LD |
| `scripts/images.py` | WebP + srcset + đo kích thước (Pillow) |
| `scripts/build.py` | Entrypoint: render toàn bộ trang |
| `templates/*.html` | Template từng trang + partial dùng chung |
| `assets/svg/*.svg` | 8 hình vẽ nét sản phẩm |
| `tests/*.py` | Bộ test `unittest` |

**Sửa:**

| File | Thay đổi |
|---|---|
| `assets/css/main.css` | Viết lại hoàn toàn theo `@layer` |
| `assets/js/main.js` | Viết lại hoàn toàn |
| `index.html`, `gioi-thieu.html`, `dich-vu.html`, `blog.html`, `lien-he.html`, `blog/*.html` | Trở thành output sinh ra, không sửa tay |

**Xóa:**

| File | Lý do |
|---|---|
| `assets/js/include.js` | Header/footer giờ inline tại build time |
| `partials/header.html`, `partials/footer.html` | Thay bằng `templates/_header.html`, `_footer.html` |
| `scripts/build_blog.py` | Thay bằng `scripts/build.py` |
| `du-an.html` | Đổi thành `khu-vuc.html` |

---

### Task 1: Module tính tương phản màu

Nền móng cho mọi quyết định màu. Test này sẽ được tái dùng ở Task 6 để kiểm tra CSS thật.

**Files:**
- Create: `scripts/color.py`
- Create: `tests/__init__.py` (file rỗng)
- Create: `tests/test_color.py`

**Interfaces:**
- Consumes: không
- Produces:
  - `relative_luminance(hex_color: str) -> float`
  - `contrast_ratio(fg: str, bg: str) -> float`
  - `passes_aa(fg: str, bg: str, large: bool = False) -> bool`
  - `parse_css_tokens(css_text: str) -> dict[str, str]` — trích mọi `--name: #hex;` trong khối `:root`

- [ ] **Step 1: Tạo package test rỗng**

```bash
mkdir -p tests scripts
touch tests/__init__.py
```

- [ ] **Step 2: Viết test thất bại**

Tạo `tests/test_color.py`:

```python
import unittest

from scripts.color import (
    contrast_ratio,
    parse_css_tokens,
    passes_aa,
    relative_luminance,
)


class TestRelativeLuminance(unittest.TestCase):
    def test_white_is_one(self):
        self.assertAlmostEqual(relative_luminance("#FFFFFF"), 1.0, places=4)

    def test_black_is_zero(self):
        self.assertAlmostEqual(relative_luminance("#000000"), 0.0, places=4)

    def test_accepts_lowercase_and_no_hash(self):
        self.assertAlmostEqual(
            relative_luminance("ffffff"), relative_luminance("#FFFFFF"), places=6
        )


class TestContrastRatio(unittest.TestCase):
    def test_black_on_white_is_21(self):
        self.assertAlmostEqual(contrast_ratio("#000000", "#FFFFFF"), 21.0, places=2)

    def test_is_symmetric(self):
        self.assertAlmostEqual(
            contrast_ratio("#0F1C26", "#FBFAF8"),
            contrast_ratio("#FBFAF8", "#0F1C26"),
            places=6,
        )

    def test_white_on_amber_passes_aa(self):
        # Token --amber #B4530A, nền nút CTA chính. Spec §3.3 ghi 5.02:1.
        self.assertAlmostEqual(contrast_ratio("#FFFFFF", "#B4530A"), 5.02, places=2)

    def test_old_accent_failed_aa(self):
        # Màu cũ #C5652B chỉ đạt 3.98:1 — đây là lý do phải đổi.
        self.assertLess(contrast_ratio("#FFFFFF", "#C5652B"), 4.5)


class TestPassesAA(unittest.TestCase):
    def test_normal_text_threshold(self):
        self.assertTrue(passes_aa("#0F1C26", "#FBFAF8"))
        self.assertFalse(passes_aa("#E07A1F", "#1E3446"))

    def test_large_text_threshold(self):
        # --amber-bright chỉ hợp lệ ở chữ lớn: 4.27:1 >= 3.0
        self.assertTrue(passes_aa("#E07A1F", "#1E3446", large=True))


class TestParseCssTokens(unittest.TestCase):
    def test_extracts_hex_tokens_from_root(self):
        css = """
        @layer tokens {
          :root {
            --ink: #0F1C26;
            --paper: #FBFAF8;
            --r: 10px;
          }
        }
        """
        tokens = parse_css_tokens(css)
        self.assertEqual(tokens["--ink"], "#0F1C26")
        self.assertEqual(tokens["--paper"], "#FBFAF8")

    def test_ignores_non_hex_values(self):
        css = ":root { --r: 10px; --container: 1200px; }"
        self.assertEqual(parse_css_tokens(css), {})
```

- [ ] **Step 3: Chạy test, xác nhận thất bại**

Run: `python -m unittest tests.test_color -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'scripts.color'`

- [ ] **Step 4: Viết implementation tối thiểu**

Tạo `scripts/__init__.py` rỗng, rồi `scripts/color.py`:

```python
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
```

- [ ] **Step 5: Chạy test, xác nhận pass**

Run: `python -m unittest tests.test_color -v`
Expected: PASS, 9 tests

- [ ] **Step 6: Commit**

```bash
git add scripts/__init__.py scripts/color.py tests/__init__.py tests/test_color.py
git commit -m "feat: module tính tương phản màu WCAG + parse token CSS"
```

---

### Task 2: Nguồn dữ liệu `site.json` và loader

Đây là task quan trọng nhất về mặt kiến trúc: sau task này, giá dịch vụ, FAQ và thông tin liên hệ chỉ tồn tại ở **một chỗ**. Nó sửa luôn lỗi C4 (dropdown form lệch 8 dịch vụ) ở gốc rễ.

**Files:**
- Create: `site.json`
- Create: `scripts/sitedata.py`
- Create: `tests/test_sitedata.py`

**Interfaces:**
- Consumes: không
- Produces:
  - `class SiteDataError(ValueError)`
  - `@dataclass(frozen=True) Spec(label: str, value: str)`
  - `@dataclass(frozen=True) Service(slug, name, group, price_from: int, price_to: int, unit, blurb, specs: tuple[Spec, ...], svg: str, popular: bool)`
  - `@dataclass(frozen=True) Faq(question: str, answer: str, contact_page: bool)`
  - `@dataclass(frozen=True) Post(slug, title, date, iso_date, img, desc, category, source)`
  - `@dataclass(frozen=True) Business(name, tagline, phone, phone_display, zalo_url, email, street, city, hours, maps_query)`
  - `@dataclass(frozen=True) SiteData(business: Business, services: tuple[Service, ...], faqs: tuple[Faq, ...], areas: tuple[str, ...], posts: tuple[Post, ...], facts: tuple[tuple[str, str], ...])`
  - `load_site(path: str = "site.json") -> SiteData`
  - `format_price(service: Service) -> str` → `"3.200.000 – 4.500.000đ/bộ"`
  - `service_groups(site: SiteData) -> list[tuple[str, list[Service]]]` — giữ nguyên thứ tự xuất hiện trong `site.json`
  - `find_service(site: SiteData, slug: str) -> Service`

Ba nhóm dịch vụ theo spec §4.2, dùng đúng ba chuỗi này làm `group`: `"Giàn phơi"`, `"An toàn ban công"`, `"Che chắn"`.

- [ ] **Step 1: Viết test thất bại**

Tạo `tests/test_sitedata.py`:

```python
import unittest

from scripts.sitedata import (
    SiteDataError,
    find_service,
    format_price,
    load_site,
    service_groups,
)

SITE = load_site()


class TestBusiness(unittest.TestCase):
    def test_phone_is_e164(self):
        self.assertTrue(SITE.business.phone.startswith("+84"))
        self.assertTrue(SITE.business.phone[1:].isdigit())

    def test_zalo_url_present(self):
        self.assertIn("zalo.me", SITE.business.zalo_url)

    def test_email_present(self):
        self.assertIn("@", SITE.business.email)


class TestServices(unittest.TestCase):
    def test_exactly_eight_services(self):
        self.assertEqual(len(SITE.services), 8)

    def test_slugs_are_unique(self):
        slugs = [s.slug for s in SITE.services]
        self.assertEqual(len(slugs), len(set(slugs)))

    def test_every_service_has_three_specs(self):
        for service in SITE.services:
            with self.subTest(service=service.slug):
                self.assertEqual(len(service.specs), 3)

    def test_every_service_has_warranty_spec(self):
        for service in SITE.services:
            with self.subTest(service=service.slug):
                labels = [spec.label for spec in service.specs]
                self.assertIn("Bảo hành", labels)

    def test_price_range_is_ordered(self):
        for service in SITE.services:
            with self.subTest(service=service.slug):
                self.assertLess(service.price_from, service.price_to)

    def test_exactly_one_popular_service(self):
        self.assertEqual(sum(1 for s in SITE.services if s.popular), 1)

    def test_groups_are_the_three_from_spec(self):
        groups = [name for name, _ in service_groups(SITE)]
        self.assertEqual(groups, ["Giàn phơi", "An toàn ban công", "Che chắn"])

    def test_every_service_references_an_svg(self):
        for service in SITE.services:
            with self.subTest(service=service.slug):
                self.assertTrue(service.svg.endswith(".svg"))


class TestFormatPrice(unittest.TestCase):
    def test_formats_with_dot_separators_and_en_dash(self):
        service = find_service(SITE, "gian-phoi-dieu-khien")
        self.assertEqual(format_price(service), "3.200.000 – 4.500.000đ/bộ")

    def test_per_square_metre_unit(self):
        service = find_service(SITE, "luoi-cap-ban-cong")
        self.assertEqual(format_price(service), "180.000 – 250.000đ/m²")


class TestFaqs(unittest.TestCase):
    def test_ten_faqs(self):
        self.assertEqual(len(SITE.faqs), 10)

    def test_four_marked_for_contact_page(self):
        # Spec §4.2: trang Liên hệ giữ 4 câu về đặt lịch và báo giá.
        self.assertEqual(sum(1 for f in SITE.faqs if f.contact_page), 4)

    def test_questions_carry_no_manual_numbering(self):
        # Bản cũ nhúng "1. ", "2. " vào câu hỏi — số thứ tự thuộc về CSS.
        for faq in SITE.faqs:
            with self.subTest(question=faq.question):
                self.assertFalse(faq.question[0].isdigit())


class TestPosts(unittest.TestCase):
    def test_twelve_posts(self):
        self.assertEqual(len(SITE.posts), 12)

    def test_iso_dates_are_sortable(self):
        for post in SITE.posts:
            with self.subTest(post=post.slug):
                self.assertRegex(post.iso_date, r"^\d{4}-\d{2}-\d{2}$")

    def test_source_files_exist(self):
        import os

        for post in SITE.posts:
            with self.subTest(post=post.slug):
                self.assertTrue(os.path.exists(post.source), post.source)

    def test_every_post_has_a_category(self):
        allowed = {"Khu vực", "Kiến thức", "So sánh"}
        for post in SITE.posts:
            with self.subTest(post=post.slug):
                self.assertIn(post.category, allowed)


class TestFacts(unittest.TestCase):
    def test_five_facts_for_numeric_rail(self):
        # Spec §3.6: numeric rail có đúng 5 số liệu.
        self.assertEqual(len(SITE.facts), 5)


class TestValidation(unittest.TestCase):
    def test_missing_file_raises(self):
        with self.assertRaises(SiteDataError):
            load_site("khong-ton-tai.json")

    def test_malformed_service_raises(self):
        import json
        import os
        import tempfile

        bad = {"business": {}, "services": [{"slug": "x"}], "faqs": [], "areas": [], "posts": [], "facts": []}
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "bad.json")
            with open(path, "w", encoding="utf-8") as handle:
                json.dump(bad, handle)
            with self.assertRaises(SiteDataError):
                load_site(path)
```

- [ ] **Step 2: Chạy test, xác nhận thất bại**

Run: `python -m unittest tests.test_sitedata -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'scripts.sitedata'`

- [ ] **Step 3: Viết `site.json`**

Lấy dữ liệu từ các file hiện có — **không bịa số mới**:
- 8 dịch vụ, tên/giá/mô tả: `dich-vu.html` (8 khối `<article class="card service-card">`)
- 10 FAQ: `lien-he.html` (10 khối `.faq-item`) — **bỏ tiền tố số "1. ", "2. "** trong câu hỏi
- Thông tin liên hệ: `partials/footer.html`
- Khu vực: `du-an.html` + `index.html` ("Bình Dương, Thủ Dầu Một, Thủ Đức, Quận 7, Quận 1")
- 12 bài blog: mảng `POSTS` trong `scripts/build_blog.py`
- Số liệu `facts`: `gioi-thieu.html` `.stat-strip` (10+ năm, 8 dịch vụ, 1000+ công trình, 24/7) + tải trọng 70kg từ mô tả "Giàn Phơi Treo Trần"

Thông số kỹ thuật (`specs`) cho từng dịch vụ lấy từ chính câu mô tả đang có. Ví dụ "Hòa Phát chính hãng, inox 304, tải trọng tới 70kg" → ba spec. Dịch vụ nào mô tả không đủ ba thông số thì dùng nhãn phù hợp có sẵn trong câu (Chất liệu / Ứng dụng / Bảo hành), **không tự nghĩ ra con số**.

Cấu trúc:

```json
{
  "business": {
    "name": "Giàn Phơi Thông Minh Bình Dương & TP.HCM",
    "tagline": "Đơn vị chuyên lắp đặt & sửa chữa giàn phơi thông minh, lưới cáp ban công uy tín tại TP.HCM & Bình Dương.",
    "phone": "+84902725760",
    "phone_display": "0902.725.760",
    "zalo_url": "https://zalo.me/0902725760",
    "email": "daihoaphat999@gmail.com",
    "street": "Đường 48, khu phố 6, Hiệp Bình Chánh",
    "city": "TP Hồ Chí Minh",
    "hours": "Mo-Su 07:30-19:00",
    "maps_query": "Hiệp Bình Chánh, TP Hồ Chí Minh"
  },
  "facts": [
    ["10+", "năm kinh nghiệm"],
    ["1000+", "công trình đã bàn giao"],
    ["70 kg", "tải trọng tối đa"],
    ["5 năm", "bảo hành"],
    ["24h", "phản hồi yêu cầu"]
  ],
  "services": [
    {
      "slug": "gian-phoi-dieu-khien",
      "name": "Giàn Phơi Thông Minh Điều Khiển",
      "group": "Giàn phơi",
      "price_from": 3200000,
      "price_to": 4500000,
      "unit": "bộ",
      "blurb": "Điều khiển bằng remote, sang trọng, tiết kiệm diện tích.",
      "popular": true,
      "svg": "gian-phoi-dieu-khien.svg",
      "specs": [
        {"label": "Vận hành", "value": "Remote điều khiển"},
        {"label": "Ưu điểm", "value": "Tiết kiệm diện tích"},
        {"label": "Bảo hành", "value": "5 năm"}
      ]
    }
  ],
  "faqs": [
    {
      "question": "Giàn phơi thông minh có điều khiển từ xa không?",
      "answer": "Có. Các mẫu giàn phơi thông minh đều được trang bị điều khiển từ xa, giúp nâng hạ dễ dàng, tiết kiệm sức lực và mang tính thẩm mỹ cao.",
      "contact_page": false
    }
  ],
  "areas": ["Thủ Đức", "Quận 1", "Quận 3", "Quận 7", "Dĩ An", "Thủ Dầu Một", "Bình Dương"],
  "posts": [
    {
      "slug": "quan-3",
      "title": "Lắp đặt giàn phơi thông minh chính hãng quận 3 TP HCM giá rẻ",
      "date": "29/5/2026",
      "iso_date": "2026-05-29",
      "img": "quan-3.webp",
      "desc": "Hướng dẫn lắp đặt giàn phơi thông minh chính hãng giá rẻ tại Quận 3 TP.HCM, quy trình 4 bước và bảng giá tham khảo.",
      "category": "Khu vực",
      "source": "docs/research/blog-raw/quan-3.txt"
    }
  ]
}
```

Điền đủ 8 dịch vụ, 10 FAQ, 12 bài. Đánh dấu `contact_page: true` cho đúng 4 câu về đặt lịch/báo giá: "Thời gian lắp đặt giàn phơi mất bao lâu?", "Dịch vụ có hỗ trợ đo đạc miễn phí không?", "Tôi có thể đặt giàn phơi theo kích thước riêng không?", "Lưới cáp có bền không và bảo hành bao lâu?".

Phân loại `category` cho 12 bài: `quan-1`, `quan-3`, `di-an`, `vach-lanh` → `"Khu vực"`; `top5-thuong-hieu`, `top5-mau`, `top10-don-vi`, `nhan-biet-chinh-hang` → `"So sánh"`; còn lại → `"Kiến thức"`.

- [ ] **Step 4: Viết `scripts/sitedata.py`**

```python
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
    desc: str
    category: str
    source: str


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

    faqs = tuple(Faq(**f) for f in _require(data, "faqs", full))
    posts = tuple(
        Post(**{**p, "source": os.path.join(ROOT, p["source"])})
        for p in _require(data, "posts", full)
    )
    facts = tuple((str(a), str(b)) for a, b in _require(data, "facts", full))
    areas = tuple(_require(data, "areas", full))

    return SiteData(business, tuple(services), faqs, areas, posts, facts)


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
```

- [ ] **Step 5: Chạy test, xác nhận pass**

Run: `python -m unittest tests.test_sitedata -v`
Expected: PASS, 20 tests

Nếu `test_exactly_one_popular_service` fail: đúng một dịch vụ được đặt `popular: true`, chọn `gian-phoi-treo-tran` hoặc `gian-phoi-dieu-khien`.

- [ ] **Step 6: Commit**

```bash
git add site.json scripts/sitedata.py tests/test_sitedata.py
git commit -m "feat: site.json làm nguồn dữ liệu duy nhất + loader có kiểm tra"
```

---

### Task 3: Tách module markdown

`md_to_html` trong `build_blog.py` hoạt động tốt nhưng chưa có test và chưa sinh anchor cho mục lục. Tách ra, pin hành vi bằng test, thêm phần trích heading.

**Files:**
- Create: `scripts/markdown.py`
- Create: `tests/test_markdown.py`
- Reference: `scripts/build_blog.py:56-118` (nguồn của `md_to_html`, `inline`)

**Interfaces:**
- Consumes: không
- Produces:
  - `md_to_html(md: str) -> str`
  - `strip_front_matter(raw: str) -> str` — bỏ khối `URL:` / `Thumb:` / `Title:` / `Date:` ở đầu file raw
  - `slugify(text: str) -> str` — bỏ dấu tiếng Việt, trả về chuỗi an toàn cho `id`
  - `add_heading_anchors(html: str) -> tuple[str, list[tuple[int, str, str]]]` — gắn `id` vào `<h2>`/`<h3>`, trả về `(html_mới, [(level, text, anchor), ...])`

- [ ] **Step 1: Viết test thất bại**

Tạo `tests/test_markdown.py`:

```python
import unittest

from scripts.markdown import (
    add_heading_anchors,
    md_to_html,
    slugify,
    strip_front_matter,
)


class TestMdToHtml(unittest.TestCase):
    def test_paragraph(self):
        self.assertEqual(md_to_html("Xin chào."), "<p>Xin chào.</p>")

    def test_headings(self):
        self.assertEqual(md_to_html("## Lợi ích"), "<h2>Lợi ích</h2>")
        self.assertEqual(md_to_html("### Chi tiết"), "<h3>Chi tiết</h3>")

    def test_unordered_list(self):
        self.assertEqual(
            md_to_html("- Một\n- Hai"),
            "<ul>\n<li>Một</li>\n<li>Hai</li>\n</ul>",
        )

    def test_ordered_list(self):
        self.assertEqual(
            md_to_html("1. Khảo sát\n2. Báo giá"),
            "<ol>\n<li>Khảo sát</li>\n<li>Báo giá</li>\n</ol>",
        )

    def test_bold_inline(self):
        self.assertEqual(md_to_html("Giá **rẻ** nhất"), "<p>Giá <strong>rẻ</strong> nhất</p>")

    def test_escapes_html_entities(self):
        self.assertIn("&amp;", md_to_html("TP.HCM & Bình Dương"))
        self.assertIn("&lt;script&gt;", md_to_html("<script>"))

    def test_table_first_row_is_header(self):
        html = md_to_html("| A | B |\n| --- | --- |\n| 1 | 2 |")
        self.assertIn("<th>A</th>", html)
        self.assertIn("<td>1</td>", html)
        self.assertNotIn("---", html)


class TestStripFrontMatter(unittest.TestCase):
    def test_removes_metadata_block(self):
        raw = "URL: https://x\nTitle: Y\nDate: 1/1/2025\n\n## Nội dung"
        self.assertEqual(strip_front_matter(raw), "## Nội dung")

    def test_leaves_plain_markdown_untouched(self):
        self.assertEqual(strip_front_matter("## Nội dung"), "## Nội dung")


class TestSlugify(unittest.TestCase):
    def test_strips_vietnamese_diacritics(self):
        self.assertEqual(slugify("Lợi ích nổi bật"), "loi-ich-noi-bat")

    def test_handles_d_with_stroke(self):
        self.assertEqual(slugify("Đặc điểm"), "dac-diem")

    def test_drops_punctuation(self):
        self.assertEqual(slugify("Giá bao nhiêu?"), "gia-bao-nhieu")


class TestAddHeadingAnchors(unittest.TestCase):
    def test_adds_ids_and_returns_outline(self):
        html, outline = add_heading_anchors("<h2>Lợi ích</h2>\n<p>x</p>\n<h3>Chi tiết</h3>")
        self.assertIn('<h2 id="loi-ich">', html)
        self.assertIn('<h3 id="chi-tiet">', html)
        self.assertEqual(outline, [(2, "Lợi ích", "loi-ich"), (3, "Chi tiết", "chi-tiet")])

    def test_deduplicates_repeated_headings(self):
        html, outline = add_heading_anchors("<h2>Giá</h2><h2>Giá</h2>")
        self.assertEqual([a for _, _, a in outline], ["gia", "gia-2"])
        self.assertIn('id="gia-2"', html)
```

- [ ] **Step 2: Chạy test, xác nhận thất bại**

Run: `python -m unittest tests.test_markdown -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'scripts.markdown'`

- [ ] **Step 3: Viết `scripts/markdown.py`**

Copy nguyên `inline()` và `md_to_html()` từ `scripts/build_blog.py` (dòng 56–118) — chúng đã đúng, đừng viết lại. Bổ sung:

```python
import re
import unicodedata

_D_STROKE = str.maketrans({"đ": "d", "Đ": "D"})
_HEADING = re.compile(r"<(h[23])>(.*?)</\1>")


def strip_front_matter(raw: str) -> str:
    if raw.startswith("URL:"):
        return re.split(r"\n\n", raw, maxsplit=1)[1].strip("\n")
    return raw


def slugify(text: str) -> str:
    text = text.translate(_D_STROKE)
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return text


def add_heading_anchors(html: str) -> tuple[str, list[tuple[int, str, str]]]:
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
```

- [ ] **Step 4: Chạy test, xác nhận pass**

Run: `python -m unittest tests.test_markdown -v`
Expected: PASS, 15 tests

- [ ] **Step 5: Commit**

```bash
git add scripts/markdown.py tests/test_markdown.py
git commit -m "refactor: tách markdown ra module riêng + anchor cho mục lục"
```

---

### Task 4: Template engine tối giản

Không dùng Jinja2 (thêm dependency cho một site 18 trang là thừa). Engine chỉ cần ba thứ: thay biến có escape, thay biến thô, và include partial. Vòng lặp làm bằng Python trong Task 5.

**Files:**
- Create: `scripts/template.py`
- Create: `tests/test_template.py`

**Interfaces:**
- Consumes: không
- Produces:
  - `class TemplateError(ValueError)`
  - `render(template_str: str, context: dict, *, partials_dir: str) -> str`
  - `render_file(path: str, context: dict, *, partials_dir: str) -> str`
  - `escape(text: str) -> str`

Cú pháp: `{{ name }}` escape HTML, `{{{ name }}}` chèn thô, `{{> ten-partial }}` include `partials_dir/ten-partial.html` rồi render đệ quy với cùng context.

- [ ] **Step 1: Viết test thất bại**

Tạo `tests/test_template.py`:

```python
import os
import tempfile
import unittest

from scripts.template import TemplateError, escape, render, render_file


class TestEscape(unittest.TestCase):
    def test_escapes_the_five_entities(self):
        self.assertEqual(escape('<a href="x">&\'</a>'), "&lt;a href=&quot;x&quot;&gt;&amp;&#39;&lt;/a&gt;")


class TestRender(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.partials = self.tmp.name
        self.addCleanup(self.tmp.cleanup)

    def write_partial(self, name: str, content: str) -> None:
        with open(os.path.join(self.partials, f"{name}.html"), "w", encoding="utf-8") as handle:
            handle.write(content)

    def test_substitutes_variable(self):
        out = render("Xin chào {{ name }}", {"name": "An"}, partials_dir=self.partials)
        self.assertEqual(out, "Xin chào An")

    def test_escapes_by_default(self):
        out = render("{{ v }}", {"v": "<b>x</b>"}, partials_dir=self.partials)
        self.assertEqual(out, "&lt;b&gt;x&lt;/b&gt;")

    def test_triple_brace_is_raw(self):
        out = render("{{{ v }}}", {"v": "<b>x</b>"}, partials_dir=self.partials)
        self.assertEqual(out, "<b>x</b>")

    def test_tolerates_whitespace_in_tag(self):
        self.assertEqual(render("{{name}}", {"name": "An"}, partials_dir=self.partials), "An")

    def test_includes_partial(self):
        self.write_partial("hello", "<p>{{ name }}</p>")
        out = render("{{> hello }}", {"name": "An"}, partials_dir=self.partials)
        self.assertEqual(out, "<p>An</p>")

    def test_partial_can_include_partial(self):
        self.write_partial("inner", "<i>{{ name }}</i>")
        self.write_partial("outer", "<b>{{> inner }}</b>")
        out = render("{{> outer }}", {"name": "An"}, partials_dir=self.partials)
        self.assertEqual(out, "<b><i>An</i></b>")

    def test_missing_variable_raises(self):
        with self.assertRaises(TemplateError) as ctx:
            render("{{ vang_mat }}", {}, partials_dir=self.partials)
        self.assertIn("vang_mat", str(ctx.exception))

    def test_missing_partial_raises(self):
        with self.assertRaises(TemplateError) as ctx:
            render("{{> khong-co }}", {}, partials_dir=self.partials)
        self.assertIn("khong-co", str(ctx.exception))

    def test_non_string_values_are_stringified(self):
        self.assertEqual(render("{{ n }}", {"n": 8}, partials_dir=self.partials), "8")


class TestRenderFile(unittest.TestCase):
    def test_reads_and_renders(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "page.html")
            with open(path, "w", encoding="utf-8") as handle:
                handle.write("<h1>{{ title }}</h1>")
            out = render_file(path, {"title": "Trang chủ"}, partials_dir=tmp)
            self.assertEqual(out, "<h1>Trang chủ</h1>")
```

- [ ] **Step 2: Chạy test, xác nhận thất bại**

Run: `python -m unittest tests.test_template -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'scripts.template'`

- [ ] **Step 3: Viết `scripts/template.py`**

```python
"""Template engine tối giản cho site tĩnh. Không dependency."""
from __future__ import annotations

import os
import re

_PARTIAL = re.compile(r"\{\{>\s*([a-z0-9_-]+)\s*\}\}")
_RAW = re.compile(r"\{\{\{\s*([a-zA-Z0-9_]+)\s*\}\}\}")
_VAR = re.compile(r"\{\{\s*([a-zA-Z0-9_]+)\s*\}\}")

MAX_DEPTH = 10


class TemplateError(ValueError):
    """Template tham chiếu biến hoặc partial không tồn tại."""


def escape(text: str) -> str:
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

    def lookup(name: str) -> object:
        if name not in context:
            raise TemplateError(f"Template dùng biến {name!r} nhưng context không có")
        return context[name]

    text = _RAW.sub(lambda m: str(lookup(m.group(1))), text)
    text = _VAR.sub(lambda m: escape(lookup(m.group(1))), text)
    return text


def render_file(path: str, context: dict, *, partials_dir: str) -> str:
    with open(path, encoding="utf-8") as handle:
        return render(handle.read(), context, partials_dir=partials_dir)
```

- [ ] **Step 4: Chạy test, xác nhận pass**

Run: `python -m unittest tests.test_template -v`
Expected: PASS, 11 tests

- [ ] **Step 5: Commit**

```bash
git add scripts/template.py tests/test_template.py
git commit -m "feat: template engine tối giản không dependency"
```

---

### Task 5: Component sinh HTML

Tất cả HTML lặp lại được sinh ở đây. Đây là nơi bốn yếu tố nhận diện của spec §3.6 thành code.

**Files:**
- Create: `scripts/components.py`
- Create: `tests/test_components.py`

**Interfaces:**
- Consumes: `scripts.sitedata` (`Service`, `Faq`, `Post`, `SiteData`, `format_price`, `service_groups`), `scripts.template.escape`
- Produces:
  - `spec_line(service: Service) -> str` — `<dl class="spec-line">`
  - `service_card(service: Service, *, svg_inline: str) -> str`
  - `numeric_rail(facts: tuple[tuple[str, str], ...]) -> str`
  - `stepper(steps: list[tuple[str, str]]) -> str`
  - `faq_list(faqs, *, id_prefix: str = "faq") -> str`
  - `post_card(post: Post) -> str`
  - `service_options(site: SiteData) -> str` — `<option>` cho dropdown form
  - `comparison_table(site: SiteData) -> str`
  - `area_list(areas: tuple[str, ...]) -> str`

- [ ] **Step 1: Viết test thất bại**

Tạo `tests/test_components.py`:

```python
import unittest

from scripts.components import (
    comparison_table,
    faq_list,
    numeric_rail,
    post_card,
    service_card,
    service_options,
    spec_line,
    stepper,
)
from scripts.sitedata import find_service, load_site

SITE = load_site()


class TestSpecLine(unittest.TestCase):
    def test_renders_definition_list_with_three_rows(self):
        html = spec_line(find_service(SITE, "gian-phoi-treo-tran"))
        self.assertIn('class="spec-line"', html)
        self.assertEqual(html.count("<dt>"), 3)
        self.assertEqual(html.count("<dd>"), 3)

    def test_includes_warranty_value(self):
        html = spec_line(find_service(SITE, "gian-phoi-dieu-khien"))
        self.assertIn("Bảo hành", html)


class TestServiceCard(unittest.TestCase):
    def test_has_id_price_and_quote_link(self):
        service = find_service(SITE, "luoi-cap-ban-cong")
        html = service_card(service, svg_inline="<svg></svg>")
        self.assertIn('id="luoi-cap-ban-cong"', html)
        self.assertIn("180.000 – 250.000đ/m²", html)
        self.assertIn("/lien-he.html", html)

    def test_popular_service_gets_badge(self):
        popular = next(s for s in SITE.services if s.popular)
        html = service_card(popular, svg_inline="<svg></svg>")
        self.assertIn("Phổ biến nhất", html)

    def test_ordinary_service_has_no_badge(self):
        plain = next(s for s in SITE.services if not s.popular)
        html = service_card(plain, svg_inline="<svg></svg>")
        self.assertNotIn("Phổ biến nhất", html)

    def test_never_emits_inline_style(self):
        for service in SITE.services:
            with self.subTest(service=service.slug):
                self.assertNotIn("style=", service_card(service, svg_inline="<svg></svg>"))


class TestNumericRail(unittest.TestCase):
    def test_renders_every_fact(self):
        html = numeric_rail(SITE.facts)
        self.assertEqual(html.count('class="rail__item"'), 5)
        self.assertIn("1000+", html)


class TestStepper(unittest.TestCase):
    def test_numbers_steps_from_one(self):
        html = stepper([("Tiếp nhận", "x"), ("Khảo sát", "y")])
        self.assertIn(">1<", html)
        self.assertIn(">2<", html)

    def test_uses_ordered_list_for_semantics(self):
        self.assertIn("<ol", stepper([("A", "x")]))


class TestFaqList(unittest.TestCase):
    def test_button_carries_aria_attributes(self):
        html = faq_list(SITE.faqs[:2])
        self.assertIn('aria-expanded="false"', html)
        self.assertIn("aria-controls=", html)

    def test_ids_are_unique_across_items(self):
        html = faq_list(SITE.faqs)
        ids = [chunk.split('"')[0] for chunk in html.split('id="')[1:]]
        self.assertEqual(len(ids), len(set(ids)))

    def test_prefix_isolates_two_lists_on_one_page(self):
        a = faq_list(SITE.faqs[:2], id_prefix="faq-a")
        b = faq_list(SITE.faqs[:2], id_prefix="faq-b")
        self.assertNotIn("faq-a", b)


class TestServiceOptions(unittest.TestCase):
    def test_lists_all_eight_real_services(self):
        # Sửa lỗi C4: dropdown cũ chỉ có 4 loại cửa lưới.
        html = service_options(SITE)
        self.assertEqual(html.count("<option"), 9)  # 8 dịch vụ + 1 placeholder
        for service in SITE.services:
            with self.subTest(service=service.slug):
                self.assertIn(service.name, html)


class TestComparisonTable(unittest.TestCase):
    def test_covers_the_three_drying_racks(self):
        html = comparison_table(SITE)
        for slug in ("gian-phoi-dieu-khien", "gian-phoi-treo-tran", "gian-phoi-xep-tuong"):
            with self.subTest(slug=slug):
                self.assertIn(find_service(SITE, slug).name, html)

    def test_has_scope_attributes_for_screen_readers(self):
        self.assertIn('scope="col"', comparison_table(SITE))


class TestPostCard(unittest.TestCase):
    def test_carries_category_for_filtering(self):
        html = post_card(SITE.posts[0])
        self.assertIn("data-category=", html)

    def test_uses_machine_readable_time(self):
        html = post_card(SITE.posts[0])
        self.assertIn("<time datetime=", html)

    def test_image_has_dimensions(self):
        html = post_card(SITE.posts[0])
        self.assertIn("width=", html)
        self.assertIn("height=", html)
```

- [ ] **Step 2: Chạy test, xác nhận thất bại**

Run: `python -m unittest tests.test_components -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'scripts.components'`

- [ ] **Step 3: Viết `scripts/components.py`**

Mẫu cho hai component; các hàm còn lại theo cùng phong cách — nhận dataclass, trả chuỗi HTML, không `style=`, không markup rỗng:

```python
"""Sinh chuỗi HTML cho các component tái dùng."""
from __future__ import annotations

from scripts.sitedata import Faq, Post, Service, SiteData, format_price
from scripts.template import escape


def spec_line(service: Service) -> str:
    rows = "\n".join(
        f"      <div class=\"spec-line__row\">"
        f"<dt>{escape(spec.label)}</dt><dd>{escape(spec.value)}</dd></div>"
        for spec in service.specs
    )
    return f'    <dl class="spec-line">\n{rows}\n    </dl>'


def service_card(service: Service, *, svg_inline: str) -> str:
    badge = (
        '      <span class="badge badge--popular">Phổ biến nhất</span>\n'
        if service.popular
        else ""
    )
    return (
        f'  <article class="card card--service" id="{escape(service.slug)}">\n'
        f'    <div class="card__figure" aria-hidden="true">{svg_inline}</div>\n'
        f'    <div class="card__body">\n'
        f"{badge}"
        f"      <h3>{escape(service.name)}</h3>\n"
        f'      <p class="card__price">{escape(format_price(service))}</p>\n'
        f"      <p>{escape(service.blurb)}</p>\n"
        f"{spec_line(service)}\n"
        f'      <a class="btn btn--primary" href="/lien-he.html?dich-vu={escape(service.slug)}">'
        f"Nhận báo giá</a>\n"
        f"    </div>\n"
        f"  </article>"
    )
```

Ghi chú triển khai cho các hàm còn lại:
- `faq_list`: mỗi mục là `<button aria-expanded="false" aria-controls="{prefix}-{i}-panel" id="{prefix}-{i}-btn">` và `<div id="{prefix}-{i}-panel" role="region" aria-labelledby="{prefix}-{i}-btn" hidden>`.
- `stepper`: `<ol class="stepper">`, số thứ tự do `<span class="stepper__num">` mang, không dùng CSS counter (screen reader cần đọc được).
- `service_options`: option đầu là `<option value="">Chọn dịch vụ cần báo giá</option>`, sau đó `value` là `service.slug`.
- `comparison_table`: cột `Loại | Không gian phù hợp | Vận hành | Giá | Bảo hành`, chỉ 3 dịch vụ nhóm "Giàn phơi"; `<th scope="col">` ở hàng đầu, `<th scope="row">` ở cột tên.
- `post_card`: `<time datetime="{post.iso_date}">{post.date}</time>`, thuộc tính `data-category` để Task 12 lọc bằng JS; ảnh `width="480" height="320"`.

- [ ] **Step 4: Chạy test, xác nhận pass**

Run: `python -m unittest tests.test_components -v`
Expected: PASS, 18 tests

- [ ] **Step 5: Commit**

```bash
git add scripts/components.py tests/test_components.py
git commit -m "feat: component sinh HTML — spec-line, card, rail, stepper, faq"
```

---

### Task 6: JSON-LD structured data

Sửa mục §2.7 của spec. Đây là thứ quyết định site có xuất hiện trong kết quả tìm kiếm local hay không.

**Files:**
- Create: `scripts/schema.py`
- Create: `tests/test_schema.py`

**Interfaces:**
- Consumes: `scripts.sitedata` (`SiteData`, `Service`, `Faq`, `Post`, `format_price`)
- Produces:
  - `BASE_URL: str` — đọc từ biến môi trường `SITE_BASE_URL`, mặc định `"https://gianphoithongminh.vn"`
  - `local_business(site: SiteData) -> dict`
  - `service_schema(site: SiteData, service: Service) -> dict`
  - `faq_page(faqs: tuple[Faq, ...]) -> dict`
  - `breadcrumb_list(crumbs: list[tuple[str, str]]) -> dict` — `[(tên, đường dẫn)]`
  - `blog_posting(site: SiteData, post: Post) -> dict`
  - `to_jsonld(*objects: dict) -> str` — trả về thẻ `<script type="application/ld+json">` hoàn chỉnh

- [ ] **Step 1: Viết test thất bại**

Tạo `tests/test_schema.py`:

```python
import json
import unittest

from scripts.schema import (
    blog_posting,
    breadcrumb_list,
    faq_page,
    local_business,
    service_schema,
    to_jsonld,
)
from scripts.sitedata import find_service, load_site

SITE = load_site()


class TestLocalBusiness(unittest.TestCase):
    def setUp(self):
        self.data = local_business(SITE)

    def test_type_and_context(self):
        self.assertEqual(self.data["@context"], "https://schema.org")
        self.assertEqual(self.data["@type"], "LocalBusiness")

    def test_phone_matches_site_data(self):
        self.assertEqual(self.data["telephone"], SITE.business.phone)

    def test_address_is_postal_address(self):
        self.assertEqual(self.data["address"]["@type"], "PostalAddress")
        self.assertEqual(self.data["address"]["addressCountry"], "VN")

    def test_area_served_lists_every_area(self):
        served = {a["name"] for a in self.data["areaServed"]}
        self.assertEqual(served, set(SITE.areas))

    def test_has_opening_hours(self):
        self.assertIn("openingHours", self.data)


class TestServiceSchema(unittest.TestCase):
    def test_carries_price_range_and_provider(self):
        data = service_schema(SITE, find_service(SITE, "gian-phoi-dieu-khien"))
        self.assertEqual(data["@type"], "Service")
        self.assertIn("3.200.000", data["offers"]["priceRange"])
        self.assertEqual(data["provider"]["name"], SITE.business.name)

    def test_offer_currency_is_vnd(self):
        data = service_schema(SITE, find_service(SITE, "luoi-cap-ban-cong"))
        self.assertEqual(data["offers"]["priceCurrency"], "VND")


class TestFaqPage(unittest.TestCase):
    def test_maps_every_faq_to_a_question(self):
        data = faq_page(SITE.faqs)
        self.assertEqual(data["@type"], "FAQPage")
        self.assertEqual(len(data["mainEntity"]), 10)
        self.assertEqual(data["mainEntity"][0]["@type"], "Question")
        self.assertEqual(
            data["mainEntity"][0]["acceptedAnswer"]["@type"], "Answer"
        )


class TestBreadcrumbList(unittest.TestCase):
    def test_positions_start_at_one_and_are_absolute(self):
        data = breadcrumb_list([("Trang chủ", "/"), ("Dịch vụ", "/dich-vu.html")])
        self.assertEqual(data["itemListElement"][0]["position"], 1)
        self.assertEqual(data["itemListElement"][1]["position"], 2)
        self.assertTrue(data["itemListElement"][1]["item"].startswith("https://"))


class TestBlogPosting(unittest.TestCase):
    def test_uses_iso_date_and_absolute_image(self):
        data = blog_posting(SITE, SITE.posts[0])
        self.assertEqual(data["datePublished"], SITE.posts[0].iso_date)
        self.assertTrue(data["image"].startswith("https://"))


class TestToJsonld(unittest.TestCase):
    def test_wraps_in_script_tag_with_valid_json(self):
        out = to_jsonld(local_business(SITE))
        self.assertTrue(out.startswith('<script type="application/ld+json">'))
        self.assertTrue(out.rstrip().endswith("</script>"))
        payload = out.split(">", 1)[1].rsplit("<", 1)[0]
        json.loads(payload)

    def test_multiple_objects_become_a_json_array(self):
        out = to_jsonld(local_business(SITE), faq_page(SITE.faqs))
        payload = json.loads(out.split(">", 1)[1].rsplit("<", 1)[0])
        self.assertIsInstance(payload, list)
        self.assertEqual(len(payload), 2)

    def test_output_cannot_break_out_of_script_tag(self):
        # Bảo vệ XSS: "</script>" trong dữ liệu phải được thoát.
        out = to_jsonld({"name": "</script><img onerror=alert(1)>"})
        self.assertNotIn("</script><img", out)
```

- [ ] **Step 2: Chạy test, xác nhận thất bại**

Run: `python -m unittest tests.test_schema -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'scripts.schema'`

- [ ] **Step 3: Viết `scripts/schema.py`**

Điểm cần chú ý: `to_jsonld` phải thoát `<` thành `\u003c` để dữ liệu không phá được thẻ `<script>`:

```python
import json
import os

BASE_URL = os.environ.get("SITE_BASE_URL", "https://gianphoithongminh.vn").rstrip("/")


def _abs(path: str) -> str:
    return f"{BASE_URL}/{path.lstrip('/')}"


def to_jsonld(*objects: dict) -> str:
    payload = objects[0] if len(objects) == 1 else list(objects)
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    text = text.replace("<", "\\u003c").replace(">", "\\u003e")
    return f'<script type="application/ld+json">\n{text}\n</script>'
```

Các hàm còn lại trả về dict theo schema.org; dùng `_abs()` cho mọi URL và ảnh.

- [ ] **Step 4: Chạy test, xác nhận pass**

Run: `python -m unittest tests.test_schema -v`
Expected: PASS, 12 tests

- [ ] **Step 5: Commit**

```bash
git add scripts/schema.py tests/test_schema.py
git commit -m "feat: JSON-LD LocalBusiness, Service, FAQPage, Breadcrumb, BlogPosting"
```

---

### Task 7: Nền tảng CSS — tokens và base layer

Viết lại `main.css` từ đầu. Task này chỉ làm hai layer đầu; component ở Task 8.

**Files:**
- Modify: `assets/css/main.css` (thay thế hoàn toàn 419 dòng hiện có)
- Create: `tests/test_css.py`

**Interfaces:**
- Consumes: `scripts.color` (`contrast_ratio`, `parse_css_tokens`, `passes_aa`)
- Produces: `assets/css/main.css` có `@layer tokens, base, layout, components, utilities;` ở dòng đầu

- [ ] **Step 1: Viết test thất bại**

Tạo `tests/test_css.py`:

```python
import os
import re
import unittest

from scripts.color import contrast_ratio, parse_css_tokens

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSS_PATH = os.path.join(ROOT, "assets", "css", "main.css")

with open(CSS_PATH, encoding="utf-8") as handle:
    CSS = handle.read()

TOKENS = parse_css_tokens(CSS)

REQUIRED_COLOR_TOKENS = [
    "--ink", "--ink-soft", "--muted", "--steel", "--steel-deep",
    "--paper", "--surface", "--hairline",
    "--amber", "--amber-bright", "--amber-tint", "--amber-ink",
]

EXPECTED = {
    "--ink": "#0F1C26", "--ink-soft": "#33506A", "--muted": "#5A6873",
    "--steel": "#1E3446", "--steel-deep": "#162836",
    "--paper": "#FBFAF8", "--surface": "#FFFFFF", "--hairline": "#E3E0DA",
    "--amber": "#B4530A", "--amber-bright": "#E07A1F",
    "--amber-tint": "#FDF1E3", "--amber-ink": "#8A3D06",
}


class TestTokens(unittest.TestCase):
    def test_all_required_tokens_defined(self):
        for name in REQUIRED_COLOR_TOKENS:
            with self.subTest(token=name):
                self.assertIn(name, TOKENS)

    def test_token_values_match_spec_exactly(self):
        for name, value in EXPECTED.items():
            with self.subTest(token=name):
                self.assertEqual(TOKENS[name], value)

    def test_legacy_tokens_are_gone(self):
        for dead in ("--color-primary", "--color-accent", "--color-ink",
                     "--radius-sm", "--radius-md", "--radius-lg", "--radius-pill"):
            with self.subTest(token=dead):
                self.assertNotIn(dead, CSS)

    def test_only_three_radius_tokens(self):
        radii = set(re.findall(r"--r(?:-sm|-pill)?\s*:", CSS))
        self.assertEqual(len(radii), 3)

    def test_spacing_scale_present(self):
        for i in range(1, 11):
            with self.subTest(step=i):
                self.assertIn(f"--space-{i}:", CSS)


class TestContrastOfRealTokens(unittest.TestCase):
    """Đọc màu thật trong CSS — test không thể trôi khỏi implementation."""

    def test_body_text_on_page_background(self):
        self.assertGreaterEqual(contrast_ratio(TOKENS["--ink"], TOKENS["--paper"]), 4.5)

    def test_muted_text_on_both_surfaces(self):
        for bg in ("--paper", "--surface"):
            with self.subTest(bg=bg):
                self.assertGreaterEqual(contrast_ratio(TOKENS["--muted"], TOKENS[bg]), 4.5)

    def test_white_on_primary_cta(self):
        self.assertGreaterEqual(contrast_ratio("#FFFFFF", TOKENS["--amber"]), 4.5)

    def test_white_on_steel_band(self):
        self.assertGreaterEqual(contrast_ratio("#FFFFFF", TOKENS["--steel"]), 4.5)

    def test_amber_link_on_paper(self):
        self.assertGreaterEqual(contrast_ratio(TOKENS["--amber"], TOKENS["--paper"]), 4.5)

    def test_badge_pair(self):
        self.assertGreaterEqual(
            contrast_ratio(TOKENS["--amber-ink"], TOKENS["--amber-tint"]), 4.5
        )

    def test_amber_bright_is_large_text_only(self):
        ratio = contrast_ratio(TOKENS["--amber-bright"], TOKENS["--steel"])
        self.assertGreaterEqual(ratio, 3.0)
        self.assertLess(ratio, 4.5, "Nếu đạt 4.5 thì bỏ được giới hạn chữ lớn")


class TestStructure(unittest.TestCase):
    def test_declares_layer_order_first(self):
        first = next(line for line in CSS.splitlines() if line.strip() and not line.strip().startswith("/*"))
        self.assertEqual(first.strip(), "@layer tokens, base, layout, components, utilities;")

    def test_has_focus_visible(self):
        self.assertIn(":focus-visible", CSS)

    def test_has_reduced_motion_guard(self):
        self.assertIn("prefers-reduced-motion", CSS)

    def test_no_three_pixel_accent_borders(self):
        # Spec §3.2 quy tắc 2 — bản cũ có 5 kiểu viền 3px khác nhau.
        self.assertEqual(re.findall(r"border[a-z-]*:\s*3px", CSS), [])

    def test_declares_both_font_families(self):
        self.assertIn("Be Vietnam Pro", CSS)
        self.assertIn("Inter", CSS)

    def test_uses_tabular_numerals_for_figures(self):
        self.assertIn("tabular-nums", CSS)
```

- [ ] **Step 2: Chạy test, xác nhận thất bại**

Run: `python -m unittest tests.test_css -v`
Expected: FAIL — nhiều test đỏ (token cũ còn nguyên, không có `@layer`, có `border-top: 3px`)

- [ ] **Step 3: Viết layer `tokens` và `base`**

Thay toàn bộ `assets/css/main.css`. Mở đầu chính xác như sau:

```css
@layer tokens, base, layout, components, utilities;

@layer tokens {
  :root {
    /* Màu — spec §3.3, đã verify tương phản */
    --ink: #0F1C26;
    --ink-soft: #33506A;
    --muted: #5A6873;
    --steel: #1E3446;
    --steel-deep: #162836;
    --paper: #FBFAF8;
    --surface: #FFFFFF;
    --hairline: #E3E0DA;
    --amber: #B4530A;
    --amber-bright: #E07A1F;
    --amber-tint: #FDF1E3;
    --amber-ink: #8A3D06;

    /* Chữ */
    --font-display: "Be Vietnam Pro", system-ui, sans-serif;
    --font-body: "Inter", system-ui, -apple-system, sans-serif;
    --fs-xs: 0.8125rem;
    --fs-sm: 0.875rem;
    --fs-base: 1rem;
    --fs-md: 1.125rem;
    --fs-lg: clamp(1.25rem, 1.6vw, 1.375rem);
    --fs-xl: clamp(1.5rem, 2.2vw, 1.75rem);
    --fs-2xl: clamp(1.875rem, 3vw, 2.25rem);
    --fs-3xl: clamp(2.25rem, 4vw, 3rem);
    --fs-4xl: clamp(2.75rem, 5.5vw, 3.75rem);
    --lh-display: 1.15;
    --lh-body: 1.65;

    /* Không gian */
    --space-1: 4px;  --space-2: 8px;  --space-3: 12px; --space-4: 16px;
    --space-5: 24px; --space-6: 32px; --space-7: 48px; --space-8: 64px;
    --space-9: 96px; --space-10: 128px;

    /* Hình khối */
    --r-sm: 6px;
    --r: 10px;
    --r-pill: 999px;
    --container: 1200px;
    --gutter: 24px;

    /* Đổ bóng — đúng hai mức */
    --shadow-raised: 0 12px 28px rgba(15, 28, 38, 0.10);
    --shadow-bar: 0 -2px 16px rgba(15, 28, 38, 0.12);

    /* Chuyển động */
    --ease: cubic-bezier(0.2, 0, 0, 1);
    --dur-fast: 150ms;
    --dur-move: 250ms;
  }
}

@layer base {
  *, *::before, *::after { box-sizing: border-box; }
  * { margin: 0; padding: 0; }

  html { scroll-behavior: smooth; }

  body {
    font-family: var(--font-body);
    font-size: var(--fs-base);
    line-height: var(--lh-body);
    color: var(--ink);
    background: var(--paper);
    -webkit-font-smoothing: antialiased;
  }

  h1, h2, h3, h4 {
    font-family: var(--font-display);
    line-height: var(--lh-display);
    font-weight: 700;
    letter-spacing: -0.015em;
    text-wrap: balance;
  }

  img { max-width: 100%; height: auto; display: block; }
  ul, ol { list-style: none; }
  a { color: inherit; text-decoration: none; }
  button, input, select, textarea { font: inherit; color: inherit; }

  :focus-visible {
    outline: 2px solid var(--amber);
    outline-offset: 2px;
    border-radius: var(--r-sm);
  }

  .skip-link {
    position: absolute;
    left: var(--space-4);
    top: calc(-1 * var(--space-10));
    z-index: 200;
    background: var(--surface);
    padding: var(--space-3) var(--space-4);
    border-radius: var(--r-sm);
  }
  .skip-link:focus { top: var(--space-4); }

  .price, .spec-line dd, .rail__value, table td, table th {
    font-variant-numeric: tabular-nums;
  }

  @media (prefers-reduced-motion: reduce) {
    html { scroll-behavior: auto; }
    *, *::before, *::after {
      animation-duration: 0.01ms !important;
      animation-iteration-count: 1 !important;
      transition-duration: 0.01ms !important;
    }
  }
}
```

- [ ] **Step 4: Chạy test, xác nhận pass**

Run: `python -m unittest tests.test_css -v`
Expected: PASS, 17 tests

Lưu ý: `test_no_three_pixel_accent_borders` chỉ pass khi CSS cũ đã bị xóa sạch — đừng để sót phần dưới file.

- [ ] **Step 5: Commit**

```bash
git add assets/css/main.css tests/test_css.py
git commit -m "feat: viết lại nền tảng CSS — token Thép & Nắng, base layer, a11y"
```

---

### Task 8: CSS component và layout

**Files:**
- Modify: `assets/css/main.css` (thêm layer `layout`, `components`, `utilities`)
- Modify: `tests/test_css.py` (thêm class test mới ở cuối file)

**Interfaces:**
- Consumes: token từ Task 7
- Produces: các class mà Task 5 và Task 9–12 tham chiếu:
  `.container` `.band` `.band--paper` `.band--steel` `.grid` `.grid--2` `.grid--3` `.grid--4`
  `.btn` `.btn--primary` `.btn--ghost` `.btn--quiet`
  `.card` `.card--service` `.card__figure` `.card__body` `.card__price`
  `.spec-line` `.spec-line__row` `.badge` `.badge--popular`
  `.rail` `.rail__item` `.rail__value` `.rail__label`
  `.stepper` `.stepper__num` `.faq` `.faq__question` `.faq__panel`
  `.site-header` `.nav` `.nav__link` `.nav-toggle`
  `.sticky-bar` `.sticky-bar__action` `.site-footer`
  `.field` `.field__error` `.chip` `.chip--active`
  `.article` `.toc` `.quote-aside`

- [ ] **Step 1: Viết test thất bại**

Thêm vào cuối `tests/test_css.py`:

```python
class TestComponentClasses(unittest.TestCase):
    REQUIRED = [
        ".container", ".band", ".band--steel", ".grid",
        ".btn", ".btn--primary", ".btn--ghost",
        ".card", ".card--service", ".card__price",
        ".spec-line", ".badge--popular",
        ".rail", ".rail__value", ".stepper", ".stepper__num",
        ".faq__question", ".faq__panel",
        ".site-header", ".nav__link", ".nav-toggle",
        ".sticky-bar", ".site-footer",
        ".field", ".field__error", ".chip",
        ".article", ".toc", ".quote-aside",
    ]

    def test_every_component_class_defined(self):
        for selector in self.REQUIRED:
            with self.subTest(selector=selector):
                self.assertIn(selector, CSS)

    def test_amber_bright_only_used_at_large_sizes(self):
        """Ràng buộc toàn cục #4: --amber-bright chỉ cho chữ >= 24px, weight >= 700."""
        blocks = re.findall(r"\{[^{}]*var\(--amber-bright\)[^{}]*\}", CSS)
        self.assertTrue(blocks, "Không tìm thấy chỗ nào dùng --amber-bright")
        for block in blocks:
            with self.subTest(block=block[:60]):
                has_large_font = re.search(r"font-size:\s*var\(--fs-(2xl|3xl|4xl)\)", block)
                is_border_or_icon = re.search(r"(border|stroke|fill|background)", block)
                self.assertTrue(
                    has_large_font or is_border_or_icon,
                    "--amber-bright dùng cho chữ nhỏ — vi phạm ngưỡng tương phản 4.27:1",
                )

    def test_transitions_use_only_the_two_durations(self):
        durations = set(re.findall(r"transition[^;]*?(\d+)ms", CSS))
        self.assertTrue(durations <= {"150", "250"}, f"Thời lượng lạ: {durations}")

    def test_transitions_only_animate_transform_and_opacity(self):
        props = re.findall(r"transition:\s*([a-z-]+)\s", CSS)
        allowed = {"transform", "opacity", "color", "background", "background-color",
                   "border-color", "outline-color", "all"}
        for prop in props:
            with self.subTest(prop=prop):
                self.assertIn(prop, allowed)
                self.assertNotEqual(prop, "all", "transition: all làm jank — liệt kê cụ thể")

    def test_touch_targets_reach_44px(self):
        for selector in (".btn", ".sticky-bar__action", ".nav-toggle"):
            with self.subTest(selector=selector):
                block = re.search(re.escape(selector) + r"\s*\{([^{}]*)\}", CSS)
                self.assertIsNotNone(block, f"{selector} chưa định nghĩa")
                self.assertIn("min-height", block.group(1))

    def test_sticky_bar_is_mobile_only(self):
        self.assertRegex(CSS, r"@media[^{]*min-width[^{]*\{[^}]*\.sticky-bar[^}]*display:\s*none")


class TestNoHorizontalOverflow(unittest.TestCase):
    def test_no_fixed_min_width_wider_than_phone(self):
        widths = [int(w) for w in re.findall(r"min-width:\s*(\d+)px", CSS)]
        inline_only = [w for w in widths if w < 100]
        media_queries = [w for w in widths if w >= 100]
        self.assertTrue(all(w >= 320 for w in media_queries))
        self.assertEqual([w for w in inline_only if w > 320], [])

    def test_tables_scroll_inside_their_own_container(self):
        self.assertRegex(CSS, r"overflow-x:\s*auto")
```

- [ ] **Step 2: Chạy test, xác nhận thất bại**

Run: `python -m unittest tests.test_css -v`
Expected: FAIL — `test_every_component_class_defined` đỏ cho hầu hết selector

- [ ] **Step 3: Viết layer `layout`, `components`, `utilities`**

Điểm bắt buộc, bám spec §3:

**Layout** — band trải hết chiều rộng, container nằm trong. Thay hẳn cách cũ (`.bg-alt` bo góc trong container):
```css
@layer layout {
  .container {
    width: 100%;
    max-width: var(--container);
    margin-inline: auto;
    padding-inline: var(--gutter);
  }
  .band { padding-block: clamp(var(--space-8), 8vw, var(--space-10)); }
  .band--paper { background: var(--paper); }
  .band--steel { background: var(--steel); color: #fff; }
  .grid { display: grid; gap: var(--space-5); }
  .grid--2 { grid-template-columns: repeat(2, 1fr); }
  .grid--3 { grid-template-columns: repeat(3, 1fr); }
  .grid--4 { grid-template-columns: repeat(4, 1fr); }
  @media (max-width: 1024px) {
    .grid--3, .grid--4 { grid-template-columns: repeat(2, 1fr); }
  }
  @media (max-width: 640px) {
    .grid--2, .grid--3, .grid--4 { grid-template-columns: 1fr; }
  }
}
```

**Component** — mọi viền là `1px solid var(--hairline)`. Không có `border-top: 3px` ở bất kỳ đâu.

`.spec-line` là chữ ký thị giác (spec §3.6): `<dl>` với `.spec-line__row` dùng `display: flex; justify-content: space-between;` và `border-bottom: 1px solid var(--hairline)`; `dt` màu `--muted` cỡ `--fs-sm`, `dd` màu `--ink` `font-weight: 600`.

`.rail` trên nền `--steel`, `.rail__value` là chỗ duy nhất dùng `--amber-bright` cho chữ, phải kèm `font-size: var(--fs-2xl)` trở lên và `font-weight: 800` (test sẽ kiểm).

`.nav__link` gạch chân hổ phách mọc từ trái:
```css
.nav__link::after {
  content: "";
  position: absolute;
  inset-inline: 0;
  bottom: -4px;
  height: 2px;
  background: var(--amber);
  transform: scaleX(0);
  transform-origin: left;
}
@media (prefers-reduced-motion: no-preference) {
  .nav__link::after { transition: transform var(--dur-move) var(--ease); }
}
.nav__link:hover::after, .nav__link[aria-current="page"]::after { transform: scaleX(1); }
```

`.sticky-bar`: `position: fixed; inset-inline: 0; bottom: 0;` với `padding-bottom: env(safe-area-inset-bottom)`, ẩn ở `@media (min-width: 768px)`. Mỗi `.sticky-bar__action` có `min-height: 56px`.

`.btn`, `.nav-toggle`, `.sticky-bar__action` đều phải có `min-height: 44px`.

Bảng so sánh bọc trong `.table-scroll { overflow-x: auto; }`.

- [ ] **Step 4: Chạy test, xác nhận pass**

Run: `python -m unittest tests.test_css -v`
Expected: PASS, 24 tests

- [ ] **Step 5: Kiểm tra thủ công bằng mắt**

```bash
python -m http.server 8000
```
Mở `http://localhost:8000` — trang sẽ còn vỡ vì HTML chưa dựng lại (Task 9). Chỉ cần xác nhận CSS load được, không có lỗi parse trong DevTools Console.

- [ ] **Step 6: Commit**

```bash
git add assets/css/main.css tests/test_css.py
git commit -m "feat: CSS layout + component — band, spec-line, rail, stepper, sticky bar"
```

---

### Task 9: Hình vẽ nét SVG cho 8 dịch vụ

Yếu tố nhận diện số 2 (spec §3.6). Thay hoàn toàn ảnh stock sai chủ đề trong grid dịch vụ.

**Files:**
- Create: `assets/svg/gian-phoi-dieu-khien.svg`, `gian-phoi-treo-tran.svg`, `gian-phoi-xep-tuong.svg`, `luoi-cap-ban-cong.svg`, `cua-luoi-chong-muoi.svg`, `vach-ngan-lanh.svg`, `mai-hien-quay-tay.svg`, `bat-che-nang-mua.svg`
- Create: `tests/test_svg.py`

**Interfaces:**
- Consumes: `scripts.sitedata` (trường `Service.svg`)
- Produces: 8 file SVG, mỗi file `viewBox="0 0 240 180"`, nét `stroke-width="1.5"`, `stroke="currentColor"`, `fill="none"`, có `role="img"` và `<title>`

- [ ] **Step 1: Viết test thất bại**

Tạo `tests/test_svg.py`:

```python
import os
import unittest
import xml.etree.ElementTree as ET

from scripts.sitedata import load_site

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SVG_DIR = os.path.join(ROOT, "assets", "svg")
SITE = load_site()


class TestProductLineDrawings(unittest.TestCase):
    def test_one_svg_per_service(self):
        for service in SITE.services:
            with self.subTest(service=service.slug):
                self.assertTrue(os.path.exists(os.path.join(SVG_DIR, service.svg)))

    def test_all_share_the_same_viewbox(self):
        for service in SITE.services:
            with self.subTest(service=service.slug):
                root = ET.parse(os.path.join(SVG_DIR, service.svg)).getroot()
                self.assertEqual(root.get("viewBox"), "0 0 240 180")

    def test_stroke_style_is_consistent(self):
        for service in SITE.services:
            with self.subTest(service=service.slug):
                text = open(os.path.join(SVG_DIR, service.svg), encoding="utf-8").read()
                self.assertIn('stroke-width="1.5"', text)
                self.assertIn('stroke="currentColor"', text)
                self.assertIn('fill="none"', text)

    def test_no_hardcoded_colour(self):
        """Màu đến từ CSS qua currentColor — SVG không được ghim hex."""
        for service in SITE.services:
            with self.subTest(service=service.slug):
                text = open(os.path.join(SVG_DIR, service.svg), encoding="utf-8").read()
                self.assertNotIn("#", text)

    def test_has_accessible_title(self):
        ns = "{http://www.w3.org/2000/svg}"
        for service in SITE.services:
            with self.subTest(service=service.slug):
                root = ET.parse(os.path.join(SVG_DIR, service.svg)).getroot()
                title = root.find(f"{ns}title")
                self.assertIsNotNone(title, "SVG thiếu <title>")
                self.assertTrue(title.text.strip())

    def test_drawing_is_not_trivially_empty(self):
        for service in SITE.services:
            with self.subTest(service=service.slug):
                text = open(os.path.join(SVG_DIR, service.svg), encoding="utf-8").read()
                marks = sum(text.count(f"<{tag}") for tag in ("path", "line", "rect", "circle", "polyline"))
                self.assertGreaterEqual(marks, 4, "Hình quá sơ sài, cần ít nhất 4 nét")
```

- [ ] **Step 2: Chạy test, xác nhận thất bại**

Run: `python -m unittest tests.test_svg -v`
Expected: FAIL — `assets/svg/` chưa tồn tại

- [ ] **Step 3: Vẽ 8 hình**

Mỗi hình vẽ **cơ cấu thật**, không phải icon trừu tượng. Ví dụ `gian-phoi-treo-tran.svg`:

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 180" role="img"
     fill="none" stroke="currentColor" stroke-width="1.5"
     stroke-linecap="round" stroke-linejoin="round">
  <title>Giàn phơi treo trần quay tay: hai thanh phơi inox nâng hạ bằng dây cáp</title>
  <line x1="20" y1="24" x2="220" y2="24"/>
  <rect x="96" y="24" width="48" height="14" rx="2"/>
  <line x1="108" y1="38" x2="108" y2="96"/>
  <line x1="132" y1="38" x2="132" y2="112"/>
  <line x1="56" y1="96" x2="184" y2="96"/>
  <line x1="56" y1="112" x2="184" y2="112"/>
  <circle cx="196" cy="60" r="10"/>
  <line x1="196" y1="60" x2="206" y2="52"/>
  <path d="M72 96v24M96 96v20M120 112v22M144 112v18M168 96v26"/>
</svg>
```

Bảy hình còn lại theo cùng khung 240×180 và cùng ngôn ngữ nét. Gợi ý nội dung:
- `gian-phoi-dieu-khien`: giàn treo trần + hộp motor + remote có sóng phát
- `gian-phoi-xep-tuong`: cánh tay gấp xếp sát tường, ký hiệu cung xoay
- `luoi-cap-ban-cong`: lan can + lưới cáp đan chéo + tăng đơ
- `cua-luoi-chong-muoi`: khung cửa + hộp cuốn + lưới xếp ly
- `vach-ngan-lanh`: khung cửa + dải nhựa PVC dọc
- `mai-hien-quay-tay`: mái nghiêng + tay quay + khung đỡ
- `bat-che-nang-mua`: trục cuốn + bạt thả + ròng rọc

Giữ mọi nét trong khung `16 ≤ x ≤ 224`, `16 ≤ y ≤ 164` để có lề.

- [ ] **Step 4: Chạy test, xác nhận pass**

Run: `python -m unittest tests.test_svg -v`
Expected: PASS, 6 tests

- [ ] **Step 5: Kiểm tra bằng mắt**

Tạo file tạm `scratch-svg.html` mở tất cả 8 hình cạnh nhau trên nền `#FBFAF8`, màu `#1E3446`, mỗi hình rộng 240px. Xác nhận: nét đều nhau, nhận ra được sản phẩm, không hình nào lệch tông. Xóa file tạm sau khi xem.

- [ ] **Step 6: Commit**

```bash
git add assets/svg tests/test_svg.py
git commit -m "feat: 8 hình vẽ nét sản phẩm thay ảnh stock sai chủ đề"
```

---

### Task 10: Build pipeline và trang chủ

Task đầu tiên sinh ra HTML thật. Sửa lỗi C1, C2, C3 (hotline mobile, sticky bar, Zalo) và mục §2.7 (header/footer inline).

**Files:**
- Create: `templates/_base.html`, `templates/_head.html`, `templates/_header.html`, `templates/_footer.html`, `templates/_sticky-bar.html`, `templates/index.html`
- Create: `scripts/build.py`
- Create: `tests/build_fixture.py`
- Create: `tests/test_build.py`
- Modify: `index.html` (trở thành output)
- Delete: `assets/js/include.js`, `partials/header.html`, `partials/footer.html`

**Interfaces:**
- Consumes: `scripts.sitedata`, `scripts.components`, `scripts.schema`, `scripts.template`
- Produces:
  - `scripts/build.py`: `build(root: str = ROOT) -> list[str]` (trả về đường dẫn đã ghi), `main() -> None`
  - `tests/build_fixture.py`: `ensure_built() -> None`, `read_output(relpath: str) -> str`

- [ ] **Step 1: Viết test thất bại**

Tạo `tests/build_fixture.py`:

```python
"""Chạy build đúng một lần cho cả bộ test."""
import functools

from scripts.build import ROOT, build


@functools.lru_cache(maxsize=1)
def ensure_built() -> tuple[str, ...]:
    return tuple(build(ROOT))


def read_output(relpath: str) -> str:
    import os

    ensure_built()
    with open(os.path.join(ROOT, relpath), encoding="utf-8") as handle:
        return handle.read()
```

Tạo `tests/test_build.py`:

```python
import os
import re
import unittest

from scripts.build import ROOT
from scripts.sitedata import load_site
from tests.build_fixture import ensure_built, read_output

SITE = load_site()


class TestBuildRuns(unittest.TestCase):
    def test_writes_expected_pages(self):
        written = {os.path.relpath(p, ROOT).replace("\\", "/") for p in ensure_built()}
        self.assertIn("index.html", written)

    def test_include_js_is_gone(self):
        self.assertFalse(os.path.exists(os.path.join(ROOT, "assets", "js", "include.js")))


class TestHomepageShell(unittest.TestCase):
    def setUp(self):
        self.html = read_output("index.html")

    def test_header_is_inlined_not_fetched(self):
        # Sửa §2.7: bản cũ nạp header bằng fetch nên Google không thấy.
        self.assertNotIn("data-include", self.html)
        self.assertIn('class="site-header"', self.html)
        self.assertIn("Trang chủ", self.html)

    def test_footer_is_inlined(self):
        self.assertIn('class="site-footer"', self.html)
        self.assertIn(SITE.business.email, self.html)

    def test_no_inline_style_attributes(self):
        # Ràng buộc toàn cục #1.
        self.assertEqual(re.findall(r'\sstyle="', self.html), [])

    def test_has_skip_link_to_main(self):
        self.assertIn('class="skip-link"', self.html)
        self.assertIn('id="main"', self.html)

    def test_declares_vietnamese_language(self):
        self.assertIn('<html lang="vi">', self.html)

    def test_loads_both_fonts(self):
        self.assertIn("Be+Vietnam+Pro", self.html)
        self.assertIn("Inter", self.html)


class TestHotlineAlwaysReachable(unittest.TestCase):
    """Sửa lỗi C1 + C3."""

    def setUp(self):
        self.html = read_output("index.html")

    def test_header_shows_phone_number_as_text(self):
        self.assertIn(SITE.business.phone_display, self.html)

    def test_tel_link_uses_e164(self):
        self.assertIn(f'href="tel:{SITE.business.phone}"', self.html)

    def test_zalo_link_present(self):
        self.assertIn(SITE.business.zalo_url, self.html)

    def test_sticky_bar_has_three_actions(self):
        self.assertIn('class="sticky-bar"', self.html)
        self.assertEqual(self.html.count("sticky-bar__action"), 3)


class TestHomepageSections(unittest.TestCase):
    """Thứ tự 8 khối theo spec §4.1."""

    def setUp(self):
        self.html = read_output("index.html")

    def test_hero_has_no_stock_photo(self):
        self.assertNotIn("hero-banner", self.html)

    def test_hero_uses_line_drawing(self):
        hero = self.html.split('class="hero"')[1].split("</section>")[0]
        self.assertIn("<svg", hero)

    def test_numeric_rail_present_with_five_facts(self):
        self.assertEqual(self.html.count('class="rail__item"'), 5)

    def test_decision_layer_offers_three_use_cases(self):
        # Sửa lỗi C6 — tầng quyết định đang thiếu hoàn toàn.
        self.assertIn("Chọn loại giàn phù hợp", self.html)
        self.assertEqual(self.html.count('class="card card--usecase"'), 3)

    def test_price_preview_shows_four_services_with_specs(self):
        self.assertEqual(self.html.count('class="card card--service"'), 4)
        self.assertEqual(self.html.count('class="spec-line"'), 4)

    def test_popular_badge_appears_once(self):
        self.assertEqual(self.html.count("Phổ biến nhất"), 1)

    def test_process_has_five_steps(self):
        self.assertEqual(self.html.count('class="stepper__num"'), 5)

    def test_trust_band_lists_service_areas(self):
        for area in SITE.areas:
            with self.subTest(area=area):
                self.assertIn(area, self.html)

    def test_shows_three_latest_posts(self):
        self.assertEqual(self.html.count('class="card card--post"'), 3)

    def test_prices_come_from_site_json(self):
        from scripts.sitedata import format_price

        featured = [s for s in SITE.services][:4]
        for service in featured:
            with self.subTest(service=service.slug):
                self.assertIn(format_price(service), self.html)


class TestHomepageSeo(unittest.TestCase):
    def setUp(self):
        self.html = read_output("index.html")

    def test_has_canonical(self):
        self.assertIn('rel="canonical"', self.html)

    def test_has_open_graph(self):
        for prop in ('property="og:title"', 'property="og:description"', 'property="og:image"'):
            with self.subTest(prop=prop):
                self.assertIn(prop, self.html)

    def test_has_local_business_jsonld(self):
        self.assertIn('type="application/ld+json"', self.html)
        self.assertIn("LocalBusiness", self.html)

    def test_exactly_one_h1(self):
        self.assertEqual(len(re.findall(r"<h1[\s>]", self.html)), 1)


class TestHomepageImages(unittest.TestCase):
    def test_every_img_has_explicit_dimensions(self):
        html = read_output("index.html")
        for tag in re.findall(r"<img[^>]*>", html):
            with self.subTest(tag=tag[:70]):
                self.assertIn("width=", tag)
                self.assertIn("height=", tag)

    def test_below_fold_images_are_lazy(self):
        html = read_output("index.html")
        tags = re.findall(r"<img[^>]*>", html)
        for tag in tags[1:]:
            with self.subTest(tag=tag[:70]):
                self.assertIn('loading="lazy"', tag)
```

- [ ] **Step 2: Chạy test, xác nhận thất bại**

Run: `python -m unittest tests.test_build -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'scripts.build'`

- [ ] **Step 3: Viết template**

`templates/_base.html` là khung chung; các trang cung cấp `{{{ main }}}`:

```html
<!DOCTYPE html>
<html lang="vi">
<head>
{{> _head }}
</head>
<body data-page="{{ page_id }}">
<a class="skip-link" href="#main">Bỏ qua, tới nội dung chính</a>
{{> _header }}
<main id="main">
{{{ main }}}
</main>
{{> _footer }}
{{> _sticky-bar }}
<script src="/assets/js/main.js" defer></script>
</body>
</html>
```

`templates/_head.html` nhận `title`, `description`, `canonical`, `og_image`, `jsonld`:

```html
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{ title }}</title>
<meta name="description" content="{{ description }}">
<link rel="canonical" href="{{ canonical }}">
<meta property="og:type" content="website">
<meta property="og:title" content="{{ title }}">
<meta property="og:description" content="{{ description }}">
<meta property="og:image" content="{{ og_image }}">
<meta property="og:locale" content="vi_VN">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/images/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="/assets/images/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@600;700;800&family=Inter:wght@400;500;600&display=swap">
<link rel="stylesheet" href="/assets/css/main.css">
{{{ jsonld }}}
```

`templates/_sticky-bar.html` — sửa C2 và C3:

```html
<nav class="sticky-bar" aria-label="Liên hệ nhanh">
  <a class="sticky-bar__action" href="tel:{{ phone }}">
    <span aria-hidden="true">{{{ icon_phone }}}</span><span>Gọi ngay</span>
  </a>
  <a class="sticky-bar__action" href="{{ zalo_url }}" target="_blank" rel="noopener">
    <span aria-hidden="true">{{{ icon_zalo }}}</span><span>Zalo</span>
  </a>
  <a class="sticky-bar__action sticky-bar__action--primary" href="/lien-he.html">
    <span aria-hidden="true">{{{ icon_quote }}}</span><span>Nhận báo giá</span>
  </a>
</nav>
```

Trong `_header.html`, hotline **không** được ẩn ở mobile — đây chính là lỗi C1:
```html
<a class="header__phone" href="tel:{{ phone }}">
  <span aria-hidden="true">{{{ icon_phone }}}</span>
  <span class="header__phone-number">{{ phone_display }}</span>
</a>
```
Ở CSS, chỉ được rút gọn cỡ chữ ở mobile, tuyệt đối không `display: none` trên `.header__phone-number`.

- [ ] **Step 4: Viết `scripts/build.py`**

```python
"""Sinh toàn bộ HTML tĩnh từ site.json + templates/."""
from __future__ import annotations

import os

from scripts import components, schema
from scripts.sitedata import ROOT, SiteData, load_site
from scripts.template import render_file

TEMPLATES = os.path.join(ROOT, "templates")


def _write(path: str, html: str) -> str:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(html)
    return path


def _shell(site: SiteData, **extra) -> dict:
    """Context mà mọi trang đều cần."""
    return {
        "phone": site.business.phone,
        "phone_display": site.business.phone_display,
        "zalo_url": site.business.zalo_url,
        "email": site.business.email,
        "business_name": site.business.name,
        "tagline": site.business.tagline,
        "icon_phone": components.icon("phone"),
        "icon_zalo": components.icon("zalo"),
        "icon_quote": components.icon("quote"),
        **extra,
    }


def build_home(site: SiteData) -> str:
    main = render_file(
        os.path.join(TEMPLATES, "index.html"),
        _shell(site, rail=components.numeric_rail(site.facts), ...),
        partials_dir=TEMPLATES,
    )
    html = render_file(
        os.path.join(TEMPLATES, "_base.html"),
        _shell(
            site,
            page_id="home",
            main=main,
            title=f"{site.business.name} | Lắp đặt chính hãng",
            description=site.business.tagline,
            canonical=f"{schema.BASE_URL}/",
            og_image=f"{schema.BASE_URL}/assets/images/logo.png",
            jsonld=schema.to_jsonld(schema.local_business(site)),
        ),
        partials_dir=TEMPLATES,
    )
    return _write(os.path.join(ROOT, "index.html"), html)


def build(root: str = ROOT) -> list[str]:
    site = load_site()
    return [build_home(site)]


def main() -> None:
    for path in build():
        print("wrote", os.path.relpath(path, ROOT))


if __name__ == "__main__":
    main()
```

Bổ sung `components.icon(name: str) -> str` trả về SVG inline cho `phone`, `zalo`, `quote` (nét 1.5px, `currentColor`, 20×20). Thêm test cho nó vào `tests/test_components.py`.

- [ ] **Step 5: Viết `templates/index.html`** theo đúng 8 khối của spec §4.1, thứ tự: hero → rail → 3 thẻ tình huống → bảng giá rút gọn 4 mục → stepper 5 bước → band tin cậy → 3 bài blog → CTA band.

- [ ] **Step 6: Chạy build và test**

```bash
python -m scripts.build
python -m unittest tests.test_build -v
```
Expected: PASS, 26 tests

- [ ] **Step 7: Xóa cơ chế include cũ**

```bash
git rm assets/js/include.js partials/header.html partials/footer.html
```

- [ ] **Step 8: Kiểm tra bằng mắt ở 4 breakpoint**

```bash
python -m http.server 8000
```
Mở `http://localhost:8000` và kiểm ở 375 / 768 / 1024 / 1440px:
- Hotline đọc được ở **mọi** bề rộng (đây là lỗi C1 đang sửa)
- Sticky bar chỉ hiện dưới 768px, không che nội dung cuối trang
- Không có scroll ngang
- Tab qua toàn trang, focus ring hổ phách luôn nhìn thấy

- [ ] **Step 9: Commit**

```bash
git add -A
git commit -m "feat: build pipeline + trang chủ mới, sticky bar, Zalo, header/footer inline"
```

---

### Task 11: Trang Dịch vụ, Giới thiệu, Khu vực phục vụ

Sửa lỗi C5 (link `tel:` trên thẻ dự án) và C6 (thiếu phân nhóm), và giải quyết vấn đề trung thực ở spec §2.2.

**Files:**
- Create: `templates/dich-vu.html`, `templates/gioi-thieu.html`, `templates/khu-vuc.html`
- Modify: `scripts/build.py` (thêm `build_services`, `build_about`, `build_areas`)
- Modify: `tests/test_build.py` (thêm class test mới)
- Delete: `du-an.html`

**Interfaces:**
- Consumes: `scripts.components` (`service_card`, `comparison_table`, `faq_list`, `stepper`, `area_list`), `scripts.schema` (`service_schema`, `faq_page`, `breadcrumb_list`)
- Produces: `build_services(site) -> str`, `build_about(site) -> str`, `build_areas(site) -> str`

- [ ] **Step 1: Viết test thất bại**

Thêm vào `tests/test_build.py`:

```python
class TestServicesPage(unittest.TestCase):
    def setUp(self):
        self.html = read_output("dich-vu.html")

    def test_all_eight_services_rendered(self):
        self.assertEqual(self.html.count('class="card card--service"'), 8)

    def test_grouped_into_the_three_categories(self):
        # Sửa lỗi C6.
        for group in ("Giàn phơi", "An toàn ban công", "Che chắn"):
            with self.subTest(group=group):
                self.assertIn(group, self.html)

    def test_each_service_anchor_is_reachable(self):
        for service in SITE.services:
            with self.subTest(service=service.slug):
                self.assertIn(f'id="{service.slug}"', self.html)

    def test_has_comparison_table_in_scroll_container(self):
        self.assertIn("table-scroll", self.html)
        self.assertIn("<table", self.html)

    def test_all_ten_faqs_live_here(self):
        self.assertEqual(self.html.count('class="faq__question"'), 10)

    def test_faq_page_schema_present(self):
        self.assertIn("FAQPage", self.html)

    def test_service_schema_for_every_service(self):
        self.assertEqual(self.html.count('"@type": "Service"'), 8)

    def test_no_inline_style(self):
        self.assertEqual(re.findall(r'\sstyle="', self.html), [])

    def test_breadcrumb_schema_present(self):
        self.assertIn("BreadcrumbList", self.html)


class TestAreasPage(unittest.TestCase):
    """Thay du-an.html — spec §4.6."""

    def setUp(self):
        self.html = read_output("khu-vuc.html")

    def test_old_projects_page_is_gone(self):
        self.assertFalse(os.path.exists(os.path.join(ROOT, "du-an.html")))

    def test_does_not_claim_stock_photos_are_completed_projects(self):
        # Spec §2.2 — đây là lý do trang cũ bị đổi mục đích.
        self.assertNotIn("Dự án đã thi công", self.html)
        for stock in ("projects/thu-duc.jpg", "projects/quan-1.jpg",
                      "projects/quan-7.jpg", "projects/thu-dau-mot.jpg"):
            with self.subTest(stock=stock):
                self.assertNotIn(stock, self.html)

    def test_no_tel_link_on_non_call_elements(self):
        # Sửa lỗi C5: thẻ dự án cũ link tới tel:.
        for tag in re.findall(r'<a[^>]*href="tel:[^"]*"[^>]*>', self.html):
            with self.subTest(tag=tag[:80]):
                self.assertNotIn("card--project", tag)

    def test_lists_every_service_area(self):
        for area in SITE.areas:
            with self.subTest(area=area):
                self.assertIn(area, self.html)

    def test_has_empty_project_grid_awaiting_real_photos(self):
        self.assertIn('class="project-grid"', self.html)
        self.assertIn("ảnh công trình thật", self.html.lower())


class TestAboutPage(unittest.TestCase):
    def setUp(self):
        self.html = read_output("gioi-thieu.html")

    def test_has_numeric_rail(self):
        self.assertEqual(self.html.count('class="rail__item"'), 5)

    def test_no_inline_style(self):
        self.assertEqual(re.findall(r'\sstyle="', self.html), [])

    def test_alt_text_describes_actual_image_content(self):
        # Spec §2.2: bản cũ ghi "kỹ thuật viên lắp đặt" cho ảnh thợ mộc dùng MacBook.
        self.assertNotIn("Kỹ thuật viên đang thao tác lắp đặt", self.html)
```

- [ ] **Step 2: Chạy test, xác nhận thất bại**

Run: `python -m unittest tests.test_build -v`
Expected: FAIL — `FileNotFoundError: dich-vu.html` (build chưa sinh)

- [ ] **Step 3: Viết ba template và ba hàm build**

`templates/dich-vu.html`: sub-nav neo dính ở đầu (`<nav aria-label="Nhóm dịch vụ">` với 3 link `#gian-phoi`, `#an-toan-ban-cong`, `#che-chan`), rồi ba `<section>` tương ứng, mỗi section render `service_card` cho các dịch vụ trong nhóm, tiếp theo là bảng so sánh, stepper 5 bước, và `faq_list(site.faqs)` đầy đủ 10 câu.

Năm bước quy trình lấy nguyên văn từ `dich-vu.html` cũ (Tiếp nhận yêu cầu → Khảo sát thực tế → Báo giá chi tiết → Thi công lắp đặt → Bảo hành & chăm sóc).

`templates/khu-vuc.html`: bản đồ nhúng, `area_list(site.areas)`, và grid rỗng kèm chú thích HTML hướng dẫn:
```html
<!-- Thả ảnh công trình thật vào đây. Mỗi mục:
     <figure class="card card--project">
       <img src="/assets/images/projects/<ten>.webp" alt="<mô tả đúng nội dung ảnh>"
            width="640" height="480" loading="lazy">
       <figcaption>Địa điểm · Hạng mục · Thời gian thi công</figcaption>
     </figure>
     Không dùng ảnh stock. Không gắn link tel: lên thẻ. -->
<div class="project-grid" data-empty="Chưa có ảnh công trình thật"></div>
```

`templates/gioi-thieu.html`: giữ nội dung văn bản hiện có, thêm numeric rail, bỏ mọi `style=`, viết lại alt text cho khớp ảnh thật (hoặc bỏ ảnh nếu không mô tả trung thực được).

- [ ] **Step 4: Chạy build và test**

```bash
python -m scripts.build && python -m unittest tests.test_build -v
```
Expected: PASS, 45 tests

- [ ] **Step 5: Xóa trang cũ và cập nhật liên kết**

```bash
git rm du-an.html
grep -rn "du-an.html" templates/ scripts/ site.json
```
Mọi kết quả grep phải được đổi sang `khu-vuc.html`. Chạy lại build và test.

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "feat: trang dịch vụ phân nhóm + bảng so sánh, khu vực phục vụ thay trang dự án"
```

---

### Task 12: Trang Liên hệ và form báo giá

Sửa lỗi C4 — dropdown lệch hoàn toàn với dịch vụ đang bán.

**Files:**
- Create: `templates/lien-he.html`
- Modify: `scripts/build.py` (thêm `build_contact`)
- Modify: `tests/test_build.py`

**Interfaces:**
- Consumes: `scripts.components` (`service_options`, `faq_list`)
- Produces: `build_contact(site) -> str`

- [ ] **Step 1: Viết test thất bại**

Thêm vào `tests/test_build.py`:

```python
class TestContactPage(unittest.TestCase):
    def setUp(self):
        self.html = read_output("lien-he.html")

    def test_dropdown_lists_the_eight_real_services(self):
        """Sửa lỗi C4: bản cũ chỉ liệt kê 4 loại cửa lưới."""
        for service in SITE.services:
            with self.subTest(service=service.slug):
                self.assertIn(f'value="{service.slug}"', self.html)

    def test_dropdown_has_no_orphan_cua_luoi_options(self):
        for dead in ("Cửa lưới xếp gọn", "Cửa lưới cố định", "Cửa lưới inox, nhôm cao cấp"):
            with self.subTest(option=dead):
                self.assertNotIn(dead, self.html)

    def test_form_has_exactly_four_fields(self):
        # Spec §4.3: Tên, SĐT, Khu vực, Dịch vụ.
        self.assertEqual(self.html.count('class="field"'), 4)

    def test_every_field_has_a_visible_label(self):
        labels = re.findall(r'<label[^>]*for="([^"]+)"', self.html)
        inputs = re.findall(r'<(?:input|select|textarea)[^>]*id="([^"]+)"', self.html)
        self.assertEqual(sorted(labels), sorted(inputs))

    def test_phone_field_uses_tel_input_mode(self):
        field = re.search(r'<input[^>]*id="phone"[^>]*>', self.html).group(0)
        self.assertIn('type="tel"', field)
        self.assertIn('inputmode="numeric"', field)

    def test_each_field_has_an_error_container(self):
        self.assertEqual(self.html.count('class="field__error"'), 4)

    def test_error_containers_are_live_regions(self):
        self.assertEqual(self.html.count('aria-live="polite"'), 4)

    def test_contact_channels_appear_before_the_form(self):
        # Spec §4.3: Zalo và hotline đặt phía trên form.
        self.assertLess(self.html.index("zalo.me"), self.html.index("<form"))

    def test_only_four_faqs_here(self):
        self.assertEqual(self.html.count('class="faq__question"'), 4)

    def test_links_to_full_faq_list(self):
        self.assertIn("/dich-vu.html#faq", self.html)

    def test_submission_is_marked_as_not_wired_up(self):
        # Spec §6: giữ giả lập, phải có TODO rõ ràng.
        js = read_output("assets/js/main.js")
        self.assertIn("TODO", js)

    def test_no_inline_style(self):
        self.assertEqual(re.findall(r'\sstyle="', self.html), [])
```

- [ ] **Step 2: Chạy test, xác nhận thất bại**

Run: `python -m unittest tests.test_build -v`
Expected: FAIL — `FileNotFoundError: lien-he.html`

- [ ] **Step 3: Viết `templates/lien-he.html`**

Thứ tự: page header → khối kênh liên hệ (hotline, Zalo, email, địa chỉ, giờ làm việc) → form 4 trường → bản đồ → 4 FAQ + link "Xem tất cả câu hỏi".

Mỗi trường theo mẫu:
```html
<div class="field">
  <label for="phone">Số điện thoại</label>
  <input type="tel" id="phone" name="phone" inputmode="numeric"
         autocomplete="tel" required aria-describedby="phone-error">
  <p class="field__error" id="phone-error" aria-live="polite"></p>
</div>
```

Trường dịch vụ dùng `{{{ service_options }}}` từ `components.service_options(site)`.

- [ ] **Step 4: Chạy build và test**

```bash
python -m scripts.build && python -m unittest tests.test_build -v
```
Expected: PASS — riêng `test_submission_is_marked_as_not_wired_up` vẫn đỏ vì `main.js` chưa viết lại (Task 14). Chấp nhận đỏ đúng một test này, ghi chú lại.

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "feat: trang liên hệ + form 4 trường khớp 8 dịch vụ thật (sửa C4)"
```

---

### Task 13: Trang blog và template bài viết

Sửa lỗi C7 — nguồn traffic chính không có đường chuyển đổi nào.

**Files:**
- Create: `templates/blog.html`, `templates/post.html`
- Modify: `scripts/build.py` (thêm `build_blog_index`, `build_posts`)
- Modify: `tests/test_build.py`
- Delete: `scripts/build_blog.py`

**Interfaces:**
- Consumes: `scripts.markdown` (`md_to_html`, `strip_front_matter`, `add_heading_anchors`), `scripts.components` (`post_card`, `spec_line`), `scripts.schema` (`blog_posting`)
- Produces: `build_blog_index(site) -> str`, `build_posts(site) -> list[str]`

- [ ] **Step 1: Viết test thất bại**

Thêm vào `tests/test_build.py`:

```python
class TestBlogIndex(unittest.TestCase):
    def setUp(self):
        self.html = read_output("blog.html")

    def test_lists_every_post(self):
        self.assertEqual(self.html.count('class="card card--post"'), 12)

    def test_has_category_filter_chips(self):
        self.assertEqual(self.html.count('class="chip"') + self.html.count('chip chip--active'), 4)

    def test_chips_are_real_buttons(self):
        chips = re.findall(r'<(\w+)[^>]*class="chip[^"]*"', self.html)
        self.assertTrue(all(tag == "button" for tag in chips), chips)


class TestBlogPost(unittest.TestCase):
    def setUp(self):
        self.html = read_output("blog/quan-1.html")

    def test_has_conversion_sidebar(self):
        # Sửa lỗi C7.
        self.assertIn('class="quote-aside"', self.html)
        self.assertIn(SITE.business.phone_display, self.html)

    def test_sidebar_links_to_a_related_service(self):
        aside = self.html.split('class="quote-aside"')[1].split("</aside>")[0]
        self.assertIn("/dich-vu.html#", aside)

    def test_has_table_of_contents(self):
        self.assertIn('class="toc"', self.html)

    def test_headings_have_anchor_ids(self):
        self.assertRegex(self.html, r'<h2 id="[a-z0-9-]+">')

    def test_has_blogposting_schema(self):
        self.assertIn("BlogPosting", self.html)

    def test_no_inline_style(self):
        # Bản cũ có style="max-width:760px" ngay trong PAGE_TMPL.
        self.assertEqual(re.findall(r'\sstyle="', self.html), [])

    def test_tables_are_wrapped_for_horizontal_scroll(self):
        if "<table" in self.html:
            self.assertIn("table-scroll", self.html)

    def test_cover_image_has_dimensions(self):
        cover = re.search(r'<img[^>]*class="[^"]*cover[^"]*"[^>]*>', self.html)
        self.assertIsNotNone(cover)
        self.assertIn("width=", cover.group(0))


class TestAllPostsBuild(unittest.TestCase):
    def test_every_post_file_exists(self):
        for post in SITE.posts:
            with self.subTest(post=post.slug):
                path = os.path.join(ROOT, "blog", f"{post.slug}.html")
                self.assertTrue(os.path.exists(path))

    def test_old_build_script_removed(self):
        self.assertFalse(os.path.exists(os.path.join(ROOT, "scripts", "build_blog.py")))
```

- [ ] **Step 2: Chạy test, xác nhận thất bại**

Run: `python -m unittest tests.test_build -v`
Expected: FAIL — `blog.html` chưa được build lại, `quote-aside` không tồn tại

- [ ] **Step 3: Viết template và hàm build**

`templates/blog.html`: hàng chip lọc (`Tất cả`, `Khu vực`, `Kiến thức`, `So sánh`) là `<button class="chip" data-filter="...">`, rồi grid 12 `post_card`.

`templates/post.html`: bố cục 2 cột trên desktop (`.article` + `<aside class="quote-aside">`). Sidebar chứa: hotline, nút Zalo, một `service_card` rút gọn của dịch vụ liên quan, và link "Nhận báo giá". Trên mobile sidebar rơi xuống sau bài, đồng thời chèn một khối CTA sau đoạn văn đầu tiên.

Trong `build_posts`, ánh xạ bài → dịch vụ liên quan bằng từ khóa trong slug: chứa `vach-lanh` → `vach-ngan-lanh`; chứa `mua-mua` → `bat-che-nang-mua`; còn lại → dịch vụ đang có `popular: true`.

Bọc mọi `<table>` do markdown sinh ra trong `<div class="table-scroll">` trước khi chèn vào template.

- [ ] **Step 4: Chạy build và test**

```bash
python -m scripts.build && python -m unittest tests.test_build -v
```
Expected: PASS

- [ ] **Step 5: Xóa script cũ**

```bash
git rm scripts/build_blog.py
python -m unittest discover -s tests -t . -v
```

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "feat: blog index có lọc chủ đề + bài viết có sidebar chuyển đổi (sửa C7)"
```

---

### Task 14: Viết lại JavaScript

**Files:**
- Modify: `assets/js/main.js` (thay thế hoàn toàn 56 dòng hiện có)
- Create: `tests/test_js.py`

**Interfaces:**
- Consumes: các class và thuộc tính ARIA do Task 8 và 10–13 sinh ra
- Produces: `assets/js/main.js` — vanilla, không dependency, chạy được với `defer`

- [ ] **Step 1: Viết test thất bại**

Tạo `tests/test_js.py`:

```python
import os
import re
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JS_PATH = os.path.join(ROOT, "assets", "js", "main.js")

with open(JS_PATH, encoding="utf-8") as handle:
    JS = handle.read()


class TestNoLegacyCode(unittest.TestCase):
    def test_include_loader_is_gone(self):
        self.assertNotIn("data-include", JS)
        self.assertNotIn("includes:loaded", JS)

    def test_faq_no_longer_uses_max_height_hack(self):
        self.assertNotIn("scrollHeight", JS)


class TestAccessibility(unittest.TestCase):
    def test_nav_toggle_updates_aria_expanded(self):
        self.assertIn("aria-expanded", JS)

    def test_faq_updates_aria_expanded(self):
        self.assertGreaterEqual(JS.count("aria-expanded"), 2)

    def test_escape_closes_mobile_nav(self):
        self.assertIn("Escape", JS)

    def test_respects_reduced_motion(self):
        self.assertIn("prefers-reduced-motion", JS)


class TestFeatures(unittest.TestCase):
    def test_has_sticky_bar_scroll_behaviour(self):
        self.assertIn("sticky-bar", JS)

    def test_has_chip_filtering(self):
        self.assertIn("data-filter", JS)

    def test_has_inline_form_validation(self):
        self.assertIn("field__error", JS)

    def test_form_submission_is_flagged_as_placeholder(self):
        self.assertIn("TODO", JS)
        self.assertRegex(JS, r"TODO[^\n]*(endpoint|backend|Formspree|Zalo)")

    def test_preselects_service_from_query_string(self):
        # Link "Nhận báo giá" trên card mang ?dich-vu=<slug>.
        self.assertIn("dich-vu", JS)


class TestRobustness(unittest.TestCase):
    def test_guards_every_query_selector_result(self):
        """Script chạy trên mọi trang — phần tử vắng mặt không được ném lỗi."""
        self.assertNotRegex(JS, r"querySelector\([^)]*\)\.\w+\s*=")

    def test_no_inline_event_handlers_needed(self):
        self.assertIn("addEventListener", JS)
```

- [ ] **Step 2: Chạy test, xác nhận thất bại**

Run: `python -m unittest tests.test_js -v`
Expected: FAIL — `main.js` cũ còn `includes:loaded` và `scrollHeight`

- [ ] **Step 3: Viết lại `assets/js/main.js`**

Năm module độc lập, mỗi module tự thoát nếu không tìm thấy phần tử của mình:

```javascript
// 1. initNav — toggle menu mobile
//    - Cập nhật aria-expanded trên .nav-toggle
//    - Đóng bằng phím Escape, trả focus về nút toggle
//    - Đóng khi click ra ngoài
//
// 2. initFaq — accordion
//    - Dùng aria-expanded trên button + thuộc tính hidden trên panel
//    - Mở/đóng bằng grid-template-rows: 0fr <-> 1fr, KHÔNG dùng scrollHeight
//    - Mở một mục thì đóng các mục khác cùng danh sách
//
// 3. initStickyBar
//    - Ẩn khi cuộn lên, hiện khi cuộn xuống, dùng transform (không dùng top)
//    - Bỏ qua hiệu ứng nếu prefers-reduced-motion: reduce
//
// 4. initChips — lọc bài blog
//    - Đọc data-filter, so với data-category trên .card--post
//    - Cập nhật aria-pressed trên chip
//
// 5. initQuoteForm
//    - Validation inline: lỗi ghi vào .field__error tương ứng (aria-live đã có sẵn)
//    - Đọc ?dich-vu=<slug> từ URL để chọn sẵn option trong dropdown
//    - TODO: form hiện chỉ giả lập thành công phía client.
//      Để nối backend thật, thay khối này bằng fetch() tới endpoint
//      (Formspree / Web3Forms) hoặc chuyển hướng sang Zalo với nội dung soạn sẵn.
```

Mỗi module bắt đầu bằng `const el = document.querySelector(...); if (!el) return;`.

- [ ] **Step 4: Chạy test, xác nhận pass**

```bash
python -m unittest tests.test_js tests.test_build -v
```
Expected: PASS — `test_submission_is_marked_as_not_wired_up` (Task 12) giờ chuyển xanh

- [ ] **Step 5: Kiểm tra tương tác bằng tay**

```bash
python -m http.server 8000
```
Xác nhận từng mục:
- Menu mobile: mở, đóng bằng Escape, focus quay lại nút toggle
- FAQ: mở/đóng bằng Enter và Space, screen reader đọc được trạng thái
- Sticky bar: ẩn/hiện theo hướng cuộn, không giật
- Chip blog: lọc đúng theo chủ đề
- Form: bỏ trống SĐT rồi submit → lỗi hiện ngay dưới trường, không phải ở đầu trang
- Vào `/lien-he.html?dich-vu=luoi-cap-ban-cong` → dropdown chọn sẵn đúng mục

- [ ] **Step 6: Commit**

```bash
git add assets/js/main.js tests/test_js.py
git commit -m "feat: viết lại JS — nav a11y, FAQ ARIA, sticky bar, lọc chip, validation"
```

---

### Task 15: Tối ưu ảnh và sửa alt text

Giải quyết spec §2.6 và phần còn lại của §2.2.

**Files:**
- Create: `scripts/images.py`
- Create: `tests/test_images.py`
- Modify: `scripts/build.py` (dùng `image_tag`)
- Move: ảnh gốc sang `assets/images/_src/`

**Interfaces:**
- Consumes: Pillow
- Produces:
  - `@dataclass(frozen=True) ImageInfo(path: str, width: int, height: int)`
  - `probe(path: str) -> ImageInfo`
  - `make_variants(src: str, out_dir: str, widths=(480, 960, 1440)) -> list[ImageInfo]`
  - `srcset_attr(variants: list[ImageInfo]) -> str`
  - `image_tag(src: str, alt: str, *, sizes: str, lazy: bool = True, variants: list[ImageInfo] | None = None) -> str`

- [ ] **Step 1: Viết test thất bại**

Tạo `tests/test_images.py`:

```python
import os
import unittest

from scripts.images import ImageInfo, image_tag, probe, srcset_attr

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(ROOT, "assets", "images")

MAX_BYTES = 200 * 1024


class TestProbe(unittest.TestCase):
    def test_returns_real_dimensions(self):
        info = probe(os.path.join(IMG_DIR, "logo.png"))
        self.assertGreater(info.width, 0)
        self.assertGreater(info.height, 0)


class TestSrcsetAttr(unittest.TestCase):
    def test_formats_width_descriptors(self):
        variants = [
            ImageInfo("/assets/images/x-480.webp", 480, 320),
            ImageInfo("/assets/images/x-960.webp", 960, 640),
        ]
        self.assertEqual(
            srcset_attr(variants),
            "/assets/images/x-480.webp 480w, /assets/images/x-960.webp 960w",
        )


class TestImageTag(unittest.TestCase):
    def test_always_emits_dimensions(self):
        tag = image_tag("/assets/images/logo.png", "Logo", sizes="40px")
        self.assertIn("width=", tag)
        self.assertIn("height=", tag)

    def test_lazy_by_default(self):
        tag = image_tag("/assets/images/logo.png", "Logo", sizes="40px")
        self.assertIn('loading="lazy"', tag)
        self.assertIn('decoding="async"', tag)

    def test_eager_when_requested(self):
        tag = image_tag("/assets/images/logo.png", "Logo", sizes="40px", lazy=False)
        self.assertNotIn("lazy", tag)

    def test_escapes_alt_text(self):
        tag = image_tag("/assets/images/logo.png", 'Giàn "A" & B', sizes="40px")
        self.assertIn("&quot;", tag)
        self.assertIn("&amp;", tag)

    def test_rejects_empty_alt_without_explicit_decorative_flag(self):
        with self.assertRaises(ValueError):
            image_tag("/assets/images/logo.png", "", sizes="40px")


class TestOptimisedAssets(unittest.TestCase):
    def test_no_shipped_image_exceeds_budget(self):
        oversized = []
        for dirpath, dirnames, filenames in os.walk(IMG_DIR):
            if "_src" in dirpath:
                continue
            for name in filenames:
                path = os.path.join(dirpath, name)
                if os.path.getsize(path) > MAX_BYTES:
                    oversized.append((os.path.relpath(path, ROOT), os.path.getsize(path)))
        self.assertEqual(oversized, [], f"Ảnh quá nặng: {oversized}")

    def test_originals_are_kept_out_of_the_shipped_tree(self):
        self.assertTrue(os.path.isdir(os.path.join(IMG_DIR, "_src")))


class TestAltTextHonesty(unittest.TestCase):
    """Spec §2.2 — alt text phải mô tả đúng nội dung ảnh."""

    FORBIDDEN = [
        "Khách hàng vui vẻ trên ban công căn hộ hiện đại tại Việt Nam",
        "Kỹ thuật viên đang thao tác lắp đặt, thi công thực tế",
        "Thủ Đức – Giàn phơi thông minh gắn tường",
        "Quận 7 – Giàn phơi điều khiển từ xa",
    ]

    def test_no_page_reuses_the_false_alt_text(self):
        import glob

        for path in glob.glob(os.path.join(ROOT, "*.html")) + glob.glob(
            os.path.join(ROOT, "blog", "*.html")
        ):
            html = open(path, encoding="utf-8").read()
            for phrase in self.FORBIDDEN:
                with self.subTest(page=os.path.basename(path), phrase=phrase[:30]):
                    self.assertNotIn(phrase, html)
```

- [ ] **Step 2: Chạy test, xác nhận thất bại**

Run: `python -m unittest tests.test_images -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'scripts.images'`

- [ ] **Step 3: Viết `scripts/images.py`**

```python
"""Tối ưu ảnh: WebP, srcset, kích thước tường minh."""
from __future__ import annotations

import os
from dataclasses import dataclass

from PIL import Image

from scripts.template import escape


@dataclass(frozen=True)
class ImageInfo:
    path: str
    width: int
    height: int


def probe(path: str) -> ImageInfo:
    with Image.open(path) as img:
        return ImageInfo(path, img.width, img.height)


def make_variants(src: str, out_dir: str, widths=(480, 960, 1440)) -> list[ImageInfo]:
    os.makedirs(out_dir, exist_ok=True)
    stem = os.path.splitext(os.path.basename(src))[0]
    out: list[ImageInfo] = []
    with Image.open(src) as img:
        img = img.convert("RGB")
        for width in widths:
            if width > img.width:
                continue
            height = round(img.height * width / img.width)
            resized = img.resize((width, height), Image.LANCZOS)
            path = os.path.join(out_dir, f"{stem}-{width}.webp")
            resized.save(path, "WEBP", quality=82, method=6)
            out.append(ImageInfo(path, width, height))
    return out


def srcset_attr(variants: list[ImageInfo]) -> str:
    return ", ".join(f"{v.path} {v.width}w" for v in variants)


def image_tag(src, alt, *, sizes, lazy=True, variants=None, decorative=False) -> str:
    if not alt and not decorative:
        raise ValueError(f"Ảnh {src!r} thiếu alt — truyền decorative=True nếu là ảnh trang trí")
    info = probe(src) if os.path.exists(src) else None
    dims = f' width="{info.width}" height="{info.height}"' if info else ""
    srcset = f' srcset="{srcset_attr(variants)}" sizes="{sizes}"' if variants else ""
    loading = ' loading="lazy" decoding="async"' if lazy else ""
    return f'<img src="{src}" alt="{escape(alt)}"{dims}{srcset}{loading}>'
```

- [ ] **Step 4: Chuyển ảnh gốc và sinh bản tối ưu**

```bash
mkdir -p assets/images/_src
git mv assets/images/hero-banner.jpg assets/images/_src/
git mv assets/images/about-thi-cong.jpg assets/images/_src/
git mv assets/images/nhan-vien-huong-dan.jpg assets/images/_src/
git mv assets/images/thi-cong.jpeg assets/images/_src/
git mv assets/images/services assets/images/_src/services
git mv assets/images/projects assets/images/_src/projects
python -c "
import glob, os
from scripts.images import make_variants
for src in glob.glob('assets/images/_src/**/*.*', recursive=True):
    out = os.path.dirname(src).replace('_src' + os.sep, '').replace('_src', 'assets/images')
    print(src, '->', make_variants(src, out))
"
```

Ảnh nào không còn dùng đến sau khi thay bằng hình vẽ nét thì để nguyên trong `_src/` — không ship.

- [ ] **Step 5: Viết lại alt text**

Rà mọi `alt=` trong `templates/`. Nguyên tắc: mô tả **thứ có trong ảnh**, không mô tả thứ mong muốn có. Ảnh nào không mô tả trung thực được thì bỏ khỏi trang.

- [ ] **Step 6: Chạy build và toàn bộ test**

```bash
python -m scripts.build && python -m unittest discover -s tests -t . -v
```
Expected: PASS

- [ ] **Step 7: Commit**

```bash
git add -A
git commit -m "feat: pipeline ảnh WebP + srcset, sửa alt text sai sự thật"
```

---

### Task 16: Sitemap, robots, và bộ test nghiệm thu

Task cuối: biến 11 tiêu chí nghiệm thu của spec §7 thành test tự động chạy trên output thật.

**Files:**
- Modify: `scripts/build.py` (thêm `build_sitemap`, `build_robots`)
- Create: `tests/test_acceptance.py`
- Create: `README.md` (viết lại phần hướng dẫn build)

**Interfaces:**
- Consumes: toàn bộ pipeline
- Produces: `sitemap.xml`, `robots.txt`

- [ ] **Step 1: Viết test nghiệm thu**

Tạo `tests/test_acceptance.py` — mỗi test ánh xạ trực tiếp một tiêu chí ở spec §7:

```python
"""Tiêu chí nghiệm thu — spec §7. Mỗi test là một dòng trong bảng."""
import glob
import os
import re
import unittest

from scripts.build import ROOT
from scripts.sitedata import load_site
from tests.build_fixture import ensure_built

SITE = load_site()


def all_pages() -> list[str]:
    ensure_built()
    return sorted(
        glob.glob(os.path.join(ROOT, "*.html"))
        + glob.glob(os.path.join(ROOT, "blog", "*.html"))
    )


def read(path: str) -> str:
    with open(path, encoding="utf-8") as handle:
        return handle.read()


class Criterion01NoInlineStyle(unittest.TestCase):
    def test_no_style_attribute_anywhere(self):
        for path in all_pages():
            with self.subTest(page=os.path.basename(path)):
                self.assertEqual(re.findall(r'\sstyle="', read(path)), [])


class Criterion02Contrast(unittest.TestCase):
    """Đã phủ đầy đủ ở tests/test_css.py::TestContrastOfRealTokens."""

    def test_delegates_to_css_suite(self):
        from tests.test_css import TestContrastOfRealTokens

        suite = unittest.TestLoader().loadTestsFromTestCase(TestContrastOfRealTokens)
        result = unittest.TextTestRunner(verbosity=0).run(suite)
        self.assertTrue(result.wasSuccessful())


class Criterion03ContactReachable(unittest.TestCase):
    def test_every_page_exposes_phone_and_zalo(self):
        for path in all_pages():
            html = read(path)
            with self.subTest(page=os.path.basename(path)):
                self.assertIn(SITE.business.phone_display, html)
                self.assertIn(SITE.business.zalo_url, html)

    def test_no_css_rule_hides_the_header_phone_number(self):
        css = read(os.path.join(ROOT, "assets", "css", "main.css"))
        blocks = re.findall(r"\.header__phone-number[^{]*\{([^}]*)\}", css)
        for block in blocks:
            with self.subTest(block=block[:60]):
                self.assertNotIn("display: none", block.replace("display:none", "display: none"))


class Criterion04ServiceDropdown(unittest.TestCase):
    def test_contact_form_lists_all_eight_services(self):
        html = read(os.path.join(ROOT, "lien-he.html"))
        for service in SITE.services:
            with self.subTest(service=service.slug):
                self.assertIn(f'value="{service.slug}"', html)


class Criterion05NoJsRequiredForShell(unittest.TestCase):
    def test_header_footer_jsonld_present_without_javascript(self):
        for path in all_pages():
            html = read(path)
            with self.subTest(page=os.path.basename(path)):
                self.assertIn('class="site-header"', html)
                self.assertIn('class="site-footer"', html)
                self.assertIn('type="application/ld+json"', html)
                self.assertNotIn("data-include", html)


class Criterion06ImageDimensions(unittest.TestCase):
    def test_every_img_declares_width_and_height(self):
        for path in all_pages():
            for tag in re.findall(r"<img[^>]*>", read(path)):
                with self.subTest(page=os.path.basename(path), tag=tag[:60]):
                    self.assertIn("width=", tag)
                    self.assertIn("height=", tag)


class Criterion07NoThreePixelAccents(unittest.TestCase):
    def test_css_has_no_three_pixel_borders(self):
        css = read(os.path.join(ROOT, "assets", "css", "main.css"))
        self.assertEqual(re.findall(r"border[a-z-]*:\s*3px", css), [])


class Criterion08KeyboardNavigable(unittest.TestCase):
    def test_focus_visible_defined(self):
        css = read(os.path.join(ROOT, "assets", "css", "main.css"))
        self.assertIn(":focus-visible", css)

    def test_no_outline_none_without_replacement(self):
        css = read(os.path.join(ROOT, "assets", "css", "main.css"))
        for block in re.findall(r"\{[^{}]*outline:\s*none[^{}]*\}", css):
            with self.subTest(block=block[:60]):
                self.assertIn("box-shadow", block, "outline: none mà không thay bằng gì khác")

    def test_interactive_elements_are_not_divs(self):
        for path in all_pages():
            html = read(path)
            with self.subTest(page=os.path.basename(path)):
                self.assertEqual(re.findall(r'<div[^>]*onclick', html), [])


class Criterion09NoHorizontalScroll(unittest.TestCase):
    def test_no_element_forces_width_beyond_viewport(self):
        css = read(os.path.join(ROOT, "assets", "css", "main.css"))
        self.assertEqual(re.findall(r"width:\s*\d{4,}px", css), [])

    def test_wide_content_is_wrapped_in_scroll_containers(self):
        for path in all_pages():
            html = read(path)
            if "<table" in html:
                with self.subTest(page=os.path.basename(path)):
                    self.assertIn("table-scroll", html)


class Criterion10TelLinksOnlyOnCallActions(unittest.TestCase):
    def test_tel_href_only_on_explicit_call_elements(self):
        allowed = ("header__phone", "sticky-bar__action", "contact-row",
                   "footer", "quote-aside", "btn")
        for path in all_pages():
            for tag in re.findall(r'<a[^>]*href="tel:[^"]*"[^>]*>', read(path)):
                with self.subTest(page=os.path.basename(path), tag=tag[:80]):
                    self.assertTrue(
                        any(marker in tag for marker in allowed),
                        f"tel: gắn trên phần tử không phải hành động gọi: {tag}",
                    )


class Criterion11NoFakeProjectClaims(unittest.TestCase):
    def test_no_page_labels_stock_photos_as_completed_work(self):
        for path in all_pages():
            html = read(path)
            with self.subTest(page=os.path.basename(path)):
                self.assertNotIn("Dự án đã thi công", html)


class TestSitemapAndRobots(unittest.TestCase):
    def test_sitemap_lists_every_page(self):
        ensure_built()
        sitemap = read(os.path.join(ROOT, "sitemap.xml"))
        for path in all_pages():
            rel = os.path.relpath(path, ROOT).replace("\\", "/")
            with self.subTest(page=rel):
                self.assertIn(rel, sitemap)

    def test_robots_points_at_sitemap(self):
        ensure_built()
        robots = read(os.path.join(ROOT, "robots.txt"))
        self.assertIn("Sitemap:", robots)
        self.assertIn("sitemap.xml", robots)
```

- [ ] **Step 2: Chạy test, xác nhận thất bại**

Run: `python -m unittest tests.test_acceptance -v`
Expected: FAIL — `sitemap.xml` và `robots.txt` chưa tồn tại; một vài tiêu chí có thể đỏ

- [ ] **Step 3: Thêm `build_sitemap` và `build_robots` vào `scripts/build.py`**

`sitemap.xml`: một `<url>` cho mỗi trang, `<lastmod>` lấy từ `Post.iso_date` với bài blog và ngày build với trang tĩnh.
`robots.txt`: `User-agent: *`, `Allow: /`, `Sitemap: {BASE_URL}/sitemap.xml`.

- [ ] **Step 4: Sửa mọi tiêu chí còn đỏ**

Chạy `python -m unittest tests.test_acceptance -v`, sửa từng lỗi cho tới khi xanh hết. Đây là lưới an toàn cho toàn bộ 15 task trước.

- [ ] **Step 5: Chạy toàn bộ bộ test**

```bash
python -m scripts.build
python -m unittest discover -s tests -t . -v
```
Expected: PASS toàn bộ. Ghi lại số test cuối cùng.

- [ ] **Step 6: Viết lại `README.md`**

Nội dung bắt buộc: cách build (`python -m scripts.build`), cách chạy test, giải thích `site.json` là nguồn dữ liệu duy nhất, và ghi rõ form báo giá hiện chỉ giả lập kèm hướng dẫn nối endpoint thật.

- [ ] **Step 7: Kiểm tra lần cuối trên trình duyệt**

```bash
python -m http.server 8000
```
Đi hết 6 trang chính + 1 bài blog ở 375px và 1440px. Kiểm: không scroll ngang, hotline luôn thấy, sticky bar hoạt động, tab qua toàn site thấy focus ring, DevTools Console không lỗi.

- [ ] **Step 8: Commit**

```bash
git add -A
git commit -m "feat: sitemap, robots, bộ test nghiệm thu 11 tiêu chí spec §7"
```

---

## Self-Review

**Phủ spec:**

| Mục spec | Task |
|---|---|
| §2.1 C1 hotline mobile | 10 (`TestHotlineAlwaysReachable`), 16 (`Criterion03`) |
| §2.1 C2 sticky bar | 8 (CSS), 10 (markup), 14 (JS) |
| §2.1 C3 Zalo | 10, 16 |
| §2.1 C4 dropdown lệch | 5 (`service_options`), 12, 16 (`Criterion04`) |
| §2.1 C5 `tel:` trên thẻ dự án | 11, 16 (`Criterion10`) |
| §2.1 C6 tầng quyết định | 10 (3 thẻ tình huống), 11 (phân nhóm) |
| §2.1 C7 blog không chuyển đổi | 13 (`quote-aside`) |
| §2.2 ảnh stock + alt sai | 9 (hình vẽ nét), 11 (trang khu vực), 15 (alt text) |
| §2.3 hệ thống thị giác | 7, 8 |
| §2.4 tương phản | 1, 7 (`TestContrastOfRealTokens`) |
| §2.5 accessibility | 7, 8, 14, 16 (`Criterion08`) |
| §2.6 hiệu năng | 15 |
| §2.7 SEO | 6, 10, 16 |
| §3.3 token màu | 7 |
| §3.4 chữ | 7 |
| §3.5 không gian, bo góc | 7 |
| §3.6 bốn yếu tố nhận diện | 5 (spec-line, rail, stepper), 8 (gạch chân), 9 (hình vẽ nét) |
| §3.7 chuyển động | 8 (`test_transitions_use_only_the_two_durations`) |
| §4.1 trang chủ | 10 |
| §4.2 dịch vụ | 11 |
| §4.3 liên hệ | 12 |
| §4.4 blog | 13 |
| §4.5 giới thiệu | 11 |
| §4.6 dự án → khu vực | 11 |
| §4.7 mobile | 8, 10, 14 |
| §5.1 build | 2, 4, 10 |
| §5.2 CSS `@layer` | 7, 8 |
| §5.3 JavaScript | 14 |
| §5.4 SEO/schema | 6, 16 |
| §5.5 ảnh | 15 |
| §5.6 a11y | 7, 8, 14 |
| §7 cả 11 tiêu chí | 16 |

Không có mục spec nào thiếu task.

**Ghi chú nhất quán đã kiểm:**
- `load_site()` trả `SiteData` ở Task 2, mọi task sau dùng đúng tên trường đó.
- `service_card(service, *, svg_inline)` định nghĩa ở Task 5, gọi đúng chữ ký ở Task 10 và 11.
- `components.icon(name)` được thêm ở Task 10 — đã ghi rõ phải bổ sung test vào `tests/test_components.py` trong cùng task.
- `ensure_built()` / `read_output()` định nghĩa ở Task 10, dùng lại ở Task 11–13 và 16.
- Đường dẫn `du-an.html` bị xóa ở Task 11; Task 16 kiểm mọi tham chiếu còn sót qua sitemap.

**Một điểm chấp nhận đỏ tạm thời:** `test_submission_is_marked_as_not_wired_up` được viết ở Task 12 nhưng chỉ xanh sau Task 14. Đã ghi rõ trong Step 4 của Task 12 để người thực thi không tưởng nhầm là lỗi.
