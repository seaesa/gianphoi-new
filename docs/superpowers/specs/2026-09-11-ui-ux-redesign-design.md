# Thiết kế lại UI/UX — "Thép & Nắng"

Ngày: 2026-09-11
Dự án: gianphoi-new — site lắp đặt & sửa chữa giàn phơi thông minh, TP.HCM & Bình Dương
Trạng thái: spec đã chốt, chờ viết implementation plan

---

## 1. Bối cảnh

Site tĩnh gồm 6 trang chính (`index`, `gioi-thieu`, `dich-vu`, `du-an`, `blog`, `lien-he`) và 12 bài blog nhắm từ khóa local SEO. Mô hình kinh doanh là lead-gen: doanh thu đến từ cuộc gọi hotline và tin nhắn Zalo, không có giỏ hàng hay thanh toán online.

Toàn bộ CSS nằm trong `assets/css/main.css` (419 dòng). Header/footer nạp runtime bằng `fetch` trong `assets/js/include.js`.

## 2. Vấn đề đã xác định

### 2.1 Kiến trúc chuyển đổi

| # | Vấn đề | Vị trí | Mức độ |
|---|---|---|---|
| C1 | `.header-phone span { display: none }` ở breakpoint 768px ẩn toàn bộ hotline trên mobile (cả icon lẫn số) | `main.css` §Responsive | Nghiêm trọng |
| C2 | Không có sticky action bar trên mobile | toàn site | Nghiêm trọng |
| C3 | Không có nút Zalo ở bất kỳ đâu, dù `assets/images/icon-zalo.png` đã tồn tại | toàn site | Nghiêm trọng |
| C4 | Dropdown "Loại cửa lưới cần báo giá" chỉ có 4 loại cửa lưới, lệch hoàn toàn với 8 dịch vụ đang bán | `lien-he.html` | Nghiêm trọng |
| C5 | Thẻ dự án link tới `tel:` — bấm xem ảnh thì máy gọi điện | `du-an.html` | Cao |
| C6 | Không có tầng quyết định: 8 dịch vụ dàn hàng ngang giống hệt nhau, khách không biết chọn gì | `dich-vu.html`, `index.html` | Cao |
| C7 | Bài blog (nguồn traffic chính) không có CTA, sidebar hay khối báo giá | `blog/*.html` | Cao |

### 2.2 Tính trung thực của nội dung

Toàn bộ thư viện ảnh là stock sai chủ đề, alt text mô tả nội dung không có trong ảnh:

| File | Alt text hiện tại | Nội dung ảnh thật |
|---|---|---|
| `hero-banner.jpg` | "Khách hàng vui vẻ trên ban công căn hộ hiện đại tại Việt Nam" | Phố cổ châu Âu, quần áo vắt trên lan can sắt uốn |
| `services/gian-phoi-dieu-khien.jpeg` | "Giàn Phơi Thông Minh Điều Khiển" | Cây treo đồ với móc gỗ trắng |
| `projects/thu-duc.jpg` | "Thủ Đức – Giàn phơi thông minh gắn tường" | Ảnh trắng đen chung cư phương Tây |
| `about-thi-cong.jpg` | "Kỹ thuật viên đang thao tác lắp đặt, thi công thực tế" | Thợ mộc phương Tây dùng MacBook trong xưởng gỗ |

Nghiêm trọng nhất: `du-an.html` gắn ảnh stock nước ngoài dưới nhãn "Dự án đã thi công · Thủ Đức · 2 ngày" — đây là tuyên bố thương mại sai sự thật.

**Quyết định**: không dựng lại trang Dự án với ảnh giả. Thiết kế thay bằng hình vẽ nét (SVG line-drawing) cho grid dịch vụ và hero; trang Dự án chuyển thành "Khu vực phục vụ" có sẵn slot markup để thả ảnh công trình thật vào sau.

### 2.3 Hệ thống thị giác

