// PROFESSIONAL ANIMATIONS AND INTERACTIONS
document.addEventListener('DOMContentLoaded', function () {
    
    // PAGE LOADER
    const pageLoader = document.getElementById('page-loader');
    if (pageLoader) {
        window.addEventListener('load', function () {
            pageLoader.style.opacity = '0';
            setTimeout(() => {
                pageLoader.style.display = 'none';
            }, 500);
        });
    }

    // SMOOTH SCROLL FOR ANCHOR LINKS
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#' && href.length > 1) {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });

    // STAGGER ANIMATION FOR CARDS
    const cards = document.querySelectorAll('.card, .choose-card, .job-card');
    cards.forEach((card, index) => {
        card.style.setProperty('--animation-order', index);
        card.style.animationDelay = `${index * 0.1}s`;
    });

    // TABLE ROW INDEX FOR ANIMATIONS
    const tableRows = document.querySelectorAll('.table tbody tr');
    tableRows.forEach((row, index) => {
        row.style.setProperty('--row-index', index);
    });

    // FORM VALIDATION ANIMATIONS
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function (e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn && this.checkValidity()) {
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
                submitBtn.disabled = true;
            }
        });
    });

    // INPUT FOCUS ANIMATIONS
    const inputs = document.querySelectorAll('.form-control, .form-select');
    inputs.forEach(input => {
        input.addEventListener('focus', function () {
            this.closest('.mb-3, .mb-4')?.classList.add('focused');
        });
        input.addEventListener('blur', function () {
            this.closest('.mb-3, .mb-4')?.classList.remove('focused');
        });
    });

    // NOTIFICATION DROPDOWN ANIMATION
    const notificationBell = document.querySelector('.notification-bell');
    if (notificationBell) {
        notificationBell.addEventListener('click', function () {
            const dropdown = this.nextElementSibling;
            if (dropdown) {
                dropdown.style.animation = 'fadeIn 0.3s ease';
            }
        });
    }

    // TOAST NOTIFICATIONS AUTO-HIDE
    const toasts = document.querySelectorAll('.toast');
    toasts.forEach(toast => {
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(100%)';
            setTimeout(() => toast.remove(), 300);
        }, 5000);
    });

    // CARDS HOVER SOUND EFFECT (Optional)
    const hoverCards = document.querySelectorAll('.card, .choose-card');
    hoverCards.forEach(card => {
        card.addEventListener('mouseenter', function () {
            this.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
        });
    });

    // INFINITE SCROLL (Optional for job listings)
    let loading = false;
    const jobContainer = document.querySelector('.job-listings');
    if (jobContainer) {
        window.addEventListener('scroll', function () {
            if (loading) return;
            
            const scrollPosition = window.innerHeight + window.scrollY;
            const pageHeight = document.documentElement.scrollHeight;
            
            if (scrollPosition >= pageHeight - 100) {
                loading = true;
                // Trigger load more functionality here
                setTimeout(() => { loading = false; }, 1000);
            }
        });
    }

    // SCROLL TO TOP BUTTON
    const scrollTopBtn = document.createElement('button');
    scrollTopBtn.innerHTML = '<i class="bx bx-up-arrow-alt"></i>';
    scrollTopBtn.className = 'scroll-to-top btn btn-danger rounded-circle';
    scrollTopBtn.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 50px;
        height: 50px;
        display: none;
        z-index: 9999;
        transition: all 0.3s ease;
        box-shadow: 0 5px 20px rgba(255, 43, 43, 0.4);
    `;
    document.body.appendChild(scrollTopBtn);

    window.addEventListener('scroll', function () {
        if (window.scrollY > 300) {
            scrollTopBtn.style.display = 'block';
            scrollTopBtn.style.animation = 'fadeIn 0.3s ease';
        } else {
            scrollTopBtn.style.display = 'none';
        }
    });

    scrollTopBtn.addEventListener('click', function () {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    // ENHANCED TABLE SEARCH (if search input exists)
    const tableSearch = document.querySelector('#tableSearch');
    if (tableSearch) {
        tableSearch.addEventListener('keyup', function () {
            const filter = this.value.toLowerCase();
            const table = this.closest('.table-responsive')?.querySelector('table');
            if (table) {
                const rows = table.querySelectorAll('tbody tr');
                rows.forEach(row => {
                    const text = row.textContent.toLowerCase();
                    row.style.display = text.includes(filter) ? '' : 'none';
                    if (row.style.display === '') {
                        row.style.animation = 'fadeIn 0.3s ease';
                    }
                });
            }
        });
    }

    // COUNT UP ANIMATION FOR STATS
    const stats = document.querySelectorAll('.stat-number, .choose-card h3');
    stats.forEach(stat => {
        const target = parseInt(stat.textContent.replace(/\D/g, ''));
        if (target && !isNaN(target)) {
            let current = 0;
            const increment = target / 50;
            const timer = setInterval(() => {
                current += increment;
                if (current >= target) {
                    stat.textContent = target;
                    clearInterval(timer);
                } else {
                    stat.textContent = Math.floor(current);
                }
            }, 30);
        }
    });

    // PARALLAX EFFECT FOR HERO SECTIONS
    const heroSections = document.querySelectorAll('.banner-style-two, .page-title');
    window.addEventListener('scroll', function () {
        heroSections.forEach(section => {
            const scrolled = window.scrollY;
            section.style.backgroundPositionY = `${scrolled * 0.5}px`;
        });
    });

    // IMAGE LAZY LOADING
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                img.style.animation = 'fadeIn 0.5s ease';
                observer.unobserve(img);
            }
        });
    });
    images.forEach(img => imageObserver.observe(img));

    // COPY TO CLIPBOARD FUNCTIONALITY
    const copyButtons = document.querySelectorAll('[data-copy]');
    copyButtons.forEach(btn => {
        btn.addEventListener('click', function () {
            const text = this.getAttribute('data-copy');
            navigator.clipboard.writeText(text).then(() => {
                const original = this.innerHTML;
                this.innerHTML = '<i class="bx bx-check"></i> Copied!';
                setTimeout(() => {
                    this.innerHTML = original;
                }, 2000);
            });
        });
    });

    // CONFIRMATION DIALOGS
    const confirmButtons = document.querySelectorAll('[data-confirm]');
    confirmButtons.forEach(btn => {
        btn.addEventListener('click', function (e) {
            const message = this.getAttribute('data-confirm') || 'Are you sure?';
            if (!confirm(message)) {
                e.preventDefault();
                return false;
            }
        });
    });

    // RESPONSIVE NAVBAR CLOSE ON CLICK
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    navLinks.forEach(link => {
        link.addEventListener('click', function () {
            if (window.innerWidth < 992 && navbarCollapse?.classList.contains('show')) {
                navbarCollapse.classList.remove('show');
            }
        });
    });

    // PRINT FUNCTIONALITY
    const printButtons = document.querySelectorAll('[data-print]');
    printButtons.forEach(btn => {
        btn.addEventListener('click', function () {
            window.print();
        });
    });

    console.log('🎨 Professional animations and interactions loaded successfully!');
});

// UTILITY FUNCTIONS
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.style.cssText = 'position: fixed; top: 20px; right: 20px; z-index: 99999;';
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    document.body.appendChild(toast);
    toast.style.animation = 'slideInRight 0.3s ease';
    
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function animateValue(element, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        element.innerHTML = Math.floor(progress * (end - start) + start);
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}
