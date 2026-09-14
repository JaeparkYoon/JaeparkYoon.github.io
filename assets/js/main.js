/**
 * Jaepark Yoon Portfolio - SnapFolio Showcase & App Flow Simulator
 */

document.addEventListener("DOMContentLoaded", () => {
  initHeader();
  initSnapfolioCarousel();
  initScreenshotModal();
  initAppFlowSimulation();
});

/* ==========================================================================
   Header & Navigation
   ========================================================================== */
function initHeader() {
  const header = document.querySelector(".site-header");
  const navLinks = document.querySelectorAll(".nav-link");
  const sections = document.querySelectorAll("section[id]");
  const menuToggle = document.getElementById("mobileMenuToggle");
  const navList = document.getElementById("navLinks");

  if (menuToggle && navList) {
    menuToggle.addEventListener("click", () => {
      const open = navList.classList.toggle("open");
      menuToggle.setAttribute("aria-expanded", String(open));
      menuToggle.innerHTML = open
        ? '<i class="fa-solid fa-xmark"></i>'
        : '<i class="fa-solid fa-bars"></i>';
    });
    navList.querySelectorAll("a").forEach((a) =>
      a.addEventListener("click", () => {
        navList.classList.remove("open");
        menuToggle.setAttribute("aria-expanded", "false");
        menuToggle.innerHTML = '<i class="fa-solid fa-bars"></i>';
      })
    );
  }

  window.addEventListener("scroll", () => {
    if (window.scrollY > 30) {
      header.classList.add("scrolled");
    } else {
      header.classList.remove("scrolled");
    }

    // Scroll spy
    let current = "";
    sections.forEach((section) => {
      const sectionTop = section.offsetTop - 120;
      const sectionHeight = section.clientHeight;
      if (window.scrollY >= sectionTop && window.scrollY < sectionTop + sectionHeight) {
        current = section.getAttribute("id");
      }
    });

    navLinks.forEach((link) => {
      link.classList.remove("active");
      if (link.getAttribute("href") === `#${current}`) {
        link.classList.add("active");
      }
    });
  });
}

/* ==========================================================================
   SnapFolio Screenshot Carousel
   ========================================================================== */
function initSnapfolioCarousel() {
  const track = document.getElementById("snapfolioCarousel");
  const prevBtn = document.getElementById("carouselPrev");
  const nextBtn = document.getElementById("carouselNext");

  if (!track || !prevBtn || !nextBtn) return;

  const scrollAmount = 300;

  prevBtn.addEventListener("click", () => {
    track.scrollBy({ left: -scrollAmount, behavior: "smooth" });
  });

  nextBtn.addEventListener("click", () => {
    track.scrollBy({ left: scrollAmount, behavior: "smooth" });
  });
}

/* ==========================================================================
   Screenshot Lightbox Modal
   ========================================================================== */
function initScreenshotModal() {
  const modal = document.getElementById("screenshotModal");
  const modalImg = document.getElementById("modalImage");
  const closeBtn = document.querySelector(".modal-close-btn");
  const cards = document.querySelectorAll(".screenshot-card");
  const lightboxImgs = document.querySelectorAll("img[data-lightbox]");

  if (!modal || !modalImg) return;

  const openWith = (img) => {
    if (!img) return;
    modalImg.src = img.src;
    modalImg.alt = img.alt || "Screenshot Preview";
    modal.classList.add("open");
    document.body.style.overflow = "hidden";
  };

  cards.forEach((card) => {
    card.addEventListener("click", () => openWith(card.querySelector("img")));
  });

  lightboxImgs.forEach((img) => {
    img.addEventListener("click", () => openWith(img));
  });

  const closeModal = () => {
    modal.classList.remove("open");
    document.body.style.overflow = "";
  };

  if (closeBtn) closeBtn.addEventListener("click", closeModal);

  modal.addEventListener("click", (e) => {
    if (e.target === modal) {
      closeModal();
    }
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && modal.classList.contains("open")) {
      closeModal();
    }
  });
}

/* ==========================================================================
   SnapFolio App Flow Simulation
   ========================================================================== */
