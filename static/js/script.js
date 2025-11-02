// Hamburger Menu Toggle
document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    if (hamburger && navLinks) {
        hamburger.addEventListener('click', function() {
            hamburger.classList.toggle('active');
            navLinks.classList.toggle('active');
        });

        // Close menu when clicking on a link
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', function() {
                hamburger.classList.remove('active');
                navLinks.classList.remove('active');
            });
        });
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
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
    window.addEventListener('load', function() {
        // Removed loading animation to prevent page transition effects
    });

    // Testimonial Slider
    let currentSlide = 0;
    let slides = document.querySelectorAll('.testimonial-slide');
    let dots = document.querySelectorAll('.dot');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');

    function updateSliderElements() {
        slides = document.querySelectorAll('.testimonial-slide');
        dots = document.querySelectorAll('.dot');
    }

    function showSlide(index) {
        updateSliderElements();

        if (slides.length === 0) return;

        if (index >= slides.length) currentSlide = 0;
        if (index < 0) currentSlide = slides.length - 1;

        const container = document.querySelector('.testimonial-container');
        if (container) {
            container.style.transform = `translateX(-${currentSlide * 100}%)`;
        }

        // Update dots
        dots.forEach((dot, i) => {
            dot.classList.toggle('active', i === currentSlide);
        });
    }

    function nextSlide() {
        currentSlide++;
        showSlide(currentSlide);
    }

    function prevSlide() {
        currentSlide--;
        showSlide(currentSlide);
    }

    // Initialize slider
    function initSlider() {
        updateSliderElements();

        // Reset to first slide when new testimonials are added
        currentSlide = 0;
        showSlide(currentSlide);

        // Event listeners for slider
        if (prevBtn && nextBtn) {
            // Remove existing event listeners to avoid duplicates
            nextBtn.replaceWith(nextBtn.cloneNode(true));
            prevBtn.replaceWith(prevBtn.cloneNode(true));

            const newNextBtn = document.getElementById('nextBtn');
            const newPrevBtn = document.getElementById('prevBtn');

            newNextBtn.addEventListener('click', nextSlide);
            newPrevBtn.addEventListener('click', prevSlide);
        }

        if (dots.length > 0) {
            dots.forEach((dot, index) => {
                // Remove existing event listeners
                dot.replaceWith(dot.cloneNode(true));
            });

            // Re-select dots after cloning
            updateSliderElements();

            dots.forEach((dot, index) => {
                dot.addEventListener('click', () => {
                    currentSlide = index;
                    showSlide(currentSlide);
                });
            });
        }

        // Auto slide only if more than 1 slide
        if (slides.length > 1) {
            let autoSlideInterval = setInterval(nextSlide, 5000);

            // Pause auto slide on hover
            const slider = document.querySelector('.testimonial-slider');
            if (slider) {
                slider.addEventListener('mouseenter', () => {
                    clearInterval(autoSlideInterval);
                });

                slider.addEventListener('mouseleave', () => {
                    autoSlideInterval = setInterval(nextSlide, 5000);
                });
            }
        }
    }

    // Initialize slider on page load
    initSlider();
});