- `--radius-lg: 4px` nhỏ hơn `--radius-md: 12px` — token đặt tên sai, đang dùng làm bo góc section.
- Hàng chục thuộc tính `style="..."` inline ghi đè token (font-size, màu, grid-template) → không còn nguồn chân lý duy nhất.
- Năm kiểu viền nhấn 3px khác nhau xuất hiện trên cùng một trang: viền trên card, viền trái FAQ, viền trái CTA band, viền trên footer, viền dưới header.
- `.btn-outline` mặc định dùng `border-color: rgba(255,255,255,0.55)` → vô hình trên nền sáng.
- `.bg-alt` đặt bên trong `.container` kèm bo góc → các section trông như panel trôi nổi thay vì một trang được thiết kế liền mạch.
- `grid-4` → 1 cột ở 768px: 8 card dịch vụ thành một cột dọc rất dài trên mobile.

### 2.4 Tương phản (đã đo)

| Cặp màu | Tỷ lệ | Kết luận |
|---|---|---|
| Trắng trên `--color-accent` `#C5652B` (nút CTA chính) | 3.98:1 | **Fail** WCAG AA 4.5:1 |
| `--color-muted` `#667585` trên `--color-surface-alt` `#ECEFF3` | 4.09:1 | **Fail** cho chữ thường |
| `--color-muted` `#667585` trên trắng | 4.72:1 | Pass (sát ngưỡng) |

### 2.5 Accessibility

- Không có `:focus-visible` ở bất kỳ đâu trong `main.css`.
- `.nav-toggle` thiếu `aria-expanded`; menu mobile không quản lý focus.
- FAQ dùng `div` + `button` thiếu `aria-expanded` / `aria-controls`.
- Không có khối `prefers-reduced-motion`.

### 2.6 Hiệu năng

- Ảnh không có `width`/`height` → CLS.
- Không `loading="lazy"`, không `srcset`.
- `services/bat-che-nang-mua.png` 1.78 MB; `hero-banner.jpg` 471 KB.

### 2.7 SEO

- Header/footer nạp bằng `fetch` → không có trong HTML gốc.
- Không có structured data: thiếu `LocalBusiness`, `Service`, `FAQPage`, `BreadcrumbList`, `BlogPosting`.
- Không có canonical, không có Open Graph.

Với một site mà toàn bộ chiến lược nội dung là 12 bài từ khóa local, đây là điểm chí mạng.

---

## 3. Hướng thiết kế: "Thép & Nắng"

### 3.1 Ý tưởng cốt lõi

Sản phẩm là một cơ cấu cơ khí: inox 304, tải trọng 70kg, tay quay hoặc remote, bảo hành 5 năm. Bán cơ cấu bằng **số liệu và bản vẽ**, không bằng ảnh.

Site đọc như catalogue kỹ thuật của một nhà thầu nghiêm túc: chữ chuẩn xác, bảng thông số, hình vẽ nét từng loại giàn, số liệu ở khắp nơi, bề mặt rất tĩnh, một sắc ấm duy nhất dành riêng cho hành động.

Hướng này vừa giải quyết ràng buộc thiếu ảnh thật, vừa tạo khác biệt thực: các site giàn phơi cùng ngành đều là collage ảnh cộng banner đỏ; không ai làm kiểu catalogue kỹ thuật.

### 3.2 Nguyên tắc

1. Nhấn mạnh đến từ cỡ chữ, độ đậm và khoảng trắng — không đến từ thanh màu.
2. Mọi đường kẻ là hairline 1px. Không có viền 3px nào tồn tại.
3. Hổ phách chỉ dùng cho hành động và số liệu. Không dùng làm trang trí.
4. Mọi con số đều là số thật lấy từ nội dung hiện có; không bịa thêm số liệu.
5. Không có `style=` inline trong HTML.

### 3.3 Token màu

```css
--ink:          #0F1C26;  /* chữ chính */
--ink-soft:     #33506A;  /* chữ phụ trên nền sáng */
--muted:        #5A6873;  /* chữ mờ */
--steel:        #1E3446;  /* header, footer, band đậm */
--steel-deep:   #162836;  /* band đậm hơn */
--paper:        #FBFAF8;  /* nền trang — ngà ấm */
--surface:      #FFFFFF;  /* card */
--hairline:     #E3E0DA;
--amber:        #B4530A;  /* nút CTA, link, focus ring */
--amber-bright: #E07A1F;  /* số lớn / icon trên nền navy — chỉ ≥24px bold */
--amber-tint:   #FDF1E3;
--amber-ink:    #8A3D06;
```

