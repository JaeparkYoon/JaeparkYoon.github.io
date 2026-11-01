#!/usr/bin/env python3
"""
Medium 글을 홈페이지 블로그로 옮긴다.

  python3 tools/build_blog.py

- Medium RSS(@jpyoon1122)에서 글 본문을 받아 blog/<post id>.html 로 생성
  (글 순서는 Medium 프로필과 같은 피드 순서를 따르되, "제목 — 1", "제목 — 2" 같은
   연재 글은 첫 편이 나온 자리에 1편부터 차례로 모은다. 작성일은 표시하지 않는다)
- 본문 이미지는 assets/images/blog/<slug>/ 에 내려받아 로컬 경로로 교체
- Medium 코드 임베드(GitHub Gist)는 Gist 원본 코드를 받아 <pre><code> 로 교체
  (Medium 임베드 ID = md5(gist URL) 이므로 내 Gist 목록과 대조해 찾는다.
   비밀 Gist까지 보려면 gh CLI 로그인이 필요하고, 없으면 공개 Gist만 대조한다)
- index.html 의 BLOG:START ~ BLOG:END 사이 글 목록을 다시 쓴다

외부 패키지 없이 표준 라이브러리만 사용한다.
"""

import hashlib
import html
import json
import re
import shutil
import subprocess
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

MEDIUM_USER = "jpyoon1122"
GITHUB_USER = "JaeparkYoon"
FEED_URL = f"https://medium.com/feed/@{MEDIUM_USER}"
GISTS_URL = f"https://api.github.com/users/{GITHUB_USER}/gists?per_page=100"

ROOT = Path(__file__).resolve().parent.parent
BLOG_DIR = ROOT / "blog"
IMAGE_DIR = ROOT / "assets" / "images" / "blog"
INDEX = ROOT / "index.html"

# 해시가 맞지 않는 임베드(주소 형식이 다른 경우)는 직접 연결한다: Medium 임베드 ID -> Gist ID
MANUAL_EMBEDS = {
    "8985f31089b982d6597a6f9083947cab": "d6e62b5a81b3764da86a599798092f41",  # 숏츠 뉴스 — LineMeasuredText
}

# 홈페이지에서 빼고 싶은 본문 이미지: 글 ID -> 지울 <figure> 순번(1부터)
REMOVE_FIGURES = {
    "6ab23b4448f1": {1},  # Kotlin flow sample — 맨 위 표지 이미지
}

# Medium 원본이 저해상도라 다시 그린 이미지로 바꿔 쓴다: Medium 이미지 주소 -> 글 이미지 폴더 안의 파일명
IMAGE_OVERRIDES = {
    "https://cdn-images-1.medium.com/max/500/0*LIZhF4ZzO9xm_uAC": "fading-edge.png",  # RecyclerView fadingEdge — overlay view
}

NS = {"content": "http://purl.org/rss/1.0/modules/content/"}
UA = {"User-Agent": "Mozilla/5.0 (blog builder)"}


def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as res:
        return res.read()


def list_gists():
    if shutil.which("gh"):
        result = subprocess.run(["gh", "api", "gists?per_page=100"], capture_output=True, text=True)
        if result.returncode == 0:
            return json.loads(result.stdout)
    print("  (gh CLI를 쓸 수 없어 공개 Gist만 대조합니다)")
    return json.loads(fetch(GISTS_URL))


def gist_files(gist):
    return [
        (f["filename"], (f.get("language") or "").lower(), fetch(f["raw_url"]).decode("utf-8"))
        for f in gist["files"].values()
    ]


def load_gists():
    """Medium 임베드 ID -> [(파일명, 언어, 코드)]"""
    gists = {}
    by_id = {}
    for gist in list_gists():
        files = by_id[gist["id"]] = gist_files(gist)
        for url in (
            gist["html_url"],
            f"https://gist.github.com/{gist['id']}",
            f"https://gist.github.com/{GITHUB_USER}/{gist['id']}",
            f"https://gist.github.com/{GITHUB_USER.lower()}/{gist['id']}",
        ):
            gists[hashlib.md5(url.encode()).hexdigest()] = files
    for media_id, gist_id in MANUAL_EMBEDS.items():
        if gist_id not in by_id:
            by_id[gist_id] = gist_files(json.loads(fetch(f"https://api.github.com/gists/{gist_id}")))
        gists[media_id] = by_id[gist_id]
    return gists


def post_id(link):
    # https://medium.com/@user/<title-slug>-<12자리 id>?source=rss-...
    return re.search(r"-([0-9a-f]{10,})(?:\?|$)", link).group(1)


def code_block(code, lang, filename=None):
    cls = f' class="language-{lang}"' if lang else ""
    name = f'<div class="code-filename">{html.escape(filename)}</div>' if filename else ""
    return f'<figure class="code-block">{name}<pre><code{cls}>{html.escape(code.rstrip())}</code></pre></figure>'


