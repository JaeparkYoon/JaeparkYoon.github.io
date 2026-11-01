#!/usr/bin/env python3
"""
Medium에서 옮겨 온 글을 홈페이지 블로그 페이지로 만든다.

  python3 tools/build_blog.py                                # 글 페이지·목록 생성
  python3 tools/build_blog.py new <글 주소> "<제목>"           # 새 글 파일 만들기

- 새 글은 posts/<글 주소>.md 에 Markdown 으로 쓴다(이름이 _ 로 시작하면 제외).
  머리말 title·date 필수. date 는 목록 순서에만 쓰고 화면에는 표시하지 않는다.

- Medium 블로그는 삭제됐다(2026-11-01). 글 원본은 삭제 전에 받아 둔 RSS 사본
  tools/medium-export.xml 이 유일한 소스다 — 지우지 말 것.
- 사본의 글 본문으로 blog/<post id>.html 을 생성
  (글 순서는 Medium 프로필과 같았던 피드 순서를 따르되, "제목 — 1", "제목 — 2" 같은
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
EXPORT = Path(__file__).resolve().parent / "medium-export.xml"
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
    "https://cdn-images-1.medium.com/max/428/1*ZGBSmG7mwcOpZXz75jzU9g.png": "ime-lifecycle.svg",  # InputMethodService 생명주기 (SVG로 다시 그림)
}

# 세로로 긴 다이어그램처럼 높이 제한(480px) 없이 원본 크기로 보여 줄 이미지: Medium 이미지 주소 목록
FULL_SIZE_IMAGES = {
    "https://cdn-images-1.medium.com/max/428/1*ZGBSmG7mwcOpZXz75jzU9g.png",  # InputMethodService 생명주기 다이어그램
}

# Medium 제목과 다르게 보여 줄 제목: 글 ID -> 홈페이지 제목
TITLE_OVERRIDES = {
    "35e5b2344a2b": "Android Keyboard의 InputMethodService Lifecycle 분석 내용 기록",
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
        cls = ' class="full-size"' if src in FULL_SIZE_IMAGES else ""
        if src in IMAGE_OVERRIDES:
            return f'<img src="../assets/images/blog/{slug}/{IMAGE_OVERRIDES[src]}" alt="{alt}" loading="lazy"{cls} />'
        ext = Path(src.split("?")[0]).suffix.lower()
        if ext not in (".png", ".jpg", ".jpeg", ".gif", ".webp"):
            ext = ".png"
        name = hashlib.md5(src.encode()).hexdigest()[:12] + ext
        path = target / name
        if not path.exists():
            target.mkdir(parents=True, exist_ok=True)
            path.write_bytes(fetch(src))
        return f'<img src="../assets/images/blog/{slug}/{name}" alt="{alt}" loading="lazy"{cls} />'

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


# ---------------------------------------------------------------------------
# 새 글: posts/<글 주소>.md (Markdown) -> 기존 글과 같은 글 페이지
# ---------------------------------------------------------------------------

POSTS_DIR = ROOT / "posts"

NEW_POST_TEMPLATE = """---
title: {title}
date: {date}
---

글의 첫 문단은 기술 블로그 목록 카드의 소개 문구로도 쓰입니다.

## 소제목

