#!/usr/bin/env bash
set -e
BASE="https://www.gianphoichinhhang.com"
cd "$(dirname "$0")/.."

dl() {
  local url="$1" out="$2"
  mkdir -p "$(dirname "$out")"
  curl -sL --fail "$url" -o "$out" && echo "OK  $out" || echo "FAIL $url"
}

dl "$BASE/images/logo.png" assets/images/logo.png
dl "$BASE/images/banner-dich-vu-lap-dat-gian-phoi-thong-minh-binh-duong-tp-hcm.jpg" assets/images/hero-banner.jpg
dl "$BASE/images/thi-cong-lap-dat-gian-phoi-thong-minh-binh-duong-tp-hcm.jpeg" assets/images/thi-cong.jpeg
dl "$BASE/images/nhan-vien-tien-hanh-huong-dan-su-dung-gian-phoi-sau-khi-lap-dat.jpg" assets/images/nhan-vien-huong-dan.jpg
dl "$BASE/images/gian-phoi-thong-minh-thi-cong-lap-dat-tai-thu-dau-mot.jpg" assets/images/about-thi-cong.jpg

dl "$BASE/images/gian-phoi-thong-minh-hoa-phat-hp-01-dieu-khien-tu-xa.jpeg" assets/images/services/gian-phoi-dieu-khien.jpeg
dl "$BASE/images/Gian-phoi-thong-minh-4-thanh-hoa-phat-h007.jpg" assets/images/services/gian-phoi-treo-tran.jpg
dl "$BASE/images/gian-phoi-xep-gan-tuong.jpeg" assets/images/services/gian-phoi-xep-tuong.jpeg
dl "$BASE/images/luoi-cap-an-toa-ban-cong.jpg" assets/images/services/luoi-cap-ban-cong.jpg
dl "$BASE/images/cua-luoi-chong-muoi-co-dinh.jpg" assets/images/services/cua-luoi-chong-muoi.jpg
dl "$BASE/images/vach-ngan-lanh-dieu-hoa.jpg" assets/images/services/vach-ngan-lanh.jpg
dl "$BASE/images/mai-hien-quay-tay.jpg" assets/images/services/mai-hien-quay-tay.jpg
dl "$BASE/images/bat-che-nang-mua-tu-cuon.png" assets/images/services/bat-che-nang-mua.png

dl "$BASE/images/cua-chong-muoi-dang-xep-gap-cho-cua-chinh-binh-duong.jpg" assets/images/projects/thu-dau-mot.jpg
dl "$BASE/images/gian-phoi-thong-minh-gan-tuong.jpg" assets/images/projects/thu-duc.jpg
dl "$BASE/images/gian-phoi-dieu-khien-tu-xa-quan-7.jpg" assets/images/projects/quan-7.jpg
dl "$BASE/images/vach-lanh-ngan-dieu-hoa-to-ong-quan-1.jpg" assets/images/projects/quan-1.jpg

dl "$BASE/images/icon-phone.webp" assets/images/icon-phone.webp
dl "$BASE/images/icon-zalo.png" assets/images/icon-zalo.png

for id in 12 13 14 15 16 17 18 19 20 21 22 23; do
  mkdir -p "assets/images/blog"
done

dl "$BASE/images/posts/23/thumbnails/lap-dat-gian-phoi-thong-minh-chinh-hang-quan-3-tp-hcm-gia-re-300x200.webp" assets/images/blog/quan-3.webp
dl "$BASE/images/posts/22/thumbnails/lap-dat-gian-phoi-thong-minh-chinh-hang-tai-phuong-di-an-tphcm-binh-duong-cu-300x200.webp" assets/images/blog/di-an.webp
dl "$BASE/images/posts/21/thumbnails/lap-dat-gian-phoi-thong-minh-chinh-hang-quan-1-tphcm-300x200.webp" assets/images/blog/quan-1.webp
dl "$BASE/images/posts/20/thumbnails/cach-giai-quyet-quan-ao-phoi-trong-nha-co-mui-hoi-300x200.webp" assets/images/blog/mui-hoi.webp
dl "$BASE/images/posts/19/thumbnails/gian-phoi-thong-minh-cho-chung-cu-giai-phap-hien-dai-toi-uu-khong-gian-song-nam-2025-300x200.webp" assets/images/blog/chung-cu.webp
dl "$BASE/images/posts/18/thumbnails/mua-mua-sai-gon-va-giai-phap-bat-che-nang-mua-cho-moi-nha-300x200.webp" assets/images/blog/mua-mua.webp
dl "$BASE/images/posts/17/thumbnails/top-5-thuong-hieu-gian-phoi-thong-minh-uy-tin-nhat-viet-nam-300x200.webp" assets/images/blog/top5-thuong-hieu.webp
dl "$BASE/images/posts/16/thumbnails/top-5-mau-gian-phoi-thong-minh-moi-nhat-nam-2025-tien-nghi-hien-dai-va-tiet-kiem-khong-gian-300x200.webp" assets/images/blog/top5-mau.webp
dl "$BASE/images/posts/15/thumbnails/dich-vu-lap-dat-vach-lanh-ngan-dieu-hoa-tai-binh-duong-300x200.webp" assets/images/blog/vach-lanh.webp
dl "$BASE/images/posts/14/thumbnails/giai-phap-gian-phoi-thong-minh-phu-hop-cho-tung-khong-gian-300x200.webp" assets/images/blog/giai-phap-khong-gian.webp
dl "$BASE/images/posts/13/thumbnails/top-10-don-vi-lap-dat-gian-phoi-thong-minh-uy-tin-o-binh-duong--tphcm-300x200.webp" assets/images/blog/top10-don-vi.webp
dl "$BASE/images/posts/12/thumbnails/cach-nhan-biet-gian-phoi-thong-minh-chinh-hang-300x200.webp" assets/images/blog/nhan-biet-chinh-hang.webp

echo "Done."
