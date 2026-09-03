#!/bin/bash
set -e
cd "$(dirname "$0")/.."
IMG=assets/images

fetch() {
  local url="$1" out="$2"
  echo "-> $out"
  curl -sL --max-time 30 "${url}?fm=jpg&q=80&w=1400&auto=format&fit=crop&ixlib=rb-4.1.0" -o "/tmp/dl_src.jpg"
  case "$out" in
    *.png) convert /tmp/dl_src.jpg "$out" ;;
    *.webp) convert /tmp/dl_src.jpg -quality 82 "$out" ;;
    *) cp /tmp/dl_src.jpg "$out" ;;
  esac
}

fetch https://images.unsplash.com/photo-1684703125510-673d3042873f "$IMG/hero-banner.jpg"
# Thay thế: ảnh thi công người nước ngoài -> ảnh thợ/kỹ thuật viên châu Á (Pexels, free license)
fetch https://images.pexels.com/photos/4491871/pexels-photo-4491871.jpeg "$IMG/about-thi-cong.jpg"
fetch https://images.pexels.com/photos/1249611/pexels-photo-1249611.jpeg "$IMG/thi-cong.jpeg"

fetch https://images.unsplash.com/photo-1517502166878-35c93a0072f0 "$IMG/services/gian-phoi-dieu-khien.jpeg"
fetch https://images.unsplash.com/photo-1754959069303-1b7e6cf8059f "$IMG/services/gian-phoi-treo-tran.jpg"
fetch https://plus.unsplash.com/premium_photo-1671031351385-b22383455a85 "$IMG/services/gian-phoi-xep-tuong.jpeg"
fetch https://images.unsplash.com/photo-1774796212953-f046482ee6f1 "$IMG/services/luoi-cap-ban-cong.jpg"
fetch https://images.unsplash.com/photo-1735822083502-0c5fab870457 "$IMG/services/cua-luoi-chong-muoi.jpg"
fetch https://images.unsplash.com/photo-1765371513492-264506c3ad09 "$IMG/services/vach-ngan-lanh.jpg"
fetch https://images.unsplash.com/photo-1693607053187-2650d20314f3 "$IMG/services/mai-hien-quay-tay.jpg"
fetch https://images.unsplash.com/photo-1704500335770-259940efa439 "$IMG/services/bat-che-nang-mua.png"

fetch https://images.unsplash.com/photo-1691811498201-fe44e0d0dc07 "$IMG/projects/thu-dau-mot.jpg"
fetch https://images.unsplash.com/photo-1757125505346-2d71c70e6003 "$IMG/projects/thu-duc.jpg"
fetch https://images.unsplash.com/photo-1759162788764-f40075c8857f "$IMG/projects/quan-7.jpg"
fetch https://images.unsplash.com/photo-1762028007806-751f2bef444a "$IMG/projects/quan-1.jpg"

# Blog: thay Unsplash (người nước ngoài) -> Pexels trung tính / châu Á, free license, không lộ mặt người nước ngoài
fetch https://images.pexels.com/photos/3803423/pexels-photo-3803423.jpeg "$IMG/blog/quan-3.webp"
# di-an: dùng lại ảnh gốc gianphoichinhhang.com (ảnh thật VN, không người nước ngoài)
fetch https://www.gianphoichinhhang.com/images/posts/22/thumbnails/lap-dat-gian-phoi-thong-minh-chinh-hang-tai-phuong-di-an-tphcm-binh-duong-cu-300x200.webp "$IMG/blog/di-an.webp"
fetch https://images.pexels.com/photos/8092505/pexels-photo-8092505.jpeg "$IMG/blog/quan-1.webp"
fetch https://images.pexels.com/photos/1080696/pexels-photo-1080696.jpeg "$IMG/blog/mui-hoi.webp"
fetch https://images.pexels.com/photos/271624/pexels-photo-271624.jpeg "$IMG/blog/chung-cu.webp"
fetch https://images.pexels.com/photos/4103242/pexels-photo-4103242.jpeg "$IMG/blog/mua-mua.webp"
fetch https://images.pexels.com/photos/585418/pexels-photo-585418.jpeg "$IMG/blog/top5-thuong-hieu.webp"
fetch https://images.pexels.com/photos/2988425/pexels-photo-2988425.jpeg "$IMG/blog/top5-mau.webp"
fetch https://images.pexels.com/photos/3791466/pexels-photo-3791466.jpeg "$IMG/blog/vach-lanh.webp"
fetch https://images.pexels.com/photos/259239/pexels-photo-259239.jpeg "$IMG/blog/giai-phap-khong-gian.webp"
# top10: dùng lại ảnh gốc gianphoichinhhang.com (ảnh thật VN)
fetch https://www.gianphoichinhhang.com/images/posts/13/thumbnails/top-10-don-vi-lap-dat-gian-phoi-thong-minh-uy-tin-o-binh-duong--tphcm-300x200.webp "$IMG/blog/top10-don-vi.webp"
fetch https://images.pexels.com/photos/5693633/pexels-photo-5693633.jpeg "$IMG/blog/nhan-biet-chinh-hang.webp"

echo "done"