Tương phản đã đo:

| Cặp | Tỷ lệ | Kết luận |
|---|---|---|
| `--ink` trên `--paper` | 16.58:1 | Pass |
| `--muted` trên `--paper` | 5.50:1 | Pass |
| `--muted` trên `--surface` | 5.73:1 | Pass |
| Trắng trên `--amber` (nút CTA) | 5.02:1 | Pass |
| Trắng trên `--steel` | 12.85:1 | Pass |
| `--amber` trên `--paper` (link, focus ring) | 4.81:1 | Pass |
| `--ink-soft` trên `--paper` | 8.06:1 | Pass |
| `--amber-ink` trên `--amber-tint` (badge) | 6.86:1 | Pass |
| `--amber-bright` trên `--steel` | 4.27:1 | **Chỉ dùng cho chữ ≥24px bold** |

Nền ngà ấm `#FBFAF8` thay cho xám lạnh `#f4f6f8` hiện tại: làm navy đọc ra sang trọng thay vì công sở.

### 3.4 Chữ

- **Display — Be Vietnam Pro** 600/700/800. Thiết kế riêng cho dấu tiếng Việt; Plus Jakarta Sans hiện tại bị dấu đè vào chiều cao chữ ở heading lớn.
- **Body — Inter** 400/500/600. Giữ lại; tiếng Việt tốt, đọc tốt ở cỡ nhỏ.
- Bảng giá và bảng thông số: `font-variant-numeric: tabular-nums`.

Thang cỡ chữ fluid (`clamp`), ratio ~1.25:

```
--fs-xs:   0.8125rem   /* 13px — nhãn, eyebrow */
--fs-sm:   0.875rem    /* 14px — meta, caption */
--fs-base: 1rem        /* 16px — thân bài */
--fs-md:   1.125rem    /* 18px — lead */
--fs-lg:   clamp(1.25rem, 1.6vw, 1.375rem)
--fs-xl:   clamp(1.5rem, 2.2vw, 1.75rem)
--fs-2xl:  clamp(1.875rem, 3vw, 2.25rem)
--fs-3xl:  clamp(2.25rem, 4vw, 3rem)
--fs-4xl:  clamp(2.75rem, 5.5vw, 3.75rem)   /* hero h1 */
```

`line-height`: 1.15 cho display, 1.65 cho thân bài (tiếng Việt có dấu cần nhiều hơn tiếng Anh).

### 3.5 Không gian & hình khối

```css
--space-1: 4px;   --space-2: 8px;   --space-3: 12px;  --space-4: 16px;
--space-5: 24px;  --space-6: 32px;  --space-7: 48px;  --space-8: 64px;
--space-9: 96px;  --space-10: 128px;

--r-sm:   6px;    /* input, nút */
--r:      10px;   /* card */
--r-pill: 999px;  /* badge */

--container: 1200px;
--gutter: 24px;
```

Chỉ ba token bo góc. Bỏ hoàn toàn cặp `--radius-md`/`--radius-lg` đang mâu thuẫn.

Đổ bóng: đúng hai mức — `--shadow-raised` cho card hover và dropdown, `--shadow-bar` cho sticky bar. Trạng thái nghỉ không có bóng.

Band toàn chiều rộng (`.band`, `.band--paper`, `.band--steel`) trải từ mép này sang mép kia, chứa `.container` bên trong. Thay cho `.bg-alt` bo góc đang trôi nổi.

### 3.6 Bốn yếu tố nhận diện

**1. Spec-line** — khối 3 dòng gắn vào mỗi card dịch vụ:

```
Chất liệu     Inox 304
Tải trọng     70 kg
Bảo hành      5 năm
```

Phân cách bằng hairline, số căn cột bằng `tabular-nums`. Đây là chữ ký thị giác của hệ thống; lặp lại ở card dịch vụ, bảng so sánh, và khối CTA trong bài blog.