def convert(body, slug, gists, local_links):
    # 지정한 이미지(figure) 제거
    skip = REMOVE_FIGURES.get(slug, set())
    figure_no = 0

    def drop_figure(m):
        nonlocal figure_no
        figure_no += 1
        return "" if figure_no in skip else m.group(0)

    body = re.sub(r"<figure>.*?</figure>", drop_figure, body, flags=re.S)

    # Medium 조회수 집계용 1px 이미지 제거
    body = re.sub(r'<img src="https://medium\.com/_/stat[^>]*>', "", body)

    # Gist 임베드 → 코드 블록
    def replace_embed(m):
        media_id = m.group(1)
        files = gists.get(media_id)
        if not files:
            print(f"  ! 코드 임베드를 찾지 못함: {media_id} (Medium 원문 링크로 대체)")
            return f'<p class="embed-fallback"><a href="https://medium.com/media/{media_id}/href">코드 보기 (Medium)</a></p>'
        return "".join(code_block(code, lang, name) for name, lang, code in files)

    body = re.sub(
        r'<iframe[^>]*>\s*<a href="https://medium\.com/media/([0-9a-f]{32})/href">.*?</a>\s*</iframe>',
        replace_embed,
        body,
        flags=re.S,
    )

    # Medium 코드 블록(<pre>…<br>…</pre>) → 줄바꿈 정리
    def fix_pre(m):
        code = re.sub(r"<br\s*/?>", "\n", m.group(1))
        code = re.sub(r"<[^>]+>", "", code)
        return code_block(html.unescape(code), "kotlin")

    body = re.sub(r"<pre>(.*?)</pre>", fix_pre, body, flags=re.S)

    # 이미지 내려받기 (파일 이름은 원본 주소 해시라 순서가 바뀌어도 같은 그림을 가리킨다)
    target = IMAGE_DIR / slug

    def replace_img(m):
        src = m.group(1)
        alt = re.search(r'alt="([^"]*)"', m.group(0))
        alt = alt.group(1) if alt else ""
        if src in IMAGE_OVERRIDES:
            return f'<img src="../assets/images/blog/{slug}/{IMAGE_OVERRIDES[src]}" alt="{alt}" loading="lazy" />'
        ext = Path(src.split("?")[0]).suffix.lower()
        if ext not in (".png", ".jpg", ".jpeg", ".gif", ".webp"):
            ext = ".png"
        name = hashlib.md5(src.encode()).hexdigest()[:12] + ext
        path = target / name
        if not path.exists():
            target.mkdir(parents=True, exist_ok=True)
            path.write_bytes(fetch(src))
        return f'<img src="../assets/images/blog/{slug}/{name}" alt="{alt}" loading="lazy" />'

    body = re.sub(r'<img[^>]*?src="(https://cdn-images-1\.medium\.com/[^"]+)"[^>]*>', replace_img, body)

    # 내 다른 Medium 글로 가는 링크 → 홈페이지 글로
    def replace_link(m):
        href = m.group(1)
        match = re.search(r"-([0-9a-f]{10,})(?:\?|$)", href)
        if "medium.com/@" + MEDIUM_USER in href and match and match.group(1) in local_links:
            return f'href="{local_links[match.group(1)]}.html"'
        return f'href="{href}" target="_blank" rel="noopener noreferrer"'

    body = re.sub(r'href="([^"]+)"', replace_link, body)
    return body


def excerpt(body, limit=110):
    for p in re.findall(r"<p>(.*?)</p>", body, flags=re.S):
        text = html.unescape(re.sub(r"<[^>]+>", "", p)).strip()
        if len(text) > 20:
            return text if len(text) <= limit else text[:limit].rstrip() + "…"
    return ""


def group_series(posts):
    """"제목 — N" 연재 글을 첫 편이 나온 자리에 1편부터 차례로 모은다."""
    series = {}
    for post in posts:
        m = re.match(r"(.+?)\s*[—–-]\s*(\d+)$", post["title"])
        if m:
            series.setdefault(m.group(1), []).append((int(m.group(2)), post))
    ordered, placed = [], set()
    for post in posts:
        m = re.match(r"(.+?)\s*[—–-]\s*(\d+)$", post["title"])
        if not m:
            ordered.append(post)
        elif m.group(1) not in placed:
            placed.add(m.group(1))
            ordered.extend(p for _, p in sorted(series[m.group(1)], key=lambda x: x[0]))
    return ordered


POST_TEMPLATE = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} — 윤재박 기술 블로그</title>
  <meta name="description" content="{description}" />
  <meta name="author" content="Jaepark Yoon" />
  <link rel="canonical" href="{medium_url}" />

  <meta property="og:type" content="article" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{description}" />

  <link rel="icon" type="image/png" href="../assets/images/enopy/icon.png" />
  <link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css" />
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" />
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css" />
  <link rel="stylesheet" href="../assets/css/style.css" />
