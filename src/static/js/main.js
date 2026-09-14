/* =============================================
   Portfolio — Main JavaScript v2.0
   Lenis Smooth Scroll · GSAP ScrollTrigger
   Magnetic Buttons · 3D Tilt · Custom Cursor
   Smart Navbar · Liquid Effects
   ============================================= */

document.addEventListener('DOMContentLoaded', () => {
    initPageTransition();
    initTheme();
    initMobileMenu();
    initToastAutoClose();
    initNavActiveState();
    initHeroTypewriter();

    // Lenis smooth scroll + GSAP
    if (typeof gsap !== 'undefined') {
        gsap.registerPlugin(ScrollTrigger);
        initLenisSmoothScroll();
        initGSAPScrollAnimations();
        initNavbarScrollEffects();
        initParallaxElements();
        initSkillAnimationsGSAP();
        initSkillRings();
    } else {
        // Fallback to IntersectionObserver
        initScrollAnimations();
        initSkillAnimations();
        initSkillRingsFallback();
    }

    // Interactive tabs & filters (work with or without GSAP)
    initSkillTabs();
    initProjectFilters();

    // Desktop-only effects
    if (window.matchMedia('(pointer: fine)').matches && window.innerWidth > 1024) {
        initCustomCursor();
        initMagneticButtons();
        initCardTilt();
        initCardGlow();
    }
});

/* ============================================================
   LENIS SMOOTH SCROLL — buttery momentum-based scrolling
   ============================================================ */
function initLenisSmoothScroll() {
    if (typeof Lenis === 'undefined') return;

    // Respect reduced-motion preference
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    const lenis = new Lenis({
        duration: 1.2,
        easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
        orientation: 'vertical',
        gestureOrientation: 'vertical',
        smoothWheel: true,
        wheelMultiplier: 1,
        touchMultiplier: 2,
    });

    // Wire Lenis into GSAP ScrollTrigger
    lenis.on('scroll', ScrollTrigger.update);

    gsap.ticker.add((time) => {
        lenis.raf(time * 1000);
    });

    gsap.ticker.lagSmoothing(0);

    // Store globally so mobile menu can stop/start it
    window._lenis = lenis;
}


/* ============================================================
   PAGE TRANSITION
   ============================================================ */
function initPageTransition() {
    const overlay = document.querySelector('.page-transition-overlay');
    if (!overlay) return;

    requestAnimationFrame(() => {
        requestAnimationFrame(() => {
            overlay.classList.add('loaded');
            setTimeout(() => overlay.remove(), 800);
        });
    });
}

/* ============================================================
   THEME TOGGLE
   ============================================================ */
function initTheme() {
    const toggle = document.getElementById('theme-toggle');
    const html = document.documentElement;

    const stored = localStorage.getItem('theme');
    if (stored) {
        html.setAttribute('data-theme', stored);
    } else {
        html.setAttribute('data-theme', 'dark');
    }

    updateToggleIcon();

    if (toggle) {
        toggle.addEventListener('click', () => {
            const current = html.getAttribute('data-theme');
            const next = current === 'dark' ? 'light' : 'dark';
            html.setAttribute('data-theme', next);
            localStorage.setItem('theme', next);
            updateToggleIcon();
        });
    }

    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        if (!localStorage.getItem('theme')) {
            html.setAttribute('data-theme', e.matches ? 'dark' : 'light');
            updateToggleIcon();
        }
    });
}

function updateToggleIcon() {
    const toggles = document.querySelectorAll('#theme-toggle, #theme-toggle-mobile');
    if (!toggles.length) return;
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    toggles.forEach(toggle => {
        toggle.innerHTML = isDark
            ? '<i class="fa-solid fa-sun"></i>'
            : '<i class="fa-solid fa-moon"></i>';
    });
}

/* ============================================================
   MOBILE MENU
   ============================================================ */