본문 문단입니다. **굵게**, *기울임*, `인라인 코드`, [링크](https://developer.android.com)를 쓸 수 있습니다.
한 문단 안에서 줄을 바꾸면 그대로 줄바꿈됩니다.

### 작은 소제목

- 목록 항목
- 목록 항목

1. 순서 있는 목록
2. 순서 있는 목록

> 인용문입니다.

![이미지 설명](sample.png "이미지 아래에 보일 캡션")

```kotlin title="MainActivity.kt"
fun main() {{
    println("코드 블록")
}}
```
"""


def inline_md(text):
    """한 줄 안의 Markdown(코드·굵게·기울임·링크)을 HTML 로 바꾼다."""
    codes = []

    def keep_code(m):
        codes.append(f"<code>{html.escape(m.group(1))}</code>")
        return f"\x00{len(codes) - 1}\x00"

    text = re.sub(r"`([^`]+)`", keep_code, text)
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", text)

    def link(m):
        label, href = m.group(1), m.group(2)
        external = href.startswith("http")
        attrs = ' target="_blank" rel="noopener noreferrer"' if external else ""
        return f'<a href="{html.escape(href)}"{attrs}>{label}</a>'

    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, text)
    return re.sub(r"\x00(\d+)\x00", lambda m: codes[int(m.group(1))], text)


def markdown_to_html(md, slug):
    """posts/*.md 본문을 기존 글 본문과 같은 HTML 구조로 바꾼다."""
    out, para = [], []
    lines = md.splitlines()
    i = 0

    def flush():
        if para:
            out.append("<p>" + "<br>".join(inline_md(l) for l in para) + "</p>")
            para.clear()

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        fence = re.match(r"```(\w+)?(?:\s+title=\"([^\"]+)\")?\s*$", stripped)
        if fence:
            flush()
            code = []
            i += 1
            while i < len(lines) and lines[i].strip() != "```":
                code.append(lines[i])
                i += 1
            out.append(code_block("\n".join(code), (fence.group(1) or "").lower(), fence.group(2)))
            i += 1
            continue

        if not stripped:
            flush()
            i += 1
            continue

        heading = re.match(r"(#{2,3})\s+(.*)", stripped)
        if heading:
            flush()
            tag = "h3" if len(heading.group(1)) == 2 else "h4"
            out.append(f"<{tag}>{inline_md(heading.group(2))}</{tag}>")
            i += 1
            continue

        image = re.match(r'!\[([^\]]*)\]\(([^)\s]+)(?:\s+"([^"]*)")?\)\s*(\{full\})?$', stripped)
        if image:
            flush()
            alt, src, caption, full = image.groups()
            if not src.startswith(("http", "/", "../")):
                src = f"../assets/images/blog/{slug}/{src}"
            cls = ' class="full-size"' if full else ""
            cap = f"<figcaption>{inline_md(caption)}</figcaption>" if caption else ""
            out.append(f'<figure><img src="{html.escape(src)}" alt="{html.escape(alt)}" loading="lazy"{cls} />{cap}</figure>')
            i += 1
            continue

        if stripped.startswith(">"):
            flush()
            quote = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote.append(inline_md(lines[i].strip()[1:].strip()))
                i += 1
            out.append("<blockquote>" + "<br>".join(quote) + "</blockquote>")
            continue

        bullet = re.match(r"([-*]|\d+\.)\s+", stripped)
        if bullet:
            flush()
            tag = "ol" if bullet.group(1)[0].isdigit() else "ul"
            items = []
            while i < len(lines) and re.match(r"([-*]|\d+\.)\s+", lines[i].strip()):
                items.append("<li>" + inline_md(re.sub(r"^([-*]|\d+\.)\s+", "", lines[i].strip())) + "</li>")
                i += 1
            out.append(f"<{tag}>" + "".join(items) + f"</{tag}>")
            continue

        para.append(stripped)
        i += 1

    flush()
    return "".join(out)


def load_markdown_posts():
    """posts/*.md (이름이 _ 로 시작하는 파일 제외)를 읽는다. 날짜 최신순."""
    posts = []
    for path in sorted(POSTS_DIR.glob("*.md")):
        if path.name.startswith("_"):
            continue
        text = path.read_text(encoding="utf-8")
        m = re.match(r"---\n(.*?)\n---\n(.*)", text, flags=re.S)
        if not m:
            sys.exit(f"{path.name}: 맨 위에 --- 로 감싼 title·date 머리말이 필요합니다.")
        meta = dict(
            (k.strip(), v.strip()) for k, v in
            (line.split(":", 1) for line in m.group(1).splitlines() if ":" in line)
        )
        if not meta.get("title") or not meta.get("date"):
            sys.exit(f"{path.name}: 머리말에 title 과 date 가 모두 있어야 합니다.")
        slug = path.stem
        posts.append({
            "id": slug,
            "slug": slug,
            "title": meta["title"],
            "date": meta["date"],
            "body": markdown_to_html(m.group(2), slug),
        })
    # 작성일은 화면에 표시하지 않고 목록 순서에만 쓴다
    return sorted(posts, key=lambda p: p["date"], reverse=True)


def new_post(slug, title):
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", slug):
        sys.exit("글 주소는 영문 소문자·숫자·하이픈만 씁니다. 예: ime-keyboard-tips")
    path = POSTS_DIR / f"{slug}.md"
    if path.exists():
        sys.exit(f"{path.relative_to(ROOT)} 가 이미 있습니다.")
    POSTS_DIR.mkdir(exist_ok=True)
    path.write_text(NEW_POST_TEMPLATE.format(title=title, date=datetime.now().strftime("%Y-%m-%d")), encoding="utf-8")
    (IMAGE_DIR / slug).mkdir(parents=True, exist_ok=True)
    print(f"새 글을 만들었습니다: {path.relative_to(ROOT)}")
    print(f"이미지는 {(IMAGE_DIR / slug).relative_to(ROOT)}/ 에 넣고 본문에서 파일 이름으로 씁니다.")


POST_TEMPLATE = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} — 윤재박 기술 블로그</title>
  <meta name="description" content="{description}" />
  <meta name="author" content="Jaepark Yoon" />
  <link rel="canonical" href="https://jaeparkyoon.github.io/blog/{slug}.html" />

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
    xml = EXPORT.read_bytes()
    items = ET.fromstring(xml).findall("channel/item")
    print(f"Medium 에서 옮겨 온 글 {len(items)}편")

    gists = load_gists()
    print(f"Gist 코드 {len({id(v) for v in gists.values()})}개")

    medium_posts = []
    for item in items:
        link = item.findtext("link")
        medium_posts.append({
            "id": post_id(link),
            "slug": post_id(link),
            "title": TITLE_OVERRIDES.get(post_id(link), item.findtext("title").strip()),
            "raw": item.find("content:encoded", NS).text,
        })

    # 새 글(posts/*.md)이 위, Medium 에서 옮겨 온 글이 아래
    markdown_posts = load_markdown_posts()
    print(f"새 글 {len(markdown_posts)}편")
    posts = group_series(markdown_posts + medium_posts)
    local_links = {p["id"]: p["slug"] for p in posts}

    BLOG_DIR.mkdir(exist_ok=True)
    for i, post in enumerate(posts):
        print(f"- {post['title']}")
        if "body" in post:
            body = post["body"]
        else:
            body = convert(post["raw"], post["slug"], gists, local_links)
        post["excerpt"] = excerpt(body)
        # 이전/다음 글은 목록 순서를 따른다
        prev_post = posts[i - 1] if i > 0 else None
        next_post = posts[i + 1] if i + 1 < len(posts) else None
        page = POST_TEMPLATE.format(
            title=html.escape(post["title"]),
            description=html.escape(post["excerpt"]),
            slug=post["slug"],
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
    if len(sys.argv) >= 2 and sys.argv[1] == "new":
        if len(sys.argv) != 4:
            sys.exit('사용법: python3 tools/build_blog.py new <글 주소> "<제목>"')
        new_post(sys.argv[2], sys.argv[3])
    else:
        main()