</head>
<body>

  <header class="site-header">
    <div class="container nav-container">
      <nav>
        <ul class="nav-links" id="navLinks">
          <li><a href="../#career" class="nav-link">경력</a></li>
          <li><a href="../#enopy" class="nav-link">사이드 프로젝트</a></li>
          <li><a href="../#writing" class="nav-link active">기술 블로그</a></li>
          <li><a href="../#contact" class="nav-link">연락처</a></li>
        </ul>
      </nav>

      <div class="nav-actions">
        <a href="https://github.com/JaeparkYoon" target="_blank" rel="noopener noreferrer" class="github-btn">
          <i class="fa-brands fa-github"></i>
          <span>GitHub</span>
        </a>
        <button class="mobile-menu-toggle" id="mobileMenuToggle" aria-label="메뉴 열기" aria-expanded="false">
          <i class="fa-solid fa-bars"></i>
        </button>
      </div>
    </div>
  </header>

  <main class="post-page">
    <article class="container post">
      <a href="../#writing" class="post-back"><i class="fa-solid fa-arrow-left"></i> 글 목록</a>
      <header class="post-header">
        <h1 class="post-title">{title}</h1>
        <div class="post-meta">
          <a href="{medium_url}" target="_blank" rel="noopener noreferrer">Medium 원문 <i class="fa-solid fa-arrow-up-right-from-square"></i></a>
        </div>
      </header>

      <div class="post-body">
{body}
      </div>

      <nav class="post-nav">
{nav}
      </nav>
    </article>
  </main>

  <footer class="site-footer">
    <div class="container footer-content">
      <div>
        <p>© 2026 윤재박 (Jaepark Yoon). All rights reserved.</p>
        <p style="font-size: 0.78rem; margin-top: 4px; color: var(--text-muted);">
          이 글은 <a href="https://medium.com/@{medium_user}" target="_blank" rel="noopener noreferrer">Medium</a>에 먼저 게시되었습니다.
        </p>
      </div>
      <div class="footer-links">
        <a href="https://github.com/JaeparkYoon" target="_blank" rel="noopener noreferrer">GitHub</a>
        <a href="../#career">경력</a>
        <a href="../#enopy">사이드 프로젝트</a>
        <a href="../#writing">기술 블로그</a>
        <a href="mailto:jpyoon1122@gmail.com">Email</a>
      </div>
    </div>
  </footer>

  <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
  <script>hljs.highlightAll();</script>
  <script src="../assets/js/main.js"></script>
</body>
</html>
"""


def nav_link(post, label, cls):
    if not post:
        return f'        <span class="post-nav-item {cls}"></span>'
    return (
        f'        <a class="post-nav-item {cls}" href="{post["slug"]}.html">'
        f'<span class="post-nav-label">{label}</span>'
        f'<span class="post-nav-title">{html.escape(post["title"])}</span></a>'
    )


def card(post):
    return f"""          <a class="writing-card" href="blog/{post['slug']}.html">
            <h3 class="writing-title">{html.escape(post['title'])}</h3>
            <p class="writing-desc">{html.escape(post['excerpt'])}</p>
            <span class="writing-more">읽기 <i class="fa-solid fa-arrow-right"></i></span>
          </a>"""


def main():
    feed = sys.argv[1] if len(sys.argv) > 1 else None
    xml = Path(feed).read_bytes() if feed else fetch(FEED_URL)
    items = ET.fromstring(xml).findall("channel/item")
    print(f"Medium 글 {len(items)}편")

    gists = load_gists()
    print(f"Gist 코드 {len({id(v) for v in gists.values()})}개")

    posts = []
    for item in items:
        link = item.findtext("link")
        posts.append({
            "id": post_id(link),
            "slug": post_id(link),
            "title": item.findtext("title").strip(),
            "medium_url": link.split("?")[0],
            "raw": item.find("content:encoded", NS).text,
        })
    posts = group_series(posts)
    local_links = {p["id"]: p["slug"] for p in posts}

    BLOG_DIR.mkdir(exist_ok=True)
    for i, post in enumerate(posts):
        print(f"- {post['title']}")
        body = convert(post["raw"], post["slug"], gists, local_links)
        post["excerpt"] = excerpt(body)
        # 이전/다음 글은 목록 순서를 따른다
        prev_post = posts[i - 1] if i > 0 else None
        next_post = posts[i + 1] if i + 1 < len(posts) else None
        page = POST_TEMPLATE.format(
            title=html.escape(post["title"]),
            description=html.escape(post["excerpt"]),
            medium_url=post["medium_url"],
            medium_user=MEDIUM_USER,
            body=body,
            nav="\n".join([nav_link(prev_post, "이전 글", "prev"), nav_link(next_post, "다음 글", "next")]),
        )
        (BLOG_DIR / f"{post['slug']}.html").write_text(page, encoding="utf-8")

    # index.html 글 목록 갱신
    index = INDEX.read_text(encoding="utf-8")
    cards = "\n".join(card(p) for p in posts)
    index, n = re.subn(
        r"<!-- BLOG:START -->.*?<!-- BLOG:END -->",
        lambda m: "<!-- BLOG:START -->\n" + cards + "\n          <!-- BLOG:END -->",
        index,
        flags=re.S,
    )
    if n != 1:
        sys.exit("index.html 에서 BLOG:START / BLOG:END 표시를 찾지 못했습니다.")
    INDEX.write_text(index, encoding="utf-8")
    print(f"완료: blog/ 에 {len(posts)}편 생성, index.html 목록 갱신 ({datetime.now():%H:%M})")


if __name__ == "__main__":
    main()