function initMobileMenu() {
    const hamburger = document.getElementById('hamburger');
    const mobileMenu = document.getElementById('mobile-menu');

    if (!hamburger || !mobileMenu) return;

    hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('active');
        mobileMenu.classList.toggle('open');
        const isOpen = mobileMenu.classList.contains('open');
        document.body.style.overflow = isOpen ? 'hidden' : '';
        // Pause/resume Lenis smooth scroll
        if (window._lenis) {
            isOpen ? window._lenis.stop() : window._lenis.start();
        }
    });

    mobileMenu.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            hamburger.classList.remove('active');
            mobileMenu.classList.remove('open');
            document.body.style.overflow = '';
            if (window._lenis) window._lenis.start();
        });
    });
}

/* ============================================================
   GSAP SCROLL ANIMATIONS
   ============================================================ */
function initGSAPScrollAnimations() {
    // Animate all .fade-in elements
    gsap.utils.toArray('.fade-in').forEach(el => {
        gsap.fromTo(el,
            { opacity: 0, y: 30 },
            {
                opacity: 1,
                y: 0,
                duration: 0.8,
                ease: 'power3.out',
                scrollTrigger: {
                    trigger: el,
                    start: 'top 88%',
                    once: true,
                },
            }
        );
    });

    // Animate section headers with stagger
    gsap.utils.toArray('.section-header').forEach(header => {
        const children = header.children;
        gsap.fromTo(children,
            { opacity: 0, y: 20 },
            {
                opacity: 1,
                y: 0,
                duration: 0.6,
                stagger: 0.12,
                ease: 'power3.out',
                scrollTrigger: {
                    trigger: header,
                    start: 'top 88%',
                    once: true,
                },
            }
        );
    });

    // Staggered card grids
    gsap.utils.toArray('.grid').forEach(grid => {
        const items = grid.children;
        if (items.length === 0) return;

        gsap.fromTo(items,
            { opacity: 0, y: 35, scale: 0.96 },
            {
                opacity: 1,
                y: 0,
                scale: 1,
                duration: 0.7,
                stagger: 0.1,
                ease: 'power3.out',
                scrollTrigger: {
                    trigger: grid,
                    start: 'top 85%',
                    once: true,
                },
            }
        );
    });

    // Timeline items stagger
    gsap.utils.toArray('.timeline-item').forEach((item, i) => {
        gsap.fromTo(item,
            { opacity: 0, x: -30 },
            {
                opacity: 1,
                x: 0,
                duration: 0.7,
                ease: 'power3.out',
                scrollTrigger: {
                    trigger: item,
                    start: 'top 88%',
                    once: true,
                },
                delay: i * 0.1,
            }
        );
    });

    // Reveal classes
    gsap.utils.toArray('.reveal-up, .reveal-left, .reveal-right, .reveal-scale').forEach(el => {
        gsap.to(el, {
            opacity: 1,
            x: 0,
            y: 0,
            scale: 1,
            duration: 0.8,
            ease: 'power3.out',
            scrollTrigger: {
                trigger: el,
                start: 'top 88%',
                once: true,
            },
        });
    });
}

/* ============================================================
   NAVBAR SCROLL EFFECTS — hide on scroll-down, show on scroll-up
   ============================================================ */
function initNavbarScrollEffects() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;

    let lastScroll = 0;
    const threshold = 80;

    ScrollTrigger.create({
        start: 'top top',
        end: 'max',
        onUpdate: (self) => {
            const currentScroll = self.scroll();

            if (currentScroll > threshold) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }

            if (currentScroll > lastScroll && currentScroll > 300) {
                navbar.classList.add('nav-hidden');
            } else {
                navbar.classList.remove('nav-hidden');
            }

            lastScroll = currentScroll;
        },
    });
}

/* ============================================================
   PARALLAX FLOATING ELEMENTS
   ============================================================ */
function initParallaxElements() {
    gsap.utils.toArray('.glyph').forEach((glyph, i) => {
        const speed = 0.3 + (i * 0.1);
        gsap.to(glyph, {
            yPercent: -30 * speed,
            ease: 'none',
            scrollTrigger: {
                trigger: '.hero-section',
                start: 'top top',
                end: 'bottom top',
                scrub: 1,
            },
        });
    });

    // Parallax on liquid blobs
    gsap.utils.toArray('.liquid-blob').forEach((blob, i) => {
        const speed = 0.2 + (i * 0.15);
        gsap.to(blob, {
            yPercent: -20 * speed,
            ease: 'none',
            scrollTrigger: {
                trigger: blob.closest('section') || blob.parentElement,
                start: 'top bottom',
                end: 'bottom top',
                scrub: 1.5,
            },
        });
    });
}