const FLOW_STEPS = [
  {
    step: 0,
    badge: "STEP 01",
    title: "홈 대시보드 (통합 자산 현황)",
    img: "assets/images/snapfolio/01-screenshot.png",
    body: "앱 진입 시 가장 먼저 보이는 메인 화면입니다. 총 보유 자산, 전일 대비 변동, 올해 누적 수익률(YTD), 카테고리별 자산 비중 도넛 차트, 보유 종목 리스트, 월간 배당금 요약이 하나의 스크롤에 직관적으로 정리됩니다.",
    techTags: [
      { icon: "fa-layer-group", text: "ObserveHomeDataUseCase" },
      { icon: "fa-database", text: "Room KMP StateFlow" },
      { icon: "fa-palette", text: "Compose M3 LazyColumn" },
    ],
  },
  {
    step: 1,
    badge: "STEP 02",
    title: "스크린샷 일괄 업로드 & AI 분석",
    img: "assets/images/snapfolio/02-screenshot.png",
    body: "증권사(키움, 토스, 미래에셋 등) 계좌 스크린샷을 최대 5장까지 동시 선택합니다. 백그라운드 서비스에서 ML Kit OCR 전처리와 Gemini Flash-Lite 모델이 결합되어 종목명, 수량, 매입단가, 평가금액을 실시간 자동 파싱합니다.",
    techTags: [
      { icon: "fa-robot", text: "Gemini Flash-Lite" },
      { icon: "fa-eye", text: "ML Kit Korean OCR" },
      { icon: "fa-gears", text: "Foreground Upload Service" },
    ],
  },
  {
    step: 2,
    badge: "STEP 03",
    title: "AI 포트폴리오 질의응답 (대화형 코치)",
    img: "assets/images/snapfolio/03-screenshot.png",
    body: "Gemini AI 모델이 사용자의 실제 포트폴리오 구조를 기반으로 자산 리스크와 섹터 편중도를 진단합니다. '현재 포트폴리오의 리밸런싱 방향은?', '배당 재투자 효과는?' 같은 질문에 실시간 스트리밍 대화로 구체적인 답변을 제공합니다.",
    techTags: [
      { icon: "fa-comments", text: "Vertex AI Streaming SDK" },
      { icon: "fa-coins", text: "Server Credit Verification" },
      { icon: "fa-code-branch", text: "MVI Unidirectional State" },
    ],
  },
  {
    step: 3,
    badge: "STEP 04",
    title: "시계열 자산 추이 & 카테고리 기여도",
    img: "assets/images/snapfolio/04-screenshot.png",
    body: "1일, 1주일, 1개월, 3개월, 1년, 전체 등 8개 구간의 인터랙티브 차트를 제공합니다. 드래그 Hover를 통해 특정 시점의 평가액을 정밀하게 확인하고, 국내주식·해외주식·예적금 등 카테고리별 수익 기여도를 시각적으로 추적합니다.",
    techTags: [
      { icon: "fa-chart-line", text: "ObserveTrendDataUseCase" },
      { icon: "fa-clock-rotate-left", text: "Portfolio Snapshot DB" },
      { icon: "fa-mobile", text: "Smooth Drag Gesture Canvas" },
    ],
  },
  {
    step: 4,
    badge: "STEP 05",
    title: "배당 캘린더 & 시장 지표 분석",
    img: "assets/images/snapfolio/05-screenshot.png",
    body: "보유 종목의 월별 예상 배당금과 연간 배당 수익률을 자동 산출합니다. 또한 미국 FRED 시장 지표 프록시 연동 및 워런 버핏 등 글로벌 투자 대가의 포트폴리오와 내 자산을 비교해 볼 수 있는 실험실(Lab) 기능을 지원합니다.",
    techTags: [
      { icon: "fa-calendar-days", text: "Dividend Calculation Engine" },
      { icon: "fa-server", text: "FRED & ECOS Cloud Proxy" },
      { icon: "fa-flask", text: "Investment Lab Simulation" },
    ],
  },
  {
    step: 5,
    badge: "STEP 06",
    title: "로컬 퍼스트 보안 & 커스텀 설정",
    img: "assets/images/snapfolio/06-screenshot.png",
    body: "라이트/다크 테마 전환, 4가지 감성 액센트 컬러 프리셋(Salmon, Terracotta, Coral, Burgundy), 금액 숨김 모드, CSV 내보내기/가져오기를 완벽 지원합니다. 모든 금융 데이터는 외부 서버가 아닌 기기 로컬에 안전하게 보관됩니다.",
    techTags: [
      { icon: "fa-shield-halved", text: "Local-First Room KMP" },
      { icon: "fa-sliders", text: "DataStore Preferences" },
      { icon: "fa-file-csv", text: "CSV Backup & Restore" },
    ],
  },
];

function initAppFlowSimulation() {
  const stepBtns = document.querySelectorAll(".flow-step-btn");
  const stepDots = document.querySelectorAll(".step-dot");
  const screenImg = document.getElementById("simScreenImg");
  const badgeEl = document.getElementById("flowDetailBadge");
  const titleEl = document.getElementById("flowDetailTitle");
  const bodyEl = document.getElementById("flowDetailBody");

  if (!stepBtns.length || !screenImg) return;

  function setStep(index) {
    const data = FLOW_STEPS[index];
    if (!data) return;

    // Active button state
    stepBtns.forEach((btn, i) => {
      btn.classList.toggle("active", i === index);
    });

    // Active dot state
    stepDots.forEach((dot, i) => {
      dot.classList.toggle("active", i === index);
    });

    // Animate screen image transition
    screenImg.style.opacity = "0.3";
    screenImg.style.transform = "scale(0.97)";
    setTimeout(() => {
      screenImg.src = data.img;
      screenImg.alt = data.title;
      screenImg.style.opacity = "1";
      screenImg.style.transform = "scale(1)";
    }, 150);

    // Update detail card
    if (badgeEl) badgeEl.textContent = data.badge;
    if (titleEl) titleEl.textContent = data.title;

    if (bodyEl) {
      let tagsHtml = data.techTags
        .map(
          (t) =>
            `<span class="detail-tech-tag"><i class="fa-solid ${t.icon}"></i> ${t.text}</span>`
        )
        .join("");

      bodyEl.innerHTML = `
        <p>${data.body}</p>
        <div class="flow-detail-tech">${tagsHtml}</div>
      `;
    }
  }

  // Step button click listeners
  stepBtns.forEach((btn, idx) => {
    btn.addEventListener("click", () => setStep(idx));
  });

  // Step dots click listeners
  stepDots.forEach((dot, idx) => {
    dot.addEventListener("click", () => setStep(idx));
  });
}