**2. Hình vẽ nét sản phẩm** — SVG line-drawing từng loại (treo trần, xếp tường, điều khiển, lưới cáp, cửa lưới, vách lạnh, mái hiên, bạt che), nét 1.5px `--steel` trên nền `--paper`, kèm nhãn chú thích. Thay hoàn toàn ảnh stock sai trong grid dịch vụ. Vẽ tay bằng SVG thuần, không dùng thư viện icon.

**3. Numeric rail** — dải số liệu ngăn bằng hairline, số đặt cỡ `--fs-3xl` màu `--amber-bright` trên nền `--steel`:

```
10+ năm | 1000+ công trình | 70 kg tải trọng | 5 năm bảo hành | 24h phản hồi
```

**4. Gạch chân hổ phách** — nav active và link trong bài dùng gạch 2px mọc từ trái khi hover (`transform: scaleX()`, `transform-origin: left`). Đây là thứ trang trí duy nhất trong hệ thống.

### 3.7 Chuyển động

- Chỉ hai thời lượng: 150ms cho phản hồi tức thì (màu, opacity), 250ms cho chuyển vị (transform).
- Easing: `cubic-bezier(0.2, 0, 0, 1)`.
- Chỉ animate `transform` và `opacity`.
- Toàn bộ nằm trong `@media (prefers-reduced-motion: no-preference)`; mặc định là tĩnh.

---

## 4. Kiến trúc trang

### 4.1 Trang chủ

1. **Hero** chia đôi. Trái: `h1` + một câu cam kết + hai CTA (Gọi ngay / Nhận báo giá) + dòng tin cậy "Chính hãng Hòa Phát · Bảo hành 5 năm · Khảo sát miễn phí". Phải: hình vẽ nét giàn phơi có chú thích kích thước. Bỏ ảnh phố châu Âu.
2. **Numeric rail** — 5 số liệu.
3. **"Chọn loại giàn phù hợp với bạn"** — 3 thẻ theo tình huống sử dụng: Ban công chung cư nhỏ / Sân thượng nhà phố / Muốn điều khiển tự động. Mỗi thẻ dẫn tới đúng mục trong trang Dịch vụ. Đây là tầng quyết định hiện đang thiếu hoàn toàn (C6).
4. **Bảng giá rút gọn** — 4 dịch vụ có spec-line, đánh dấu "Phổ biến nhất" trên một mục.
5. **Quy trình 5 bước** — stepper ngang nối bằng hairline; mobile chuyển thành dọc.
6. **Band tin cậy** (nền `--steel`) — đánh giá khách hàng, badge bảo hành, danh sách khu vực phục vụ.
7. **Blog** — 3 bài mới nhất.
8. **CTA band**.

### 4.2 Dịch vụ & Bảng giá

- Chia 8 dịch vụ thành 3 nhóm, mỗi nhóm có anchor trong sub-nav dính:
  - **Giàn phơi**: điều khiển, treo trần, xếp tường
  - **An toàn ban công**: lưới cáp, cửa lưới chống muỗi
  - **Che chắn**: vách ngăn lạnh, mái hiên, bạt che nắng mưa
- Mỗi mục: hình vẽ nét + tên + khoảng giá + spec-line + nút "Nhận báo giá".
- **Bảng so sánh "Giàn nào hợp với bạn"** — các cột: loại, không gian phù hợp, tải trọng, cách vận hành, giá, bảo hành.
- Quy trình 5 bước.
- FAQ: toàn bộ 10 câu chuyển từ `lien-he.html` sang đây (đây cũng là nơi gắn schema `FAQPage`). Trang Liên hệ giữ lại 4 câu liên quan trực tiếp đến đặt lịch và báo giá, kèm link "Xem tất cả câu hỏi".

### 4.3 Liên hệ

