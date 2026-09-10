# JaeparkYoon.github.io

윤재박(Jaepark Yoon) 개발자의 공식 포트폴리오 및 프로젝트 쇼케이스 웹사이트입니다.

👉 **웹사이트 바로가기**: [https://jaeparkyoon.github.io](https://jaeparkyoon.github.io)

---

## 🌟 수록 프로젝트

### 1. [SnapFolio (스냅폴)](https://github.com/JaeparkYoon/SnapFolio)
- **개요**: "스크린샷 한 장으로 흩어진 투자 자산을 모으다."
- **기술 스택**: Kotlin Multiplatform, Jetpack Compose (M3), SwiftUI 5, Gemini 3.1 Flash-Lite AI, Room KMP, Firebase Cloud Functions
- **특징**:
  - 증권사 계좌 캡처 스크린샷 5장 동시 업로드 & Gemini AI 자동 파싱
  - 실시간 자산 대시보드, 8개 구간 시계열 차트, 월별/연간 배당금 예측
  - Gemini AI 포트폴리오 진단 & 리밸런싱 질의응답 챗
  - 민감 정보 로컬 Room DB 격리 (Local-First 프라이버시)

### 2. [Tactics RPG (NewGame)](https://github.com/JaeparkYoon/NewGame)
- **개요**: 축구 리그·구단 운영 시스템을 본뜬 7v7 그리드 전술 RPG
- **기술 스택**: Kotlin Multiplatform (Deterministic Core), Unity 6 (Universal 2D), C-ABI Native Bridge (.bundle / .xcframework / .aar), Python Simulator
- **특징**:
  - 5열 × 7행 전장, 120틱(2분 30초) 자동 전투 & 3대 감독 지시 카드(집결/총력수비/돌파) 실시간 개입
  - FM 스타일 구단 및 시즌 루프 (유스 발굴, 시설 투자, 컨디션 로테이션, AI 이적)
  - 100% 결정론적 연산 (Zero Float, Pure Integer Math, xorshift64* 시드 난수로 리플레이 바이트 일치)
  - Python 시뮬레이터 실측 검증 후 KMP 1:1 이식 (골든 테스트 30경기 / 3시즌 / 평점 100% 패리티)
  - **웹사이트 내 5×7 인터랙티브 전술판 시뮬레이터 제공**

---

## 🚀 GitHub Pages 배포 방법

GitHub Pages는 저장소 이름이 `JaeparkYoon.github.io`일 때 루트 브랜치(`main`)의 파일들을 자동으로 웹 서비스로 배포합니다.

### 1. GitHub에서 저장소 생성
1. [GitHub New Repository](https://github.com/new) 페이지로 이동합니다.
2. Repository name에 정확히 **`JaeparkYoon.github.io`** 를 입력합니다.
3. **Public**으로 설정하고 생성을 완료합니다.

### 2. 로컬에서 원격으로 푸시
터미널에서 아래 명령어를 실행합니다:

```bash
cd /Users/estaid_1/Android-Projects/github/JaeparkYoon.github.io
git push -u origin main
```

푸시 후 1~2분 뒤 `https://jaeparkyoon.github.io`로 접속하면 웹사이트가 활성화됩니다!

---

## 📁 디렉터리 구조

```
JaeparkYoon.github.io/
├── .nojekyll                 # GitHub Pages Jekyll 처리 방지
├── index.html                # 메인 포트폴리오 웹페이지
├── assets/
│   ├── css/
│   │   └── style.css         # 다크 테마 디자인 시스템 & 반응형 스타일
│   ├── js/
│   │   └── main.js           # 5x7 전술판 인터랙티브 시뮬레이터 & 캐러셀
│   └── images/
│       └── snapfolio/        # 실제 Play Store 스크린샷 및 앱 아이콘
└── README.md
```
