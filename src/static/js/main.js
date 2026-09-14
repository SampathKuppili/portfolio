/* =============================================
   Portfolio — Main JavaScript
   ============================================= */

document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initMobileMenu();
    initScrollAnimations();
    initToastAutoClose();
    initSkillAnimations();
    initNavActiveState();
    initHeroTypewriter();
});

/* ---------- Theme Toggle ---------- */
function initTheme() {
    const toggle = document.getElementById('theme-toggle');
    const html = document.documentElement;

    // Load preference
    const stored = localStorage.getItem('theme');
    if (stored) {
        html.setAttribute('data-theme', stored);
    } else if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
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

    // Listen for system changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        if (!localStorage.getItem('theme')) {
            html.setAttribute('data-theme', e.matches ? 'dark' : 'light');
            updateToggleIcon();
        }
    });
}

function updateToggleIcon() {
    const toggle = document.getElementById('theme-toggle');
    if (!toggle) return;
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    toggle.innerHTML = isDark
        ? '<i class="fa-solid fa-sun"></i>'
        : '<i class="fa-solid fa-moon"></i>';
}

/* ---------- Mobile Menu ---------- */
function initMobileMenu() {
    const hamburger = document.getElementById('hamburger');
    const mobileMenu = document.getElementById('mobile-menu');

    if (!hamburger || !mobileMenu) return;

    hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('active');
        mobileMenu.classList.toggle('open');
        document.body.style.overflow = mobileMenu.classList.contains('open') ? 'hidden' : '';
    });

    // Close on link click
    mobileMenu.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            hamburger.classList.remove('active');
            mobileMenu.classList.remove('open');
            document.body.style.overflow = '';
        });
    });
}

/* ---------- Scroll Animations ---------- */
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

/* ---------- Hero Typewriter ----------
   Types the role/designation line out once, terminal-style, as the final
   beat of the hero's page-load sequence. Runs once — this is a one-time
   entrance moment, not a repeating or looping effect. */
function initHeroTypewriter() {
    const el = document.querySelector('.hero-role-text');
    if (!el) return;

    const full = el.getAttribute('data-role-text') || '';
    if (!full) return;

    // Respect reduced-motion preference: show the full text immediately.
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

    // Start once the role line itself has finished rising into place.
    setTimeout(typeNext, 750);
}

/* ---------- Skill Progress Bars ---------- */
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

/* ---------- Toast Auto-Close ---------- */
function initToastAutoClose() {
    document.querySelectorAll('.toast').forEach(toast => {
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(100%)';
            setTimeout(() => toast.remove(), 300);
        }, 4000);
    });
}

/* ---------- Active Nav State ---------- */
function initNavActiveState() {
    const path = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        const href = link.getAttribute('href');
        if (href === path || (href !== '/' && path.startsWith(href))) {
            link.classList.add('active');
        }
    });
}