// L.G.E.A Staff School Portal — Main JavaScript
'use strict';

document.addEventListener('DOMContentLoaded', function () {

  // ── Navbar scroll effect ──────────────────────────────────────────────
  const nav = document.getElementById('mainNav');
  if (nav) {
    window.addEventListener('scroll', function () {
      if (window.scrollY > 50) {
        nav.style.boxShadow = '0 4px 24px rgba(0,0,0,0.18)';
      } else {
        nav.style.boxShadow = '0 1px 4px rgba(0,0,0,0.08)';
      }
    });
  }

  // ── Auto-dismiss alerts after 5s ─────────────────────────────────────
  const alerts = document.querySelectorAll('.alert.alert-dismissible');
  alerts.forEach(function (alert) {
    setTimeout(function () {
      const bsAlert = new bootstrap.Alert(alert);
      bsAlert.close();
    }, 5000);
  });

  // ── Animated counter for stat numbers ────────────────────────────────
  function animateCounter(el, target, duration) {
    let start = 0;
    const step = Math.ceil(target / (duration / 16));
    const timer = setInterval(function () {
      start += step;
      if (start >= target) {
        el.textContent = target;
        clearInterval(timer);
      } else {
        el.textContent = start;
      }
    }, 16);
  }

  const observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        const el = entry.target;
        const text = el.textContent.replace(/[^0-9]/g, '');
        const target = parseInt(text, 10);
        if (!isNaN(target) && target > 0) {
          animateCounter(el, target, 1500);
        }
        observer.unobserve(el);
      }
    });
  }, { threshold: 0.5 });

  document.querySelectorAll('.stat-num, .hero-stat .number').forEach(function (el) {
    observer.observe(el);
  });

  // ── Active nav link highlighting ──────────────────────────────────────
  const currentPath = window.location.pathname;
  document.querySelectorAll('.navbar-nav .nav-link').forEach(function (link) {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active');
    }
  });

  // ── Form loading state ────────────────────────────────────────────────
  document.querySelectorAll('form').forEach(function (form) {
    form.addEventListener('submit', function () {
      const btn = form.querySelector('[type="submit"]');
      if (btn && !btn.disabled) {
        btn.dataset.originalText = btn.innerHTML;
        btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status"></span>Processing...';
        btn.disabled = true;
      }
    });
  });

  // ── Smooth scroll for anchor links ────────────────────────────────────
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // ── Tooltip initialization ────────────────────────────────────────────
  const tooltipEls = document.querySelectorAll('[data-bs-toggle="tooltip"]');
  tooltipEls.forEach(function (el) {
    new bootstrap.Tooltip(el);
  });

  // ── Gallery lightbox-style click (simple) ────────────────────────────
  document.querySelectorAll('.gallery-img').forEach(function (img) {
    img.addEventListener('click', function () {
      const modal = document.createElement('div');
      modal.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,0.9);display:flex;align-items:center;justify-content:center;z-index:9999;cursor:pointer;';
      const image = document.createElement('img');
      image.src = this.src;
      image.style.cssText = 'max-width:90vw;max-height:90vh;border-radius:12px;box-shadow:0 0 60px rgba(0,0,0,0.5);';
      modal.appendChild(image);
      modal.addEventListener('click', function () { document.body.removeChild(modal); });
      document.body.appendChild(modal);
    });
  });

  // ── Back to top button ────────────────────────────────────────────────
  const backBtn = document.createElement('button');
  backBtn.innerHTML = '<i class="bi bi-arrow-up"></i>';
  backBtn.id = 'backToTop';
  backBtn.title = 'Back to top';
  backBtn.style.cssText = 'position:fixed;bottom:24px;right:24px;width:44px;height:44px;border-radius:50%;background:var(--primary);color:#fff;border:none;display:none;align-items:center;justify-content:center;cursor:pointer;z-index:999;box-shadow:0 4px 16px rgba(0,107,63,0.4);font-size:1.1rem;transition:all 0.3s;';
  document.body.appendChild(backBtn);

  window.addEventListener('scroll', function () {
    backBtn.style.display = window.scrollY > 400 ? 'flex' : 'none';
  });
  backBtn.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
  backBtn.addEventListener('mouseenter', function () { this.style.background = 'var(--primary-dark)'; this.style.transform = 'scale(1.1)'; });
  backBtn.addEventListener('mouseleave', function () { this.style.background = 'var(--primary)'; this.style.transform = 'scale(1)'; });

});
