/**
 * Jaepark Yoon Portfolio - Interactive Script
 * Features:
 *  - Header blur & active scroll navigation
 *  - Project filter switcher
 *  - SnapFolio screenshot carousel & modal lightbox
 *  - Tactics RPG 5x7 interactive formation visualizer & simulation stats
 */

document.addEventListener("DOMContentLoaded", () => {
  initHeader();
  initProjectSwitcher();
  initSnapfolioCarousel();
  initScreenshotModal();
  initTacticsSimulator();
});

/* ==========================================================================
   Header & Navigation
   ========================================================================== */
function initHeader() {
  const header = document.querySelector(".site-header");
  const navLinks = document.querySelectorAll(".nav-link");
  const sections = document.querySelectorAll("section[id]");

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
   Project Switcher / Filter Tabs
   ========================================================================== */
function initProjectSwitcher() {
  const tabs = document.querySelectorAll(".switch-tab");
  const projectSections = document.querySelectorAll(".project-section");

  tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      tabs.forEach((t) => t.classList.remove("active"));
      tab.classList.add("active");

      const filter = tab.getAttribute("data-target");

      if (filter === "all") {
        projectSections.forEach((sec) => (sec.style.display = "block"));
      } else {
        projectSections.forEach((sec) => {
          if (sec.id === filter) {
            sec.style.display = "block";
            // Scroll to the selected project smoothly
            sec.scrollIntoView({ behavior: "smooth" });
          } else {
            sec.style.display = "none";
          }
        });
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

  if (!modal || !modalImg) return;

  cards.forEach((card) => {
    card.addEventListener("click", () => {
      const img = card.querySelector("img");
      if (img) {
        modalImg.src = img.src;
        modalImg.alt = img.alt || "Screenshot Preview";
        modal.classList.add("open");
        document.body.style.overflow = "hidden";
      }
    });
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
   Tactics RPG - 5x7 Interactive Tactical Pitch Simulator
   ========================================================================== */
const FORMATIONS = {
  standard: {
    name: "표준 2-3-2 (Standard Balanced)",
    code: "2-3-2",
    winRate: "56%",
    winRateClass: "success",
    structure: "DF 2 · MF 3 · FW 2 (합 7명)",
    tacticalDepth: "3단 2-3-2 / 4단 2-3-0-2",
    description:
      "공수 밸런스가 균형 잡힌 정석 진형. 중앙 3열과 양 측면의 공간 점유율이 고르고 국지전 대인 방어에 안정적입니다. 18종 기본 포지션 조합 중 가장 표준적인 전투 양상을 보입니다.",
    bestCard: "집결 (Rally)",
    weakness: "극단적 측면 기습 시 커버 동선 필요",
    placements: [
      // row: 0~6 (0: home def, 1: home mid, 2: home att)
      // col: 0~4 (0: L-Wing, 1: L-Half, 2: Center, 3: R-Half, 4: R-Wing)
      { row: 0, col: 1, role: "DF", pos: "CB-L" },
      { row: 0, col: 3, role: "DF", pos: "CB-R" },
      { row: 1, col: 0, role: "MF", pos: "LM" },
      { row: 1, col: 2, role: "MF", pos: "CM" },
      { row: 1, col: 4, role: "MF", pos: "RM" },
      { row: 2, col: 1, role: "FW", pos: "CF-L" },
      { row: 2, col: 3, role: "FW", pos: "CF-R" },
    ],
  },
  dispersion: {
    name: "측면 분산 (Flank Dispersion)",
    code: "2-1-4",
    winRate: "57%",
    winRateClass: "success",
    structure: "DF 2 · MF 1 · FW 4 (측면 우회 극대화)",
    tacticalDepth: "양 측면 2 · 중앙 1 · 하프 각 1",
    description:
      "시뮬레이터 3성 실측 평균 승률 1위(57%). 가로로 넓게 서서 상대 중앙 밀집 수비를 우회하고 넥서스를 타격합니다. 세로 쌓기를 피해 1v1 교전 효율을 극대화한 현대적 전술입니다.",
    bestCard: "돌파 지시 (Breakthrough)",
    weakness: "중앙 1선 차단 시 후방 노출 위험",
    placements: [
      { row: 0, col: 0, role: "DF", pos: "LB" },
      { row: 0, col: 4, role: "DF", pos: "RB" },
      { row: 1, col: 2, role: "MF", pos: "CAM" },
      { row: 2, col: 0, role: "FW", pos: "LW" },
      { row: 2, col: 1, role: "FW", pos: "LF" },
      { row: 2, col: 3, role: "FW", pos: "RF" },
      { row: 2, col: 4, role: "FW", pos: "RW" },
    ],
  },
  halfspace: {
    name: "하프스페이스 집중 (Halfspace Overload)",
    code: "2-3-2",
    winRate: "53%",
    winRateClass: "success",
    structure: "DF 2 · MF 3 · FW 2 (1·3열 집중)",
    tacticalDepth: "하프스페이스(Col 1, 3) 각 2명",
    description:
      "축구의 핵심 전술 구역인 하프스페이스(1열·3열)에 4명을 배치하여 상대 수비선 사이 틈새를 정밀 공략합니다. 중앙 장악력이 우수하며 안정적인 중원 압박을 구사합니다.",
    bestCard: "총력 수비 (Full Defense)",
    weakness: "극단적 와이드 윙어 상대 시 측면 공간 허용",
    placements: [
      { row: 0, col: 1, role: "DF", pos: "CB-L" },
      { row: 0, col: 3, role: "DF", pos: "CB-R" },
      { row: 1, col: 1, role: "MF", pos: "LCM" },
      { row: 1, col: 2, role: "MF", pos: "CM" },
      { row: 1, col: 3, role: "MF", pos: "RCM" },
      { row: 2, col: 1, role: "FW", pos: "SS-L" },
      { row: 2, col: 3, role: "FW", pos: "SS-R" },
    ],
  },
  leftbiased: {
    name: "좌편중 진형 (Left-Overload Risk)",
    code: "2-3-2 (좌쏠림)",
    winRate: "36%",
    winRateClass: "danger",
    structure: "좌측 3열 전원 밀집 (우측 2열 방치)",
    tacticalDepth: "Col 0~2 집중 / Col 3~4 공백",
    description:
      "좌측 국지전에서 일시적 수적 우위를 점하지만, 우측 2개 열(하프/플랭크)을 완전히 내어주어 상대의 반대편 넥서스 직접 타격에 무방비로 노출됩니다 (실측 승률 36% 급감).",
    bestCard: "비추천 (극단적 도박 진형)",
    weakness: "반대편 광역 침투에 무조건 넥서스 실점",
    placements: [
      { row: 0, col: 0, role: "DF", pos: "LB" },
      { row: 0, col: 1, role: "DF", pos: "CB" },
      { row: 1, col: 0, role: "MF", pos: "LM" },
      { row: 1, col: 1, role: "MF", pos: "LCM" },
      { row: 1, col: 2, role: "MF", pos: "CM" },
      { row: 2, col: 0, role: "FW", pos: "LW" },
      { row: 2, col: 1, role: "FW", pos: "CF" },
    ],
  },
  centerstack: {
    name: "중앙 세로 쌓기 (Central Stack - 최악)",
    code: "3-1-3 (세로 정체)",
    winRate: "35%",
    winRateClass: "danger",
    structure: "중앙 2열에 3명 집중 + 좁은 간격",
    tacticalDepth: "중앙 열 3명 중첩 배치",
    description:
      "셀 정원(1칸 1명) 및 인접 협동 규칙상, 세로로 쌓은 유닛은 맨 앞 1명만 교전하고 뒷선 유닛이 병목되어 화력을 낭비합니다. 실측 결과 최악의 승률(35%)을 기록한 실패 진형입니다.",
    bestCard: "전술 수정 필수 (교체 즉시 실행)",
    weakness: "단일 열 병목 현상 및 양 날개 무력화",
    placements: [
      { row: 0, col: 2, role: "DF", pos: "CB" },
      { row: 0, col: 1, role: "DF", pos: "LB" },
      { row: 0, col: 3, role: "DF", pos: "RB" },
      { row: 1, col: 2, role: "MF", pos: "CM" },
      { row: 2, col: 2, role: "FW", pos: "CF" },
      { row: 1, col: 1, role: "MF", pos: "LM" },
      { row: 1, col: 3, role: "MF", pos: "RM" },
    ],
  },
};

function initTacticsSimulator() {
  const pitch = document.getElementById("tacticalPitch");
  const buttons = document.querySelectorAll(".formation-btn");
  if (!pitch || buttons.length === 0) return;

  // Generate 5 cols x 7 rows pitch cells
  pitch.innerHTML = "";
  for (let r = 0; r < 7; r++) {
    for (let c = 0; c < 5; c++) {
      const cell = document.createElement("div");
      cell.className = "pitch-cell";
      cell.dataset.row = r;
      cell.dataset.col = c;

      // Assign visual zone style
      if (r === 0) cell.classList.add("zone-home-def");
      else if (r === 1) cell.classList.add("zone-home-mid");
      else if (r === 2) cell.classList.add("zone-home-att");

      pitch.appendChild(cell);
    }
  }

  // Render initial formation
  renderFormation("standard");

  buttons.forEach((btn) => {
    btn.addEventListener("click", () => {
      buttons.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      const key = btn.dataset.formation;
      renderFormation(key);
    });
  });
}

function renderFormation(key) {
  const data = FORMATIONS[key];
  if (!data) return;

  // Clear existing tokens
  document.querySelectorAll(".player-token").forEach((t) => t.remove());

  // Render tokens on the 5x7 grid
  data.placements.forEach((p) => {
    const cell = document.querySelector(
      `.pitch-cell[data-row="${p.row}"][data-col="${p.col}"]`
    );
    if (cell) {
      const token = document.createElement("div");
      token.className = `player-token token-${p.role.toLowerCase()}`;
      token.innerHTML = `
        <span class="token-role">${p.role}</span>
        <span class="token-pos">${p.pos}</span>
      `;
      cell.appendChild(token);
    }
  });

  // Update Report Panel
  const reportName = document.getElementById("reportFormationName");
  const reportWinrate = document.getElementById("reportWinRate");
  const reportDesc = document.getElementById("reportDesc");
  const reportStructure = document.getElementById("reportStructure");
  const reportTactics = document.getElementById("reportTactics");
  const reportCard = document.getElementById("reportBestCard");
  const reportWeakness = document.getElementById("reportWeakness");

  if (reportName) reportName.textContent = data.name;
  if (reportWinrate) {
    reportWinrate.textContent = `평균 승률 ${data.winRate}`;
    reportWinrate.className = `report-stat-pill ${data.winRateClass === "danger" ? "danger" : ""}`;
  }
  if (reportDesc) reportDesc.textContent = data.description;
  if (reportStructure) reportStructure.textContent = data.structure;
  if (reportTactics) reportTactics.textContent = data.tacticalDepth;
  if (reportCard) reportCard.textContent = data.bestCard;
  if (reportWeakness) reportWeakness.textContent = data.weakness;
}
