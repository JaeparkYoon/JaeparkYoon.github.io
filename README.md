# JaeparkYoon.github.io

윤재박(Jaepark Yoon) 개발자의 공식 포트폴리오 웹사이트입니다.

👉 **웹사이트 바로가기**: [https://jaeparkyoon.github.io](https://jaeparkyoon.github.io)

---

## 🌟 대표 프로젝트: [SnapFolio (스냅폴)](https://github.com/JaeparkYoon/SnapFolio)

> **"스크린샷 한 장으로 흩어진 투자 자산을 모으다."**  
> Kotlin Multiplatform · Gemini AI · 100% 바이브 코딩 창작물

### 🚀 핵심 기능 및 기술 하이라이트
- **스크린샷 AI 자동 파싱**: 증권사 계좌 캡처 최대 5장 동시 업로드 → Gemini 3.1 Flash-Lite AI & ML Kit OCR로 종목/수량/단가 자동 추출
- **통합 자산 대시보드**: 총자산, 일간 변동, YTD 수익률, 카테고리별 비중 도넛 차트, 배당금 요약
- **Gemini AI 자산 진단 챗**: Firebase Vertex AI SDK 기반 실시간 스트리밍 대화형 포트폴리오 분석 및 리밸런싱 조언
- **시계열 추이 & 차트**: 1일~전체 8개 구간 인터랙티브 차트 및 카테고리별 기여도 분석
- **로컬 퍼스트 & 완벽한 프라이버시**: 민감 금융 원장은 기기 내부 Room KMP(SQLite) 암호화 저장, 계좌번호 자동 마스킹
- **인앱 결제 연동**: Google Play Billing 9.1 & Apple StoreKit 2 + Cloud Functions 서버 사이드 영수증 검증

### 📱 웹사이트 인터랙티브 앱 흐름 시뮬레이션
웹사이트에서 실제 서비스 캡처 화면 6단계와 단계별 아키텍처 원리를 직접 클릭하며 확인할 수 있는 **폰 목업 시뮬레이터**를 제공합니다.

---

## 📁 디렉터리 구조

```
JaeparkYoon.github.io/
├── .nojekyll                 # GitHub Pages Jekyll 처리 방지
├── index.html                # 라이트 테마 싱글 페이지 포트폴리오
├── assets/
│   ├── css/
│   │   └── style.css         # 모던 라이트 테마 디자인 시스템 & 폰 목업 스타일
│   ├── js/
│   │   └── main.js           # 6단계 앱 흐름 인터랙티브 시뮬레이터 & 캐러셀
│   └── images/
│       └── snapfolio/        # 실제 Play Store 스크린샷 및 앱 아이콘
└── README.md
```