- Zalo và hotline đặt **phía trên** form.
- Form rút còn 4 trường: Tên · Số điện thoại · Khu vực · Dịch vụ quan tâm.
- Dropdown dịch vụ lấy đúng 8 dịch vụ thật, sinh từ `site.json` (sửa C4).
- Validation inline, thông báo lỗi đặt cạnh trường.
- Bản đồ, thông tin liên hệ, khung giờ làm việc.
- Submit: **giữ giả lập client-side như hiện tại**, đánh dấu `TODO` rõ ràng trong `main.js` kèm ghi chú cách nối endpoint thật sau.

### 4.4 Blog

- Trang index: chip lọc chủ đề (Khu vực / Kiến thức / So sánh), card có spec-line rút gọn.
- Trang bài viết: bố cục 2 cột trên desktop, sidebar dính gồm form báo giá mini + card dịch vụ liên quan + hotline (sửa C7). Mobile: khối CTA chèn sau đoạn đầu và ở cuối bài.
- Mục lục tự động cho bài dài.

### 4.5 Giới thiệu

Giữ nội dung hiện có, dựng lại theo hệ thống mới: câu chuyện, cam kết, numeric rail, khu vực phục vụ.

### 4.6 Dự án → Khu vực phục vụ

Đổi mục đích trang. Nội dung: bản đồ khu vực, danh sách quận/huyện đã phục vụ, và một grid `.project-grid` có sẵn markup nhưng rỗng, kèm ghi chú trong HTML hướng dẫn thả ảnh công trình thật vào. Không hiển thị ảnh stock kèm nhãn "đã thi công".

Link `tel:` trên thẻ dự án bị loại bỏ (sửa C5).

### 4.7 Mobile

- **Sticky action bar** dưới màn hình: Gọi · Zalo · Báo giá. Ẩn khi cuộn lên, hiện khi cuộn xuống (sửa C2, C3).
- Hotline **luôn hiện** trong header (sửa C1).
- Mọi target ≥44px, khoảng cách ≥8px.
- Grid giá dùng snap-scroll ngang thay cho cột dọc dài.

---

## 5. Kiến trúc kỹ thuật

### 5.1 Build

Mở rộng `scripts/build_blog.py` thành `scripts/build.py`:

- Đọc `site.json` (thông tin doanh nghiệp, 8 dịch vụ kèm thông số, FAQ, khu vực phục vụ).
- Đọc template trong `partials/` (`head.html`, `header.html`, `footer.html`, `sticky-bar.html`).
- Sinh HTML hoàn chỉnh với header/footer/schema **inline sẵn** cho từng trang.
- Dữ liệu bài blog vẫn lấy từ `docs/research/blog-raw/`.

Output vẫn là HTML tĩnh thuần, deploy được lên bất kỳ static host nào. Bỏ `assets/js/include.js`.

Một trường dữ liệu duy nhất (ví dụ giá dịch vụ) chỉ xuất hiện một lần trong `site.json`; trang chủ, trang dịch vụ, dropdown form và schema đều đọc từ đó.

### 5.2 CSS

Một file `assets/css/main.css` tổ chức bằng `@layer`:

```css
@layer tokens, base, layout, components, utilities;
```

- `tokens` — biến CSS, không có selector nào khác.
- `base` — reset, typography, focus-visible, reduced-motion.
- `layout` — container, band, grid, stack.
- `components` — button, card, spec-line, numeric-rail, stepper, faq, form, sticky-bar, nav.
- `utilities` — một tập nhỏ, đặt tên rõ ràng.

Không còn `style=` inline trong bất kỳ file HTML nào.

### 5.3 JavaScript

`assets/js/main.js` — vanilla, không dependency:

- Toggle nav mobile có quản lý `aria-expanded` và focus trap.
- FAQ dựng lại bằng `<button aria-expanded aria-controls>` + region; animate bằng `grid-template-rows` thay cho `max-height`.
- Sticky bar ẩn/hiện theo hướng cuộn, dùng `IntersectionObserver`.
- Lọc chip trong blog index.
- Validation form inline.

### 5.4 SEO

Mỗi trang nhận, sinh tại build time:

