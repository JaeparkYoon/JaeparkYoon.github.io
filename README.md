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
| 기술 블로그 | Medium 글을 옮겨 온 블로그 (`blog/`) |
| 연락처 | GitHub · Email |

## 기술 블로그 갱신

Medium에 새 글을 올린 뒤 아래 명령을 실행하면 `blog/` 글 페이지와 기술 블로그 탭 목록이 다시 만들어집니다.

```bash
python3 tools/build_blog.py
```

- 글 순서는 Medium 프로필과 같고, 작성일·분량은 표시하지 않습니다.
- 「제목 — 1」「제목 — 2」 같은 연재 글은 1편부터 붙여서 보여줍니다.
- 홈페이지에서 뺄 본문 이미지는 스크립트의 `REMOVE_FIGURES`에 등록합니다.
- 다시 그린 이미지로 바꿀 때는 `IMAGE_OVERRIDES`, 높이 제한 없이 원본 크기로 보여 줄 다이어그램은 `FULL_SIZE_IMAGES`에 등록합니다.
- 본문 이미지는 `assets/images/blog/<글 ID>/`에 내려받습니다.
- Medium 코드 임베드는 GitHub Gist 원본 코드로 바꿉니다. 비밀 Gist까지 찾으려면 `gh` CLI 로그인이 필요합니다.
- 각 글 페이지는 Medium 원문을 canonical로 지정합니다.

## 디렉터리 구조

```
JaeparkYoon.github.io/
├── .nojekyll                 # GitHub Pages Jekyll 처리 방지
├── index.html                # 탭 구성 포트폴리오
├── blog/                     # 기술 블로그 글 페이지 (tools/build_blog.py로 생성)
├── tools/build_blog.py       # Medium → 블로그 변환 스크립트
├── assets/
│   ├── css/style.css         # 라이트 테마 디자인 시스템
│   ├── js/main.js            # 탭 전환 · 모바일 메뉴 · 라이트박스
│   └── images/
│       ├── enopy/            # Enopy 아이콘·스토어 스크린샷·피처 그래픽
│       └── blog/             # 블로그 본문 이미지
└── README.md
```
