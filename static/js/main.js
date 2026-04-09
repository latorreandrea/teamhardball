/* ========================================
   N.S.O.G. MAIN JAVASCRIPT
   - Navbar hide/show on scroll
   - Smooth scrolling for anchor links
   - Scroll-to-top button
======================================== */

document.addEventListener('DOMContentLoaded', () => {
    // ========================================
    // 1) NAVBAR: Hide on scroll down, show on scroll up (desktop only)
    // ========================================
    const navbarEl = document.getElementById('site-navbar');
    let previousScrollY = window.scrollY;
    let navbarTicking = false;
    const desktopMediaQuery = window.matchMedia('(min-width: 992px)');

    const applyNavbarState = () => {
        if (!navbarEl) {
            return;
        }

        // Add shadow effect when scrolled
        navbarEl.classList.toggle('is-scrolled', window.scrollY > 16);

        // Keep navbar visible at the top
        if (window.scrollY <= 16) {
            navbarEl.classList.remove('nav-hidden');
            previousScrollY = window.scrollY;
            return;
        }

        // Always show navbar on mobile/tablet
        if (!desktopMediaQuery.matches) {
            navbarEl.classList.remove('nav-hidden');
            previousScrollY = window.scrollY;
            return;
        }

        // Hide when scrolling down, show when scrolling up (desktop only)
        if (window.scrollY > previousScrollY + 12) {
            navbarEl.classList.add('nav-hidden');
        } else if (window.scrollY < previousScrollY - 10) {
            navbarEl.classList.remove('nav-hidden');
        }

        previousScrollY = window.scrollY;
    };

    // Initialize navbar state
    applyNavbarState();

    // Update on scroll with requestAnimationFrame for performance
    window.addEventListener('scroll', () => {
        if (!navbarTicking) {
            window.requestAnimationFrame(() => {
                applyNavbarState();
                navbarTicking = false;
            });
            navbarTicking = true;
        }
    }, { passive: true });

    // ========================================
    // 2) SMOOTH SCROLL for anchor links
    // ========================================
    document.querySelectorAll('a[href*="#"]').forEach((anchor) => {
        anchor.addEventListener('click', (event) => {
            const rawHref = anchor.getAttribute('href');
            if (!rawHref || rawHref === '#') {
                return;
            }

            const linkUrl = new URL(rawHref, window.location.origin);
            if (!linkUrl.hash) {
                return;
            }

            // Only handle same-page anchors
            const samePage = linkUrl.pathname === window.location.pathname;
            if (!samePage) {
                return;
            }

            const targetId = linkUrl.hash;
            const target = document.querySelector(targetId);
            if (!target) {
                return;
            }

            event.preventDefault();
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start',
            });
        });
    });

    // ========================================
    // 3) SCROLL TO TOP BUTTON
    // ========================================
    const scrollBtn = document.getElementById('scrollToTopBtn');

    if (scrollBtn) {
        // Show/hide button based on scroll position
        window.addEventListener('scroll', () => {
            scrollBtn.classList.toggle('show', window.scrollY > 220);
        }, { passive: true });

        // Scroll to top when clicked
        scrollBtn.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // ========================================
    // 4) CLOSE MOBILE MENU after clicking nav link
    // ========================================
    const navLinks = document.querySelectorAll('.navbar-collapse .nav-link');

    navLinks.forEach((link) => {
        link.addEventListener('click', () => {
            const mobileMenu = document.querySelector('.navbar-collapse.show');

            if (mobileMenu && window.bootstrap) {
                window.bootstrap.Collapse.getOrCreateInstance(mobileMenu).hide();
            }
        });
    });
});