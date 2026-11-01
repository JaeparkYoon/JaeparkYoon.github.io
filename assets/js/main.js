/**
 * Jaepark Yoon Portfolio - Navigation, Carousel & Lightbox
 */

document.addEventListener("DOMContentLoaded", () => {
  initHeader();
  initSnapfolioCarousel();
  initScreenshotModal();
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
  });

  // Tab pages: show only the section matching the URL hash
  const ids = Array.from(sections, (section) => section.id);

  const showPage = () => {
    const hash = location.hash.slice(1);
    const current = ids.includes(hash) ? hash : ids[0];

    sections.forEach((section) => {
      section.hidden = section.id !== current;
    });

    navLinks.forEach((link) => {
      link.classList.toggle("active", link.getAttribute("href") === `#${current}`);
    });

    window.scrollTo({ top: 0, behavior: "instant" });
  };

  window.addEventListener("hashchange", showPage);
  showPage();
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
