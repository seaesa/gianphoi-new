# Giàn Phơi Thông Minh — Bình Dương & TP.HCM

Website tĩnh cho dịch vụ lắp đặt và sửa chữa giàn phơi thông minh, lưới cáp
ban công, cửa lưới chống muỗi tại TP.HCM và Bình Dương.

Thiết kế **"Thép & Nắng"** — xem
[spec](docs/superpowers/specs/2026-09-11-ui-ux-redesign-design.md) và
[implementation plan](docs/superpowers/plans/2026-09-11-ui-ux-redesign.md).

## Build

```bash
python -m scripts.build
```

Sinh toàn bộ HTML tĩnh ở thư mục gốc: 6 trang chính, 12 bài blog,
`sitemap.xml` và `robots.txt`. Không cần Node, không cần cài gì ngoài
Python 3 và Pillow (chỉ dùng khi xử lý ảnh).

**Không sửa tay các file `.html` ở thư mục gốc và trong `blog/`** — chúng là
output, sẽ bị ghi đè ở lần build sau. Sửa trong `templates/` hoặc `site.json`.

## Chạy thử

```bash
python -m http.server 8000
```

## Test

```bash
python -m unittest discover -s tests -t . -v
```

Dùng `unittest` của thư viện chuẩn, **không cần pytest**.
`tests/test_acceptance.py` chuyển 11 tiêu chí nghiệm thu ở spec §7 thành
assertion chạy trên HTML đã build.

## Cấu trúc

| Đường dẫn | Vai trò |
|---|---|
| `site.json` | **Nguồn chân lý duy nhất**: thông tin doanh nghiệp, 8 dịch vụ kèm thông số và giá, 10 FAQ, khu vực phục vụ, 12 bài blog |
| `templates/` | Template từng trang; file bắt đầu bằng `_` là partial dùng chung |
| `scripts/` | Build pipeline (`build.py`) và các module: dữ liệu, markdown, template engine, component, JSON-LD, ảnh, tương phản màu |
| `assets/css/main.css` | Toàn bộ CSS, tổ chức bằng `@layer tokens, base, layout, components, utilities` |
| `assets/svg/` | 8 hình vẽ nét sản phẩm, dùng thay ảnh |
| `assets/images/_src/` | Ảnh gốc, **không deploy** (đã chặn trong `robots.txt`) |
| `docs/research/blog-raw/` | Nội dung thô của bài blog |

Sửa giá, thêm dịch vụ, đổi số điện thoại → sửa `site.json` rồi build lại.
Một dữ liệu chỉ tồn tại một chỗ: trang chủ, trang dịch vụ, dropdown form và
JSON-LD đều đọc từ đó.

## Những việc còn lại

| Việc | Ghi chú |
|---|---|
| **Form báo giá chưa gửi đi đâu** | Hiện chỉ giả lập thành công ở client. Xem `TODO` trong `assets/js/main.js` — nối Formspree/Web3Forms hoặc chuyển hướng Zalo |
| **Ảnh công trình thật** | Trang `khu-vuc.html` có sẵn grid rỗng kèm hướng dẫn trong comment HTML. Toàn bộ ảnh stock cũ đã bị gỡ vì không đúng chủ đề (spec §2.2) |
| **Giờ làm việc** | `site.json` đang để `Mo-Su 08:00-18:00` — cần chủ doanh nghiệp xác nhận |
| **Bảo hành 5 dịch vụ** | Đang ghi "Liên hệ" vì nội dung cũ không nêu con số. Điền vào `site.json` khi có |
| **Nhãn "Phổ biến nhất"** | Đang gắn cho Giàn Phơi Treo Trần — đổi bằng cờ `popular` trong `site.json` |
| **Tên miền** | Canonical và JSON-LD dùng `https://gianphoithongminh.vn`. Đổi bằng biến môi trường `SITE_BASE_URL` |
