document.addEventListener('DOMContentLoaded', () => {
    // 1. Theme Toggle
    const themeToggleBtn = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');

    function updateThemeIcon(isDark) {
        if (themeIcon) {
            themeIcon.textContent = isDark ? 'light_mode' : 'dark_mode';
        }
    }

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            if (document.documentElement.classList.contains('dark')) {
                document.documentElement.classList.remove('dark');
                localStorage.theme = 'light';
                updateThemeIcon(false);
            } else {
                document.documentElement.classList.add('dark');
                localStorage.theme = 'dark';
                updateThemeIcon(true);
            }
        });
    }

    // Set initial icon
    const isDark = document.documentElement.classList.contains('dark');
    updateThemeIcon(isDark);

    // 3. Custom Language Dropdown
    const langBtn = document.getElementById('language-button');
    const langMenu = document.getElementById('language-menu');
    const langChevron = document.getElementById('language-chevron');
    const langInput = document.getElementById('language-input');
    const langForm = document.getElementById('language-form');
    const langOptions = document.querySelectorAll('.lang-option');

    if (langBtn && langMenu) {
        langBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            const isExpanded = !langMenu.classList.contains('invisible');
            
            if (isExpanded) {
                closeLangMenu();
            } else {
                langMenu.classList.remove('opacity-0', 'invisible', 'scale-95');
                langMenu.classList.add('opacity-100', 'visible', 'scale-100');
                langChevron.style.transform = 'rotate(180deg)';
            }
        });

        // Close on outside click
        document.addEventListener('click', (e) => {
            if (!langBtn.contains(e.target) && !langMenu.contains(e.target)) {
                closeLangMenu();
            }
        });

        function closeLangMenu() {
            langMenu.classList.add('opacity-0', 'invisible', 'scale-95');
            langMenu.classList.remove('opacity-100', 'visible', 'scale-100');
            langChevron.style.transform = 'rotate(0deg)';
        }

        langOptions.forEach(option => {
            option.addEventListener('click', () => {
                const langCode = option.getAttribute('data-lang');
                langInput.value = langCode;
                langForm.submit();
            });
        });
    }

    // 2. Scroll Animations (Intersection Observer)
    const animatedElements = document.querySelectorAll('main section > div > div, main h1, main h2, main h3, main p, main img');
    // CSS now initially hides these elements via the .js-enabled class to prevent FOUC

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: "0px 0px -50px 0px"
    });

    animatedElements.forEach(el => observer.observe(el));

    // 4. Count-up Animation for Stats
    const statNumbers = document.querySelectorAll('.stat-number');
    const statsObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const el = entry.target;
                const target = parseFloat(el.getAttribute('data-target'));
                const suffix = el.getAttribute('data-suffix') || '';
                const decimals = parseInt(el.getAttribute('data-decimals')) || 0;
                
                let startTimestamp = null;
                const duration = 2000; // 2 seconds

                const step = (timestamp) => {
                    if (!startTimestamp) startTimestamp = timestamp;
                    const progress = Math.min((timestamp - startTimestamp) / duration, 1);
                    
                    // Use easeOutQuart for smoother deceleration
                    const easeProgress = 1 - Math.pow(1 - progress, 4);
                    const current = easeProgress * target;
                    
                    let formattedNumber = current.toFixed(decimals);
                    
                    // Add comma separators for large numbers (e.g. 42,850)
                    if (decimals === 0 && current >= 1000) {
                        formattedNumber = Math.floor(current).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
                    }
                    
                    el.textContent = formattedNumber + suffix;
                    
                    if (progress < 1) {
                        window.requestAnimationFrame(step);
                    } else {
                        // Ensure it finishes exactly on target
                        let finalNumber = target.toFixed(decimals);
                        if (decimals === 0 && target >= 1000) {
                            finalNumber = Math.floor(target).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
                        }
                        el.textContent = finalNumber + suffix;
                    }
                };
                
                window.requestAnimationFrame(step);
                statsObserver.unobserve(el); // Animate only once
            }
        });
    }, {
        threshold: 0.5
    });

    statNumbers.forEach(el => statsObserver.observe(el));

    // 5. Page Transitions
    try {
        const pageWrapper = document.getElementById('page-wrapper');
        if (pageWrapper) {
            pageWrapper.classList.add('page-fade-in');
        }

        const links = document.querySelectorAll('a:not([target="_blank"]):not([href^="#"]):not([href^="mailto:"]):not([href^="tel:"])');
        links.forEach(link => {
            link.addEventListener('click', (e) => {
                const href = link.getAttribute('href');
                if (!href || href === '#' || href.startsWith('http') && !href.includes(window.location.host)) return;
                
                if (link.closest('#language-form') || link.classList.contains('no-transition')) return;

                e.preventDefault();
                if (pageWrapper) {
                    pageWrapper.classList.remove('page-fade-in');
                    pageWrapper.classList.add('page-fade-out');
                }

                setTimeout(() => {
                    window.location.href = href;
                }, 400);
            });
        });

        // Reset on back button (from cache)
        window.addEventListener('pageshow', (event) => {
            if (event.persisted && pageWrapper) {
                pageWrapper.classList.remove('page-fade-out');
                pageWrapper.classList.add('page-fade-in');
            }
        });
    } catch (err) {
        console.error("Page transition error:", err);
    }
    // 6. Mobile Menu Toggle
    const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
    const mobileMenu = document.getElementById('mobile-menu');
    const body = document.body;

    if (mobileMenuToggle && mobileMenu) {
        mobileMenuToggle.addEventListener('click', () => {
            mobileMenuToggle.classList.toggle('menu-open');
            mobileMenu.classList.toggle('menu-open');
            body.classList.toggle('menu-open');
        });

        // Close menu when clicking on a link
        const mobileLinks = mobileMenu.querySelectorAll('a');
        mobileLinks.forEach(link => {
            link.addEventListener('click', () => {
                mobileMenuToggle.classList.remove('menu-open');
                mobileMenu.classList.remove('menu-open');
                body.classList.remove('menu-open');
            });
        });
    }

    // 7. Mobile Theme Toggle
    const themeToggleMobileBtn = document.getElementById('theme-toggle-mobile');
    const mobileThemeIcon = document.querySelector('.mobile-theme-icon');

    function updateMobileThemeIcon(isDark) {
        if (mobileThemeIcon) {
            mobileThemeIcon.textContent = isDark ? 'light_mode' : 'dark_mode';
        }
    }

    if (themeToggleMobileBtn) {
        themeToggleMobileBtn.addEventListener('click', () => {
            const isDarkMode = document.documentElement.classList.toggle('dark');
            localStorage.theme = isDarkMode ? 'dark' : 'light';
            updateThemeIcon(isDarkMode);
            updateMobileThemeIcon(isDarkMode);
        });
    }

    // 9. Mobile Language Dropdown
    const langBtnMobile = document.getElementById('language-button-mobile');
    const langMenuMobile = document.getElementById('language-menu-mobile');
    const langChevronMobile = document.getElementById('language-chevron-mobile');

    if (langBtnMobile && langMenuMobile) {
        langBtnMobile.addEventListener('click', (e) => {
            e.stopPropagation();
            const isExpanded = !langMenuMobile.classList.contains('invisible');
            
            if (isExpanded) {
                closeLangMenuMobile();
            } else {
                langMenuMobile.classList.remove('opacity-0', 'invisible', 'scale-95');
                langMenuMobile.classList.add('opacity-100', 'visible', 'scale-100');
                langChevronMobile.style.transform = 'rotate(180deg)';
            }
        });

        function closeLangMenuMobile() {
            langMenuMobile.classList.add('opacity-0', 'invisible', 'scale-95');
            langMenuMobile.classList.remove('opacity-100', 'visible', 'scale-100');
            langChevronMobile.style.transform = 'rotate(0deg)';
        }

        // Close on outside click
        document.addEventListener('click', (e) => {
            if (langBtnMobile && !langBtnMobile.contains(e.target) && langMenuMobile && !langMenuMobile.contains(e.target)) {
                closeLangMenuMobile();
            }
        });

        // Language selection logic for mobile
        const langOptionsMobile = document.querySelectorAll('.lang-option-mobile');
        langOptionsMobile.forEach(option => {
            option.addEventListener('click', () => {
                const langCode = option.getAttribute('data-lang');
                if (langInput && langForm) {
                    langInput.value = langCode;
                    langForm.submit();
                }
            });
        });
    }

    // Initialize mobile theme icon
    updateMobileThemeIcon(document.documentElement.classList.contains('dark'));
});

/**
 * Global Toast Notification System
 * @param {string} message - The message to display
 * @param {string} type - 'success', 'error', or 'info'
 */
function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `message-toast mb-4 p-4 rounded-2xl shadow-2xl flex items-center gap-3 animate-message-in pointer-events-auto transition-all duration-500`;
    
    let bgClass = 'bg-surface-container-high text-on-surface';
    let icon = 'info';
    
    if (type === 'success') {
        bgClass = 'bg-green-600 text-white';
        icon = 'check_circle';
    } else if (type === 'error' || type === 'danger') {
        bgClass = 'bg-red-600 text-white';
        icon = 'error';
    }
    
    toast.classList.add(...bgClass.split(' '));

    toast.innerHTML = `
        <span class="material-symbols-outlined">${icon}</span>
        <p class="font-label-lg flex-1">${message}</p>
        <button onclick="this.parentElement.remove()" class="opacity-70 hover:opacity-100 transition-opacity">
            <span class="material-symbols-outlined text-[18px]">close</span>
        </button>
    `;

    container.appendChild(toast);

    // Auto-hide after 4 seconds
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(20px)';
        setTimeout(() => toast.remove(), 500);
    }, 4000);
}
