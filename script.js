// Mobile Navigation Toggle
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');

hamburger.addEventListener('click', () => {
    navMenu.classList.toggle('active');

    // Animate hamburger icon
    hamburger.classList.toggle('active');
});

// Close mobile menu when clicking on a link
document.querySelectorAll('.nav-menu a').forEach(link => {
    link.addEventListener('click', () => {
        navMenu.classList.remove('active');
        hamburger.classList.remove('active');
    });
});

// Navbar scroll effect
let lastScroll = 0;
const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;

    if (currentScroll > 100) {
        navbar.style.boxShadow = '0 2px 20px rgba(0,0,0,0.1)';
        navbar.style.padding = '0.5rem 0';
    } else {
        navbar.style.boxShadow = '0 5px 15px rgba(0,0,0,0.1)';
        navbar.style.padding = '1rem 0';
    }

    lastScroll = currentScroll;
});

// Smooth scroll with offset for fixed navbar
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const offsetTop = target.offsetTop - 80;
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        }
    });
});

// Intersection Observer for fade-in animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe service cards
document.querySelectorAll('.service-card').forEach((card, index) => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(30px)';
    card.style.transition = `all 0.6s ease ${index * 0.1}s`;
    observer.observe(card);
});

// Observe info cards
document.querySelectorAll('.info-card').forEach((card, index) => {
    card.style.opacity = '0';
    card.style.transform = 'translateX(-30px)';
    card.style.transition = `all 0.6s ease ${index * 0.1}s`;
    observer.observe(card);
});

// WhatsApp floating button (optional - uncomment if needed)
/*
const whatsappFloat = document.createElement('a');
whatsappFloat.href = 'https://wa.me/905438247016';
whatsappFloat.target = '_blank';
whatsappFloat.className = 'whatsapp-float';
whatsappFloat.innerHTML = '💬';
whatsappFloat.setAttribute('aria-label', 'WhatsApp ile iletişime geç');
document.body.appendChild(whatsappFloat);

// Add CSS for floating button
const style = document.createElement('style');
style.textContent = `
    .whatsapp-float {
        position: fixed;
        width: 60px;
        height: 60px;
        bottom: 40px;
        right: 40px;
        background-color: #25D366;
        color: white;
        border-radius: 50%;
        text-align: center;
        font-size: 30px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
        z-index: 999;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
        text-decoration: none;
    }

    .whatsapp-float:hover {
        background-color: #128C7E;
        transform: scale(1.1);
        box-shadow: 2px 2px 20px rgba(0,0,0,0.4);
    }

    @media (max-width: 768px) {
        .whatsapp-float {
            width: 50px;
            height: 50px;
            bottom: 20px;
            right: 20px;
            font-size: 25px;
        }
    }
`;
document.head.appendChild(style);
*/

// Form validation (if you add a contact form later)
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Phone number formatting for Turkey
function formatPhoneNumber(phone) {
    // Remove all non-numeric characters
    phone = phone.replace(/\D/g, '');

    // Format as Turkish phone number
    if (phone.length === 10) {
        return phone.replace(/(\d{3})(\d{3})(\d{2})(\d{2})/, '0$1 $2 $3 $4');
    } else if (phone.length === 11) {
        return phone.replace(/(\d{4})(\d{3})(\d{2})(\d{2})/, '$1 $2 $3 $4');
    }
    return phone;
}

// Log page view (for analytics integration later)
console.log('NÖRODİL website loaded successfully');

// Accessibility: Add keyboard navigation support
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && navMenu.classList.contains('active')) {
        navMenu.classList.remove('active');
        hamburger.classList.remove('active');
    }
});

// Lazy loading for iframe (Google Maps)
const mapIframe = document.querySelector('.contact-map iframe');
if (mapIframe) {
    const mapObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Map is already loaded in HTML, but we can add loading animation
                entry.target.style.opacity = '0';
                setTimeout(() => {
                    entry.target.style.transition = 'opacity 0.5s ease';
                    entry.target.style.opacity = '1';
                }, 100);
                mapObserver.unobserve(entry.target);
            }
        });
    });
    mapObserver.observe(mapIframe);
}

// ==================== COUNTER ANIMATION ====================
function animateCounters() {
    const counters = document.querySelectorAll('.stat-number');
    const speed = 200; // Animation speed

    counters.forEach(counter => {
        const target = parseInt(counter.getAttribute('data-target'));
        if (!target) return;

        const increment = target / speed;
        let hasAnimated = false;

        const updateCount = () => {
            const count = parseInt(counter.innerText);

            if (count < target) {
                counter.innerText = Math.ceil(count + increment);
                setTimeout(updateCount, 10);
            } else {
                counter.innerText = target;
            }
        };

        // Start counting when element is in viewport
        const counterObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !hasAnimated) {
                    hasAnimated = true;
                    updateCount();
                }
            });
        }, { threshold: 0.5 });

        counterObserver.observe(counter);
    });
}

