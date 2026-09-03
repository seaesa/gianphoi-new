#!/usr/bin/env python3
import re, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "docs/research/blog-raw")
OUT = os.path.join(ROOT, "blog")

POSTS = [
    dict(slug="quan-3", file="quan-3.txt", title="Lắp đặt giàn phơi thông minh chính hãng quận 3 TP HCM giá rẻ",
         date="29/5/2026", img="quan-3.webp",
         desc="Hướng dẫn lắp đặt giàn phơi thông minh chính hãng giá rẻ tại Quận 3 TP.HCM, quy trình 4 bước và bảng giá tham khảo."),
    dict(slug="di-an", file="di-an.txt", title="Lắp đặt giàn phơi thông minh chính hãng tại phường Dĩ An TPHCM (Bình Dương cũ)",
         date="28/5/2026", img="di-an.webp",
         desc="Dịch vụ lắp đặt giàn phơi thông minh, lưới cáp ban công và cửa lưới chống muỗi chính hãng tại Dĩ An, TP.HCM."),
    dict(slug="quan-1", file="quan-1.txt", title="Lắp đặt giàn phơi thông minh chính hãng quận 1 TPHCM",
         date="27/5/2026", img="quan-1.webp",
         desc="Tiêu chí chọn đơn vị lắp đặt giàn phơi thông minh uy tín tại Quận 1, quy trình thi công và bảng giá tham khảo."),
    dict(slug="mui-hoi", file="mui-hoi.txt", title="Cách giải quyết quần áo phơi trong nhà có mùi hôi",
         date="19/10/2025", img="mui-hoi.webp",
         desc="10 cách khử mùi hôi quần áo phơi trong nhà hiệu quả, cùng gợi ý các dòng giàn phơi thông minh phù hợp cho chung cư."),
    dict(slug="chung-cu", file="chung-cu.txt", title="Giàn phơi thông minh cho chung cư: Giải pháp hiện đại tối ưu không gian sống năm 2025",
         date="18/10/2025", img="chung-cu.webp",
         desc="Phân loại, tiêu chí chọn mua và bảng giá tham khảo giàn phơi thông minh cho căn hộ chung cư năm 2025."),
    dict(slug="mua-mua", file="mua-mua.txt", title="Mùa mưa Sài Gòn và giải pháp bạt che nắng mưa cho mọi nhà",
         date="18/10/2025", img="mua-mua.webp",
         desc="Các loại bạt che nắng mưa phổ biến và mẹo chọn bạt che phù hợp cho mùa mưa tại TP.HCM."),
    dict(slug="top5-thuong-hieu", file="top5-thuong-hieu.txt", title="Top 5 thương hiệu giàn phơi thông minh uy tín nhất Việt Nam",
         date="17/10/2025", img="top5-thuong-hieu.webp",
         desc="Đánh giá 5 thương hiệu giàn phơi thông minh uy tín: Sankaku, Hoseta, Hòa Phát, Việt Nhật, Larano."),
    dict(slug="top5-mau", file="top5-mau.txt", title="Top 5 mẫu giàn phơi thông minh mới nhất năm 2025",
         date="17/10/2025", img="top5-mau.webp",
         desc="Điểm qua 5 mẫu giàn phơi thông minh đáng mua nhất năm 2025 kèm giá tham khảo."),
    dict(slug="vach-lanh", file="vach-lanh.txt", title="Dịch Vụ Lắp Đặt Vách Lạnh Ngăn Điều Hòa Tại Bình Dương",
         date="16/10/2025", img="vach-lanh.webp",
         desc="Lợi ích, ứng dụng thực tế, quy trình và báo giá lắp đặt vách lạnh ngăn điều hòa tại Bình Dương."),
    dict(slug="giai-phap-khong-gian", file="giai-phap-khong-gian.txt", title="Giải pháp giàn phơi thông minh phù hợp cho từng không gian",
         date="16/10/2025", img="giai-phap-khong-gian.webp",
         desc="Giải pháp giàn phơi thông minh theo từng loại không gian: chung cư, nhà phố, biệt thự, ban công nhỏ."),
    dict(slug="top10-don-vi", file="top10-don-vi.txt", title="Top 10 đơn vị lắp đặt giàn phơi thông minh uy tín ở Bình Dương & TP.HCM",
         date="16/10/2025", img="top10-don-vi.webp",
         desc="Danh sách 10 đơn vị lắp đặt giàn phơi thông minh được khách hàng tin tưởng tại Bình Dương & TP.HCM."),
    dict(slug="nhan-biet-chinh-hang", file="nhan-biet-chinh-hang.txt", title="Cách Nhận Biết Giàn Phơi Thông Minh Chính Hãng",
         date="15/10/2025", img="nhan-biet-chinh-hang.webp",
         desc="Hướng dẫn nhận biết giàn phơi thông minh chính hãng qua bao bì, chất liệu, logo, hóa đơn bảo hành."),
]

