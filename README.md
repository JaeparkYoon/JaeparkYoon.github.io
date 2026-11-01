# JaeparkYoon.github.io

윤재박(Jaepark Yoon) 개발자의 포트폴리오 웹사이트입니다.

👉 **웹사이트 바로가기**: [https://jaeparkyoon.github.io](https://jaeparkyoon.github.io)

---

## 구성

포트폴리오 PDF 내용 중 공개 가능한 부분을 탭별 페이지로 구성했습니다. 상단 탭을 누르면 해당 섹션만 보입니다(`#career`, `#enopy`, `#writing`, `#contact`).

| 탭 | 내용 |
| --- | --- |
| 경력 | 이스트에이드(구 줌인터넷) · 에듀윌 · 이우솔루션 — 총 6년 3개월 |
| 사이드 프로젝트 | Enopy(에노피) 서비스 소개 — 만든 이유, 이름의 의미, 핵심 화면 6개와 기획 포인트, 기획하며 내린 결정 |
| 기술 블로그 | Medium에서 옮겨 온 글 8편 (`blog/`) |
| 연락처 | GitHub · Email |

## 기술 블로그

Medium 블로그는 삭제했고(2026-11-01), 글 8편은 이 사이트로 옮겨 왔습니다. 글 원본은 삭제 전에 받아 둔 사본 `tools/medium-export.xml`이 유일합니다 — **지우지 마세요.**

아래 명령을 실행하면 사본으로 `blog/` 글 페이지와 기술 블로그 탭 목록을 다시 만듭니다. 글 표시 방식이나 아래 설정을 바꾼 뒤에 실행합니다.

```bash
python3 tools/build_blog.py
```

- 글 순서는 Medium 프로필 순서를 따르고, 작성일·분량은 표시하지 않습니다.
- 「제목 — 1」「제목 — 2」 같은 연재 글은 1편부터 붙여서 보여줍니다.
- 홈페이지에서 뺄 본문 이미지는 스크립트의 `REMOVE_FIGURES`에 등록합니다.
- 다른 제목으로 보여 줄 글은 `TITLE_OVERRIDES`에 등록합니다.
- 다시 그린 이미지로 바꿀 때는 `IMAGE_OVERRIDES`, 높이 제한 없이 원본 크기로 보여 줄 다이어그램은 `FULL_SIZE_IMAGES`에 등록합니다.
- 본문 이미지는 `assets/images/blog/<글 ID>/`에 들어 있습니다. Medium 이미지 서버에서 다시 받을 수 있다는 보장이 없으니 **이 폴더도 지우지 마세요.**
- 코드 블록은 GitHub Gist 원본 코드에서 가져옵니다. 비밀 Gist까지 찾으려면 `gh` CLI 로그인이 필요합니다.

## 디렉터리 구조

```
JaeparkYoon.github.io/
├── .nojekyll                 # GitHub Pages Jekyll 처리 방지
├── index.html                # 탭 구성 포트폴리오
├── blog/                     # 기술 블로그 글 페이지 (tools/build_blog.py로 생성)
├── tools/build_blog.py       # 블로그 글 페이지 생성 스크립트
├── tools/medium-export.xml   # 삭제한 Medium 블로그의 글 원본 사본
├── assets/
│   ├── css/style.css         # 라이트 테마 디자인 시스템
│   ├── js/main.js            # 탭 전환 · 모바일 메뉴 · 라이트박스
│   └── images/
│       ├── enopy/            # Enopy 아이콘·스토어 스크린샷·피처 그래픽
│       └── blog/             # 블로그 본문 이미지
└── README.md
```