/* ============================================================
   SKILL ANIMATIONS — GSAP version with counter
   ============================================================ */
function initSkillAnimationsGSAP() {
    gsap.utils.toArray('.skill-progress-bar').forEach(bar => {
        const target = parseInt(bar.getAttribute('data-progress'), 10) || 0;

        gsap.to(bar, {
            width: target + '%',
            duration: 1.4,
            ease: 'power3.out',
            scrollTrigger: {
                trigger: bar,
                start: 'top 90%',
                once: true,
            },
        });
    });
}

/* ============================================================
   HERO TYPEWRITER
   ============================================================ */
function initHeroTypewriter() {
    const el = document.querySelector('.hero-role-text');
    if (!el) return;

    const full = el.getAttribute('data-role-text') || '';
    if (!full) return;

    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        el.textContent = full;
        return;
    }

    let i = 0;
    const typeNext = () => {
        el.textContent = full.slice(0, i);
        i++;
        if (i <= full.length) {
            setTimeout(typeNext, 32);
        }
    };

    setTimeout(typeNext, 750);
}

/* ============================================================
   CUSTOM CURSOR
   ============================================================ */
function initCustomCursor() {
    const dot = document.querySelector('.cursor-dot');
    const ring = document.querySelector('.cursor-ring');
    if (!dot || !ring) return;

    let mouseX = 0, mouseY = 0;
    let dotX = 0, dotY = 0;
    let ringX = 0, ringY = 0;

    document.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
    });

    // Smooth follow with different lag for dot and ring
    function animateCursor() {
        // Dot follows closely
        dotX += (mouseX - dotX) * 0.2;
        dotY += (mouseY - dotY) * 0.2;
        dot.style.left = dotX + 'px';
        dot.style.top = dotY + 'px';

        // Ring follows with more lag
        ringX += (mouseX - ringX) * 0.08;
        ringY += (mouseY - ringY) * 0.08;
        ring.style.left = ringX + 'px';
        ring.style.top = ringY + 'px';

        requestAnimationFrame(animateCursor);
    }

    animateCursor();

    // Hover effects on interactive elements
    const hoverTargets = document.querySelectorAll('a, button, .btn, .card, .tech-badge, .social-icon, .overlay-btn, input, textarea');
    hoverTargets.forEach(target => {
        target.addEventListener('mouseenter', () => {
            dot.classList.add('cursor-hover');
            ring.classList.add('cursor-hover');
        });
        target.addEventListener('mouseleave', () => {
            dot.classList.remove('cursor-hover');
            ring.classList.remove('cursor-hover');
        });
    });
}

/* ============================================================
   MAGNETIC BUTTONS
   ============================================================ */
function initMagneticButtons() {
    const buttons = document.querySelectorAll('.btn, .social-icon, .theme-toggle, .overlay-btn');

    buttons.forEach(btn => {
        btn.addEventListener('mousemove', (e) => {
            const rect = btn.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;

            btn.style.transform = `translate(${x * 0.2}px, ${y * 0.2}px)`;
        });

        btn.addEventListener('mouseleave', () => {
            btn.style.transform = '';
        });
    });
}

/* ============================================================
   3D CARD TILT
   ============================================================ */