- `<link rel="canonical">`
- Open Graph + Twitter card
- JSON-LD:
  - `LocalBusiness` (mọi trang) — tên, địa chỉ, hotline, giờ làm việc, `areaServed`
  - `Service` (trang dịch vụ) — cho từng dịch vụ trong 8 mục, kèm `offers.priceRange`
  - `FAQPage` (trang dịch vụ)
  - `BreadcrumbList` (mọi trang trừ trang chủ)
  - `BlogPosting` (bài blog)
- `sitemap.xml` và `robots.txt` sinh tự động.

### 5.5 Ảnh

- Chuyển toàn bộ sang WebP, giữ bản gốc trong `assets/images/_src/`.
- Sinh `srcset` ở các bề rộng 480 / 960 / 1440.
- `width`/`height` tường minh trên mọi thẻ `<img>`.
- `loading="lazy"` + `decoding="async"` cho ảnh dưới màn hình đầu.
- Viết lại toàn bộ alt text cho khớp nội dung ảnh thật.
- Mục tiêu: `bat-che-nang-mua.png` từ 1.78 MB xuống dưới 80 KB.

### 5.6 Accessibility

- `:focus-visible` toàn cục: viền 2px `--amber`, `outline-offset: 2px`.
- `aria-expanded` / `aria-controls` trên nav toggle và FAQ.
- Skip link tới `<main>`.
- `@media (prefers-reduced-motion: reduce)` tắt mọi transition và animation.
- Điều hướng bàn phím đầy đủ cho nav mobile, FAQ, chip lọc.
- Mọi target ≥44px trên mobile.

---

## 6. Phạm vi

### Trong phạm vi

- Toàn bộ design system mới (token, typography, component).
- Dựng lại 6 trang chính + template bài blog.
- Build script Python inline header/footer/schema.
- Hình vẽ nét SVG cho 8 dịch vụ.
- Sticky mobile action bar, nút Zalo.
- Sửa dropdown form khớp 8 dịch vụ thật.
- Structured data, sitemap, canonical, OG.
- Tối ưu ảnh, sửa alt text.
- Sửa toàn bộ lỗi accessibility đã liệt kê.

### Ngoài phạm vi

- Nối form với backend thật (giữ giả lập, có `TODO` rõ ràng — theo quyết định của chủ dự án).
- Chụp hoặc mua ảnh công trình thật (slot markup để sẵn).
- Viết nội dung blog mới.
- Đa ngôn ngữ.
- Analytics, tracking.

## 7. Tiêu chí nghiệm thu

1. Không còn thuộc tính `style=` nào trong các file HTML.
2. Mọi cặp màu chữ/nền đạt ≥4.5:1, trừ `--amber-bright` chỉ dùng ở chữ ≥24px bold (≥3:1).
3. Hotline và nút Zalo hiển thị được ở mọi breakpoint từ 320px trở lên.
4. Dropdown dịch vụ trong form liệt kê đúng 8 dịch vụ trong `site.json`.
5. `view-source` của mọi trang chứa sẵn header, footer và JSON-LD (không cần JavaScript).
6. Không thẻ `<img>` nào thiếu `width`/`height`.
7. Không còn viền accent 3px nào trong `main.css`.
8. Điều hướng được toàn site chỉ bằng bàn phím, focus luôn nhìn thấy.
9. Không có scroll ngang ở 320 / 375 / 768 / 1024 / 1440px.
10. Không thẻ `tel:` nào gắn trên phần tử không phải hành động gọi điện.
11. Trang Dự án không hiển thị ảnh stock kèm nhãn "đã thi công".

## 8. Quyết định đã chốt

| Câu hỏi | Quyết định |
|---|---|
| Hướng thiết kế | A (Kỹ thuật tin cậy) + cơ chế chuyển đổi của C |
| Palette | Tự do đề xuất — "Thép & Nắng", dẫn xuất từ màu logo |
| Header/footer | Build script Python inline vào HTML |
| Ưu tiên | Cả bốn: design system + trang chủ, chuyển đổi, trang dịch vụ, SEO/perf/a11y |
| Ảnh | Hình vẽ nét SVG, để sẵn slot chờ ảnh thật |
| Form | Giữ giả lập client-side, ghi `TODO` |