def inline(text):
    text = (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    return text

def md_to_html(md):
    lines = md.strip("\n").split("\n")
    html = []
    i = 0
    def flush_list(buf, tag):
        if buf:
            html.append(f"<{tag}>")
            for item in buf:
                html.append(f"<li>{inline(item)}</li>")
            html.append(f"</{tag}>")
            buf.clear()

    ul_buf, ol_buf, table_buf = [], [], []

    def flush_table():
        if not table_buf:
            return
        rows = [r for r in table_buf if not re.match(r"^\|[\s\-|]+\|$", r)]
        html.append("<table>")
        for idx, row in enumerate(rows):
            cells = [c.strip() for c in row.strip("|").split("|")]
            tag = "th" if idx == 0 else "td"
            html.append("<tr>" + "".join(f"<{tag}>{inline(c)}</{tag}>" for c in cells) + "</tr>")
        html.append("</table>")
        table_buf.clear()

    while i < len(lines):
        line = lines[i].strip()
        if not line:
            flush_list(ul_buf, "ul"); flush_list(ol_buf, "ol"); flush_table()
            i += 1
            continue
        if line.startswith("### "):
            flush_list(ul_buf, "ul"); flush_list(ol_buf, "ol"); flush_table()
            html.append(f"<h3>{inline(line[4:])}</h3>")
        elif line.startswith("## "):
            flush_list(ul_buf, "ul"); flush_list(ol_buf, "ol"); flush_table()
            html.append(f"<h2>{inline(line[3:])}</h2>")
        elif line.startswith("|"):
            table_buf.append(line)
        elif line.startswith("- "):
            flush_list(ol_buf, "ol"); flush_table()
            ul_buf.append(line[2:])
        elif re.match(r"^\d+\.\s", line):
            flush_list(ul_buf, "ul"); flush_table()
            ol_buf.append(re.sub(r"^\d+\.\s", "", line))
        else:
            flush_list(ul_buf, "ul"); flush_list(ol_buf, "ol"); flush_table()
            html.append(f"<p>{inline(line)}</p>")
        i += 1
    flush_list(ul_buf, "ul"); flush_list(ol_buf, "ol"); flush_table()
    return "\n".join(html)

PAGE_TMPL = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | Blog Giàn Phơi Thông Minh</title>
<meta name="description" content="{desc}">
<link rel="icon" href="/assets/images/logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@600;700;800&family=Be+Vietnam+Pro:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/main.css">
</head>
<body data-page="blog">

<header class="site-header" data-include="/partials/header.html"></header>

<main>
  <div class="container">
    <div class="page-hero">
      <div class="breadcrumb"><a href="/index.html">Trang chủ</a><span>/</span><a href="/blog.html">Blog</a><span>/</span><span>Bài viết</span></div>
      <h1 style="max-width:760px; margin-inline:auto;">{title}</h1>
      <div class="article-meta"><span>{date}</span><span>·</span><span>Giàn Phơi Thông Minh Bình Dương &amp; TP.HCM</span></div>
    </div>
  </div>

  <section class="container">
    <article class="article">
      <div class="cover"><img src="/assets/images/blog/{img}" alt="{title}"></div>
{body}
    </article>

    <div class="related-list">
      <h3>Bài viết khác</h3>
      <div class="grid grid-3">
{related}
      </div>
    </div>
  </section>
</main>

<footer class="site-footer" data-include="/partials/footer.html"></footer>

<script src="/assets/js/include.js"></script>
<script src="/assets/js/main.js"></script>
</body>
</html>
"""

RELATED_TMPL = '''        <a href="/blog/{slug}.html" class="card blog-card">
          <div class="thumb"><img src="/assets/images/blog/{img}" alt="{title}"></div>
          <div class="body"><span class="date">{date}</span><h3>{title}</h3><span class="read-more">Đọc tiếp →</span></div>
        </a>'''

os.makedirs(OUT, exist_ok=True)

for idx, post in enumerate(POSTS):
    raw_path = os.path.join(RAW, post["file"])
    with open(raw_path, encoding="utf-8") as f:
        raw = f.read()
    # strip the metadata header (URL/Thumb/Title/Date lines + blank) before content
    body_md = re.split(r"\n\n", raw, maxsplit=1)[1] if raw.startswith("URL:") else raw
    body_html = md_to_html(body_md)

    others = [p for j, p in enumerate(POSTS) if j != idx][:3]
    related_html = "\n".join(
        RELATED_TMPL.format(slug=o["slug"], img=o["img"], title=o["title"], date=o["date"])
        for o in others
    )

    page = PAGE_TMPL.format(
        title=post["title"], desc=post["desc"], date=post["date"], img=post["img"],
        body=body_html, related=related_html
    )
    out_path = os.path.join(OUT, f"{post['slug']}.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(page)
    print("wrote", out_path)
