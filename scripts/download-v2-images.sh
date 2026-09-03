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
fetch https://plus.unsplash.com/premium_photo-1683134581882-07dfd927ead1 "$IMG/about-thi-cong.jpg"
fetch https://plus.unsplash.com/premium_photo-1661963024541-1a485c66957d "$IMG/thi-cong.jpeg"

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

fetch https://images.unsplash.com/photo-1721673027581-cd2d7c342daf "$IMG/blog/quan-3.webp"
fetch https://plus.unsplash.com/premium_photo-1663045230477-ad641bffef0f "$IMG/blog/di-an.webp"
fetch https://images.unsplash.com/photo-1728034261564-18930dcb2c8e "$IMG/blog/quan-1.webp"
fetch https://plus.unsplash.com/premium_photo-1679686261674-6850ee4dedb0 "$IMG/blog/mui-hoi.webp"
fetch https://images.unsplash.com/photo-1762845872088-12c352bbb119 "$IMG/blog/chung-cu.webp"
fetch https://images.unsplash.com/photo-1724893962134-fa9647914053 "$IMG/blog/mua-mua.webp"
fetch https://images.unsplash.com/photo-1759064776046-45b988af4b6d "$IMG/blog/top5-thuong-hieu.webp"
fetch https://images.unsplash.com/photo-1737054718383-68055423d164 "$IMG/blog/top5-mau.webp"
fetch https://images.unsplash.com/photo-1765371513492-264506c3ad09 "$IMG/blog/vach-lanh.webp"
fetch https://images.unsplash.com/photo-1747113225475-8592c238cf08 "$IMG/blog/giai-phap-khong-gian.webp"
fetch https://plus.unsplash.com/premium_photo-1661963024541-1a485c66957d "$IMG/blog/top10-don-vi.webp"
fetch https://plus.unsplash.com/premium_photo-1674575954775-b5ef5af6fd17 "$IMG/blog/nhan-biet-chinh-hang.webp"

echo "done"