function initCardTilt() {
    const cards = document.querySelectorAll('.card[data-tilt]');

    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = (e.clientX - rect.left) / rect.width;
            const y = (e.clientY - rect.top) / rect.height;

            const rotateX = (y - 0.5) * -8; // max 4deg
            const rotateY = (x - 0.5) * 8;

            card.style.transform = `perspective(800px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(800px) rotateX(0) rotateY(0) scale3d(1, 1, 1)';
            // Smooth snap-back
            card.style.transition = 'transform 0.5s cubic-bezier(0.22, 1, 0.36, 1)';
            setTimeout(() => {
                card.style.transition = 'transform 0.15s ease-out';
            }, 500);
        });
    });
}

/* ============================================================
   CARD GLOW EFFECT — track mouse position for radial gradient
   ============================================================ */
function initCardGlow() {
    const cards = document.querySelectorAll('.card');

    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = ((e.clientX - rect.left) / rect.width) * 100;
            const y = ((e.clientY - rect.top) / rect.height) * 100;

            card.style.setProperty('--mouse-x', x + '%');
            card.style.setProperty('--mouse-y', y + '%');
        });
    });
}

/* ============================================================
   FALLBACK: IntersectionObserver scroll animations
   ============================================================ */
function initScrollAnimations() {
    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        },
        { threshold: 0.1, rootMargin: '0px 0px -30px 0px' }
    );

    document.querySelectorAll('.fade-in, .stagger-children').forEach(el => {
        observer.observe(el);
    });
}

/* ============================================================
   FALLBACK: Skill animations (IntersectionObserver)
   ============================================================ */
function initSkillAnimations() {
    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const bar = entry.target;
                    const target = bar.getAttribute('data-progress');
                    bar.style.width = target + '%';
                    bar.classList.add('animate');
                }
            });
        },
        { threshold: 0.3 }
    );

    document.querySelectorAll('.skill-progress-bar').forEach(bar => {
        observer.observe(bar);
    });
}

/* ============================================================
   TOAST AUTO-CLOSE
   ============================================================ */
function initToastAutoClose() {
    document.querySelectorAll('.toast').forEach(toast => {
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(100%) scale(0.9)';
            setTimeout(() => toast.remove(), 400);
        }, 4000);
    });
}

/* ============================================================
   ACTIVE NAV STATE
   ============================================================ */
function initNavActiveState() {
    const path = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        const href = link.getAttribute('href');
        if (href === path || (href !== '/' && path.startsWith(href))) {
            link.classList.add('active');
        }
    });
}

/* ============================================================
   SKILL TABS — category filter with animation
   ============================================================ */
function initSkillTabs() {
    const tabsContainer = document.getElementById('skills-tabs');
    const grid = document.getElementById('skills-grid');
    if (!tabsContainer || !grid) return;

    const tabs = tabsContainer.querySelectorAll('.skills-tab');
    const cards = grid.querySelectorAll('.skill-icon-card');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Update active tab
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            const category = tab.getAttribute('data-category');

            if (typeof gsap !== 'undefined') {
                // GSAP animated filter
                const toHide = [];
                const toShow = [];

                cards.forEach(card => {
                    const match = category === 'all' || card.getAttribute('data-category') === category;
                    if (match) {
                        toShow.push(card);
                    } else {
                        toHide.push(card);
                    }
                });

                // Animate out
                if (toHide.length) {
                    gsap.to(toHide, {
                        opacity: 0,
                        scale: 0.9,
                        y: 10,
                        duration: 0.25,
                        stagger: 0.02,
                        ease: 'power2.in',
                        onComplete: () => {
                            toHide.forEach(c => c.style.display = 'none');
                        }
                    });
                }

                // Animate in
                setTimeout(() => {
                    toShow.forEach(c => {
                        c.style.display = '';
                    });
                    gsap.fromTo(toShow,
                        { opacity: 0, scale: 0.9, y: 15 },
                        {
                            opacity: 1,
                            scale: 1,
                            y: 0,
                            duration: 0.4,
                            stagger: 0.04,
                            ease: 'power3.out',
                        }
                    );
                    // Re-animate rings for visible cards
                    animateVisibleRings(toShow);
                }, toHide.length ? 280 : 0);

            } else {
                // Fallback — simple show/hide
                cards.forEach(card => {
                    const match = category === 'all' || card.getAttribute('data-category') === category;
                    card.style.display = match ? '' : 'none';
                    card.style.opacity = match ? '1' : '0';
                });
            }
        });
    });
}

/* ============================================================
   SKILL RINGS — GSAP scroll-triggered circle animation
   ============================================================ */
function initSkillRings() {
    const rings = document.querySelectorAll('.skill-ring-progress');
    if (!rings.length) return;

    const CIRCUMFERENCE = 2 * Math.PI * 30; // r=30 → ≈188.5

    rings.forEach(ring => {
        const progress = parseInt(ring.getAttribute('data-progress'), 10) || 0;
        const offset = CIRCUMFERENCE - (progress / 100) * CIRCUMFERENCE;

        // Start fully hidden
        ring.style.strokeDasharray = CIRCUMFERENCE;
        ring.style.strokeDashoffset = CIRCUMFERENCE;

        gsap.to(ring, {
            strokeDashoffset: offset,
            duration: 1.4,
            ease: 'power3.out',
            scrollTrigger: {
                trigger: ring,
                start: 'top 90%',
                once: true,
            },
        });
    });
}

/* Helper: re-animate rings after tab switch */
function animateVisibleRings(cards) {
    const CIRCUMFERENCE = 2 * Math.PI * 30;
    cards.forEach(card => {
        const ring = card.querySelector('.skill-ring-progress');
        if (!ring) return;
        const progress = parseInt(ring.getAttribute('data-progress'), 10) || 0;
        const offset = CIRCUMFERENCE - (progress / 100) * CIRCUMFERENCE;

        // Reset then animate
        ring.style.strokeDashoffset = CIRCUMFERENCE;
        if (typeof gsap !== 'undefined') {
            gsap.to(ring, {
                strokeDashoffset: offset,
                duration: 1.0,
                ease: 'power3.out',
                delay: 0.15,
            });
        } else {
            setTimeout(() => { ring.style.strokeDashoffset = offset; }, 50);
        }
    });
}

/* Fallback: IntersectionObserver ring animation */
function initSkillRingsFallback() {
    const CIRCUMFERENCE = 2 * Math.PI * 30;
    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const ring = entry.target;
                    const progress = parseInt(ring.getAttribute('data-progress'), 10) || 0;
                    const offset = CIRCUMFERENCE - (progress / 100) * CIRCUMFERENCE;
                    ring.style.strokeDashoffset = offset;
                    observer.unobserve(ring);
                }
            });
        },
        { threshold: 0.3 }
    );

    document.querySelectorAll('.skill-ring-progress').forEach(ring => {
        ring.style.strokeDasharray = CIRCUMFERENCE;
        ring.style.strokeDashoffset = CIRCUMFERENCE;
        observer.observe(ring);
    });
}

/* ============================================================
   PROJECT FILTERS — client-side category toggle
   ============================================================ */
function initProjectFilters() {
    const tabsContainer = document.getElementById('project-filter-tabs');
    const grid = document.getElementById('projects-grid');
    if (!tabsContainer || !grid) return;

    const tabs = tabsContainer.querySelectorAll('.project-filter-tab');
    const cards = grid.querySelectorAll('.project-card-wrapper');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Update active tab
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            const filter = tab.getAttribute('data-filter');

            if (typeof gsap !== 'undefined') {
                const toHide = [];
                const toShow = [];

                cards.forEach(card => {
                    const match = filter === 'all' || card.getAttribute('data-type') === filter;
                    if (match) {
                        toShow.push(card);
                    } else {
                        toHide.push(card);
                    }
                });

                // Animate out hidden cards
                if (toHide.length) {
                    gsap.to(toHide, {
                        opacity: 0,
                        scale: 0.92,
                        y: 10,
                        duration: 0.25,
                        stagger: 0.03,
                        ease: 'power2.in',
                        onComplete: () => {
                            toHide.forEach(c => {
                                c.style.display = 'none';
                            });
                        }
                    });
                }

                // Animate in matching cards
                setTimeout(() => {
                    toShow.forEach(c => {
                        c.style.display = '';
                    });
                    gsap.fromTo(toShow,
                        { opacity: 0, scale: 0.92, y: 15 },
                        {
                            opacity: 1,
                            scale: 1,
                            y: 0,
                            duration: 0.4,
                            stagger: 0.05,
                            ease: 'power3.out',
                        }
                    );
                }, toHide.length ? 280 : 0);

            } else {
                // Simple fallback
                cards.forEach(card => {
                    const match = filter === 'all' || card.getAttribute('data-type') === filter;
                    card.style.display = match ? '' : 'none';
                    card.style.opacity = match ? '1' : '0';
                });
            }
        });
    });
}