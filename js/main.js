/* ============================================================
   Ahmed Sefdine · Portfolio JS
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {

  /* ── Navbar scroll effect ── */
  const navbar = document.getElementById('navbar');
  const backTop = document.getElementById('back-top');

  window.addEventListener('scroll', () => {
    if (window.scrollY > 40) {
      navbar.classList.add('scrolled');
      backTop.classList.add('visible');
    } else {
      navbar.classList.remove('scrolled');
      backTop.classList.remove('visible');
    }

    // Active nav link
    document.querySelectorAll('section[id]').forEach(sec => {
      const link = document.querySelector(`.nav-links a[href="#${sec.id}"]`);
      if (!link) return;
      const rect = sec.getBoundingClientRect();
      if (rect.top <= 100 && rect.bottom >= 100) {
        document.querySelectorAll('.nav-links a').forEach(l => l.classList.remove('active'));
        link.classList.add('active');
      }
    });
  });

  /* ── Back to top ── */
  backTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

  /* ── Mobile menu ── */
  const hamburger = document.getElementById('hamburger');
  const mobileMenu = document.getElementById('mobile-menu');
  const mobileClose = document.getElementById('mobile-close');

  hamburger.addEventListener('click', () => mobileMenu.classList.add('open'));
  mobileClose.addEventListener('click', () => mobileMenu.classList.remove('open'));
  mobileMenu.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => mobileMenu.classList.remove('open'));
  });

  /* ── Scroll fade-in ── */
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('visible');
        observer.unobserve(e.target);
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));

  /* ── Skill bars animate on scroll ── */
  const skillObserver = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.querySelectorAll('.skill-fill').forEach(bar => {
          bar.classList.add('animated');
        });
        skillObserver.unobserve(e.target);
      }
    });
  }, { threshold: 0.2 });

  document.querySelectorAll('.skill-group').forEach(g => skillObserver.observe(g));

  /* ── Contact form ── */
  const form = document.getElementById('contact-form');
  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const nom   = form.querySelector('#f-nom').value.trim();
      const email = form.querySelector('#f-email').value.trim();
      const msg   = form.querySelector('#f-msg').value.trim();
      if (nom && email && msg) {
        document.getElementById('form-success').style.display = 'block';
        form.reset();
        setTimeout(() => {
          document.getElementById('form-success').style.display = 'none';
        }, 5000);
      }
    });
  }

  /* ── Smooth scroll for all anchor links ── */
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', function(e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        const offset = document.getElementById('navbar').offsetHeight;
        window.scrollTo({
          top: target.getBoundingClientRect().top + window.scrollY - offset,
          behavior: 'smooth'
        });
      }
    });
  });

  /* ── Year in footer ── */
  const yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

});
