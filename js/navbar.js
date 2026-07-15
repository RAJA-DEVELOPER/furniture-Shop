/**
 * LUMIÈRE HOME — Navbar Module
 * Sticky, Glassmorphism, Mobile Menu, Dropdowns
 */

'use strict';

const initNavbar = () => {
  const navbar = document.querySelector('.navbar');
  if (!navbar) return;

  const hamburger = navbar.querySelector('.navbar__hamburger');
  const mobileMenu = document.querySelector('.navbar__mobile-menu');
  const overlay = document.querySelector('.mobile-menu-overlay');
  const closeBtn = mobileMenu?.querySelector('.mobile-menu-close');
  const isHero = navbar.classList.contains('navbar--transparent');

  /* ── Scroll: sticky + glass ── */
  const handleScroll = () => {
    if (isHero) {
      navbar.classList.toggle('navbar--scrolled', window.scrollY > 80);
    }
  };

  window.addEventListener('scroll', handleScroll, { passive: true });
  handleScroll(); // init state

  /* ── Mobile menu ── */
  const openMenu = () => {
    hamburger?.classList.add('open');
    mobileMenu?.classList.add('open');
    overlay?.classList.add('open');
    document.body.style.overflow = 'hidden';
  };

  const closeMenu = () => {
    hamburger?.classList.remove('open');
    mobileMenu?.classList.remove('open');
    overlay?.classList.remove('open');
    document.body.style.overflow = '';
  };

  hamburger?.addEventListener('click', () => {
    hamburger.classList.contains('open') ? closeMenu() : openMenu();
  });

  closeBtn?.addEventListener('click', closeMenu);
  overlay?.addEventListener('click', closeMenu);

  // Close on link click
  mobileMenu?.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', closeMenu);
  });

  // Keyboard: Escape closes
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeMenu();
  });

  /* ── Active link highlighting ── */
  const currentPath = window.location.pathname.split('/').pop() || 'index.html';
  navbar.querySelectorAll('.nav-link, .mobile-nav-links a').forEach((link) => {
    const href = link.getAttribute('href')?.split('/').pop() || '';
    if (href === currentPath || (currentPath === '' && href === 'index.html')) {
      link.classList.add('active');
    }
  });
};

/* ── RTL Toggle ── */
const initRTL = () => {
  const target = document.body;
  const saved = localStorage.getItem('lumiere-dir');
  if (saved === 'rtl') target.setAttribute('dir', 'rtl');

  document.querySelectorAll('.rtl-toggle').forEach((btn) => {
    btn.addEventListener('click', () => {
      const next = target.getAttribute('dir') === 'rtl' ? 'ltr' : 'rtl';
      target.setAttribute('dir', next);
      localStorage.setItem('lumiere-dir', next);
      btn.classList.toggle('active', next === 'rtl');
    });
  });
};

document.addEventListener('DOMContentLoaded', initNavbar);
document.addEventListener('DOMContentLoaded', initRTL);
