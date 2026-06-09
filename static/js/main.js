/**
 * CarBazar — Main JavaScript
 */

/* ============================================================
   THEME TOGGLE — runs immediately to prevent flash
   ============================================================ */
(function () {
  var saved = localStorage.getItem('carbazar-theme') || 'dark';
  document.documentElement.setAttribute('data-theme', saved);
})();

document.addEventListener('DOMContentLoaded', function () {

  /* ---------- Theme Toggle ---------- */
  var btnDesktop  = document.getElementById('themeToggleBtnDesktop');
  var btnMobile   = document.getElementById('themeToggleBtn');
  var iconDesktop = document.getElementById('themeIcon');
  var iconMobile  = document.getElementById('themeIconMobile');
  var label       = document.getElementById('themeLabel');

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('carbazar-theme', theme);
    var isLight = theme === 'light';
    var iconClass = isLight ? 'bi bi-sun-fill' : 'bi bi-moon-fill';
    var labelText = isLight ? 'Light' : 'Dark';
    if (iconDesktop) iconDesktop.className = iconClass;
    if (iconMobile)  iconMobile.className  = iconClass;
    if (label) label.textContent = labelText;
    // Update toggle track active state
    [btnDesktop, btnMobile].forEach(function(b) {
      if (b) b.classList.toggle('is-light', isLight);
    });
  }

  function toggle() {
    var current = document.documentElement.getAttribute('data-theme') || 'dark';
    applyTheme(current === 'light' ? 'dark' : 'light');
  }

  // Init
  applyTheme(localStorage.getItem('carbazar-theme') || 'dark');

  if (btnDesktop) btnDesktop.addEventListener('click', toggle);
  if (btnMobile)  btnMobile.addEventListener('click', toggle);

  // ============================================================
  // NAVBAR: scroll shadow
  // ============================================================
  const nav = document.getElementById('mainNav');
  if (nav) {
    window.addEventListener('scroll', function () {
      if (window.scrollY > 30) {
        nav.style.boxShadow = '0 4px 30px rgba(0,0,0,0.5)';
      } else {
        nav.style.boxShadow = 'none';
      }
    }, { passive: true });
  }

  // ============================================================
  // AUTO-DISMISS TOASTS
  // ============================================================
  document.querySelectorAll('.toast').forEach(function (toastEl) {
    setTimeout(function () {
      var toast = bootstrap.Toast.getOrCreateInstance(toastEl);
      toast.hide();
    }, 4500);
  });

  // ============================================================
  // IMAGE PREVIEW — Main image
  // ============================================================
  var mainImageInput = document.querySelector('[name="main_image"]');
  var mainPreview = document.getElementById('mainImgPreview');
  if (mainImageInput && mainPreview) {
    mainImageInput.addEventListener('change', function (e) {
      mainPreview.innerHTML = '';
      if (e.target.files && e.target.files[0]) {
        var img = document.createElement('img');
        img.src = URL.createObjectURL(e.target.files[0]);
        img.classList.add('img-preview-single');
        img.onload = function () { URL.revokeObjectURL(img.src); };
        mainPreview.appendChild(img);
      }
    });
  }

  // ============================================================
  // IMAGE PREVIEW — Gallery (multiple)
  // ============================================================
  var galleryInput = document.querySelector('[name="images"]');
  var galleryPreview = document.getElementById('galleryPreview');
  if (galleryInput && galleryPreview) {
    galleryInput.addEventListener('change', function (e) {
      galleryPreview.innerHTML = '';
      if (e.target.files) {
        Array.from(e.target.files).forEach(function (file) {
          var img = document.createElement('img');
          img.src = URL.createObjectURL(file);
          img.classList.add('img-preview-thumb');
          img.onload = function () { URL.revokeObjectURL(img.src); };
          galleryPreview.appendChild(img);
        });
      }
    });
  }

  // ============================================================
  // SEARCH — debounce on list page (auto-submit on pause)
  // ============================================================
  var searchInput = document.querySelector('#filterForm [name="q"]');
  if (searchInput) {
    var debounceTimer;
    searchInput.addEventListener('input', function () {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(function () {
        // Only auto-submit if user has paused typing for 800ms
        // and there's at least 2 chars (or cleared field)
        var val = searchInput.value.trim();
        if (val.length >= 2 || val.length === 0) {
          document.getElementById('filterForm').submit();
        }
      }, 800);
    });
  }

  // ============================================================
  // FILTER FORM — select auto-submit
  // ============================================================
  var filterSelects = document.querySelectorAll('#filterForm select');
  filterSelects.forEach(function (sel) {
    sel.addEventListener('change', function () {
      document.getElementById('filterForm').submit();
    });
  });

  // ============================================================
  // SMOOTH ANCHOR SCROLLING
  // ============================================================
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      var target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // ============================================================
  // CARD HOVER: add ripple-like pulse to car cards
  // ============================================================
  document.querySelectorAll('.car-card').forEach(function (card) {
    card.addEventListener('mouseenter', function () {
      this.style.willChange = 'transform';
    });
    card.addEventListener('mouseleave', function () {
      this.style.willChange = 'auto';
    });
  });

  // ============================================================
  // COPY LINK (fallback for older browsers on detail page)
  // ============================================================
  window.copyLink = function () {
    var btn = document.getElementById('copyLinkBtn');
    if (!btn) return;
    if (navigator.clipboard) {
      navigator.clipboard.writeText(window.location.href).then(function () {
        btn.innerHTML = '<i class="bi bi-check-lg me-1"></i>Copied!';
        btn.classList.add('btn-success');
        btn.classList.remove('btn-outline-secondary');
        setTimeout(function () {
          btn.innerHTML = '<i class="bi bi-link-45deg me-1"></i>Copy Link';
          btn.classList.remove('btn-success');
          btn.classList.add('btn-outline-secondary');
        }, 2000);
      });
    } else {
      // Fallback
      var el = document.createElement('input');
      el.value = window.location.href;
      document.body.appendChild(el);
      el.select();
      document.execCommand('copy');
      document.body.removeChild(el);
      if (btn) {
        btn.textContent = 'Copied!';
        setTimeout(function () { btn.textContent = 'Copy Link'; }, 2000);
      }
    }
  };

  // ============================================================
  // DELETE CONFIRMATION (fallback — also declared inline)
  // ============================================================
  window.confirmDelete = function () {
    if (confirm('Are you sure you want to delete this listing? This action cannot be undone.')) {
      var form = document.getElementById('deleteForm');
      if (form) form.submit();
    }
  };

  // ============================================================
  // DASHBOARD: animate stat numbers
  // ============================================================
  function animateNumber(el) {
    var target = parseInt(el.textContent.replace(/[^0-9]/g, ''), 10);
    if (!target || isNaN(target)) return;
    var start = 0;
    var duration = 1000;
    var startTime = null;
    function step(timestamp) {
      if (!startTime) startTime = timestamp;
      var progress = Math.min((timestamp - startTime) / duration, 1);
      var eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
      el.textContent = Math.floor(eased * target);
      if (progress < 1) requestAnimationFrame(step);
      else el.textContent = target;
    }
    requestAnimationFrame(step);
  }

  var statValues = document.querySelectorAll('.dash-stat-value');
  if (statValues.length > 0) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          animateNumber(entry.target);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.2 });
    statValues.forEach(function (el) { observer.observe(el); });
  }

  // ============================================================
  // BRAND STAT BARS: animate width
  // ============================================================
  document.querySelectorAll('.brand-stat-fill').forEach(function (bar) {
    var width = bar.style.width;
    bar.style.width = '0%';
    setTimeout(function () {
      bar.style.transition = 'width 0.8s ease';
      bar.style.width = width || '20%';
    }, 300);
  });

});