// ==================== SCROLL REVEAL ANIMATION ====================
function revealOnScroll() {
    const reveals = document.querySelectorAll('.reveal');

    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
            }
        });
    }, {
        threshold: 0.15
    });

    reveals.forEach(reveal => revealObserver.observe(reveal));
}

// ==================== SMOOTH BADGE ANIMATION ====================
function animateBadges() {
    const badges = document.querySelectorAll('.badge-item');

    badges.forEach((badge, index) => {
        badge.style.animationDelay = `${index * 0.15}s`;
    });
}

// ==================== INITIALIZE ALL ANIMATIONS ====================
document.addEventListener('DOMContentLoaded', () => {
    // Initialize counter animations
    animateCounters();

    // Initialize scroll reveal
    revealOnScroll();

    // Initialize badge animations
    animateBadges();

    console.log('All animations initialized successfully');
});

// ==================== GOOGLE REVIEWS CAROUSEL ====================
class ReviewsCarousel {
    constructor(container) {
        this.container = container;
        this.track = container.querySelector('.carousel-track');
        this.cards = Array.from(container.querySelectorAll('.review-card'));
        this.prevBtn = container.querySelector('.prev-btn');
        this.nextBtn = container.querySelector('.next-btn');
        this.dots = Array.from(container.querySelectorAll('.dot'));

        this.currentIndex = 0;
        this.autoplayInterval = null;
        this.autoplayDelay = 5000; // 5 seconds

        this.init();
    }

    init() {
        // Set initial card positions
        this.updateCards();

        // Event listeners
        this.prevBtn.addEventListener('click', () => this.prev());
        this.nextBtn.addEventListener('click', () => this.next());

        this.dots.forEach((dot, index) => {
            dot.addEventListener('click', () => this.goToSlide(index));
        });

        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowLeft') this.prev();
            if (e.key === 'ArrowRight') this.next();
        });

        // Touch swipe support
        this.setupTouchEvents();

        // Start autoplay when in viewport
        this.setupIntersectionObserver();

        // Pause on hover
        this.container.addEventListener('mouseenter', () => this.pauseAutoplay());
        this.container.addEventListener('mouseleave', () => this.startAutoplay());
    }

    updateCards() {
        this.cards.forEach((card, index) => {
            // Remove all position classes
            card.classList.remove('active', 'next', 'next-2', 'prev', 'prev-2', 'hidden');

            const position = this.getCardPosition(index);

            if (position === 0) {
                card.classList.add('active');
            } else if (position === 1) {
                card.classList.add('next');
            } else if (position === 2) {
                card.classList.add('next-2');
            } else if (position === -1) {
                card.classList.add('prev');
            } else if (position === -2) {
                card.classList.add('prev-2');
            } else {
                card.classList.add('hidden');
            }
        });

        // Update dots
        this.dots.forEach((dot, index) => {
            dot.classList.toggle('active', index === this.currentIndex);
        });
    }

    getCardPosition(cardIndex) {
        const diff = cardIndex - this.currentIndex;
        const total = this.cards.length;

        // Handle wrap-around
        if (diff > total / 2) return diff - total;
        if (diff < -total / 2) return diff + total;

        return diff;
    }

    next() {
        this.currentIndex = (this.currentIndex + 1) % this.cards.length;
        this.updateCards();
        this.resetAutoplay();
    }

    prev() {
        this.currentIndex = (this.currentIndex - 1 + this.cards.length) % this.cards.length;
        this.updateCards();
        this.resetAutoplay();
    }

    goToSlide(index) {
        this.currentIndex = index;
        this.updateCards();
        this.resetAutoplay();
    }

    startAutoplay() {
        this.autoplayInterval = setInterval(() => this.next(), this.autoplayDelay);
    }

    pauseAutoplay() {
        if (this.autoplayInterval) {
            clearInterval(this.autoplayInterval);
            this.autoplayInterval = null;
        }
    }

    resetAutoplay() {
        this.pauseAutoplay();
        this.startAutoplay();
    }

    setupTouchEvents() {
        let touchStartX = 0;
        let touchEndX = 0;

        this.track.addEventListener('touchstart', (e) => {
            touchStartX = e.changedTouches[0].screenX;
        }, { passive: true });

        this.track.addEventListener('touchend', (e) => {
            touchEndX = e.changedTouches[0].screenX;
            this.handleSwipe(touchStartX, touchEndX);
        }, { passive: true });
    }

    handleSwipe(startX, endX) {
        const threshold = 50;
        const diff = startX - endX;

        if (Math.abs(diff) > threshold) {
            if (diff > 0) {
                this.next();
            } else {
                this.prev();
            }
        }
    }

    setupIntersectionObserver() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.startAutoplay();
                } else {
                    this.pauseAutoplay();
                }
            });
        }, { threshold: 0.5 });

        observer.observe(this.container);
    }
}

// Initialize carousel when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const carouselContainer = document.querySelector('.carousel-container');
    if (carouselContainer) {
        new ReviewsCarousel(carouselContainer);
        console.log('Reviews carousel initialized successfully');
    }
});