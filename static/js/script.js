// Hamburger Menu Toggle
document.addEventListener("DOMContentLoaded", function () {
  const hamburger = document.querySelector(".hamburger");
  const navLinks = document.querySelector(".nav-links");

  if (hamburger && navLinks) {
    hamburger.addEventListener("click", function () {
      hamburger.classList.toggle("active");
      navLinks.classList.toggle("active");
    });

    // Close menu when clicking on a link
    navLinks.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", function () {
        hamburger.classList.remove("active");
        navLinks.classList.remove("active");
      });
    });
  }

  // Smooth scrolling for anchor links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute("href"));
      if (target) {
        target.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }
    });
  });

  // Add fade-in animation on scroll - REMOVED to prevent white flash effects
  /*
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, observerOptions);

    // Observe all sections
    document.querySelectorAll('section').forEach(section => {
        observer.observe(section);
    });
    */

  // Add loading animation
  window.addEventListener("load", function () {
    // Removed loading animation to prevent page transition effects
  });

  // Testimonial Slider (robust re-querying, no node cloning)
  (function () {
    let current = 0;
    let autoSlideInterval = null;

    function getSlides() {
      return Array.from(document.querySelectorAll(".testimonial-slide"));
    }

    function getDots() {
      return Array.from(document.querySelectorAll(".dot"));
    }

    function updateView() {
      const slides = getSlides();
      const dots = getDots();
      const container = document.querySelector(".testimonial-container");

      if (!container || slides.length === 0) return;

      // normalize current index
      if (current >= slides.length) current = 0;
      if (current < 0) current = slides.length - 1;

      // Robust mode: show exactly one slide, hide the rest
      slides.forEach((s, i) => {
        if (i === current) {
          s.classList.add("active");
        } else {
          s.classList.remove("active");
        }
      });

      // When showing exactly one slide via .active, don't translate container
      // as it can move the only visible slide out of view. Keep it at 0.
      container.style.transform = "translateX(0)";

      // update dots
      dots.forEach((dot, i) => dot.classList.toggle("active", i === current));
    }

    function goTo(index) {
      current = index;
      updateView();
    }

    function next() {
      goTo(current + 1);
    }
    function prev() {
      goTo(current - 1);
    }

    function setupControls() {
      const prevBtn = document.getElementById("prevBtn");
      const nextBtn = document.getElementById("nextBtn");

      if (prevBtn)
        prevBtn.addEventListener("click", function (e) {
          e.preventDefault();
          prev();
        });
      if (nextBtn)
        nextBtn.addEventListener("click", function (e) {
          e.preventDefault();
          next();
        });

      // dots
      const dots = getDots();
      dots.forEach((dot, idx) => {
        dot.addEventListener("click", function () {
          goTo(idx);
        });
      });
    }

    function setupAutoSlide() {
      const slider = document.querySelector(".testimonial-slider");
      const slides = getSlides();
      if (autoSlideInterval) {
        clearInterval(autoSlideInterval);
        autoSlideInterval = null;
      }
      if (slides.length > 1) {
        autoSlideInterval = setInterval(next, 4000); // Auto slide every 4 seconds
        if (slider) {
          slider.addEventListener("mouseenter", () => {
            if (autoSlideInterval) clearInterval(autoSlideInterval);
          });
          slider.addEventListener("mouseleave", () => {
            if (!autoSlideInterval) autoSlideInterval = setInterval(next, 4000);
          });
        }
      }
    }

    function init() {
      // always reinitialize view to handle DOM changes
      current = 0;
      updateView();
      setupAutoSlide();
      // Debug: log slide contents so we can see if elements are empty after a form POST
      try {
        const slides = getSlides();
        console.log("[slider-debug] init - slide count =", slides.length);
        slides.forEach((s, idx) => {
          const textEl = s.querySelector(".testimonial-text");
          const nameEl = s.querySelector(".author-info h4");
          const msg = textEl
            ? textEl.innerText.trim()
            : "[no testimonial-text element]";
          const name = nameEl ? nameEl.innerText.trim() : "[no author name]";
          console.log(
            `[slider-debug] slide ${idx}: name="${name}" msg="${msg}"`
          );
        });
      } catch (err) {
        console.warn("[slider-debug] failed to enumerate slides:", err);
      }
    }

    // Initialize slider on page load
    init();
  })();
});
