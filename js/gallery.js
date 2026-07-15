/**
 * LUMIÈRE HOME — Gallery Module
 * Filter tabs + Lightbox
 */

'use strict';

const initGalleryFilter = () => {
  const filterBtns = document.querySelectorAll('[data-filter]');
  const galleryItems = document.querySelectorAll('[data-category]');

  if (!filterBtns.length || !galleryItems.length) return;

  filterBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      const filter = btn.dataset.filter;

      // Active state
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      // Filter items
      galleryItems.forEach((item) => {
        const category = item.dataset.category;
        const show = filter === 'all' || category === filter;

        if (show) {
          item.style.display = '';
          item.style.animation = 'scaleIn 0.4s ease forwards';
        } else {
          item.style.display = 'none';
        }
      });
    });
  });
};

/* ══════════════════════════════════════════════
   LIGHTBOX
══════════════════════════════════════════════ */
const initLightbox = () => {
  const triggers = document.querySelectorAll('[data-lightbox]');
  if (!triggers.length) return;

  // Build lightbox DOM
  const lightbox = document.createElement('div');
  lightbox.className = 'lightbox-overlay';
  lightbox.innerHTML = `
    <div class="lightbox-container">
      <button class="lightbox-close" aria-label="Close lightbox">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="24" height="24"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
      </button>
      <button class="lightbox-prev" aria-label="Previous">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="24" height="24"><polyline points="15 18 9 12 15 6"/></svg>
      </button>
      <div class="lightbox-content">
        <div class="lightbox-image"></div>
        <div class="lightbox-caption"></div>
      </div>
      <button class="lightbox-next" aria-label="Next">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="24" height="24"><polyline points="9 18 15 12 9 6"/></svg>
      </button>
    </div>
  `;
  document.body.appendChild(lightbox);

  const items = Array.from(triggers);
  let current = 0;

  const show = (index) => {
    current = (index + items.length) % items.length;
    const item = items[current];
    const caption = item.dataset.caption || '';
    const bg = item.querySelector('.img-placeholder')?.style.background
      || item.querySelector('[data-bg]')?.dataset.bg
      || 'linear-gradient(135deg, #EADBC8, #F5EEE4)';

    lightbox.querySelector('.lightbox-image').style.background = bg;
    lightbox.querySelector('.lightbox-caption').textContent = caption;
    lightbox.classList.add('open');
    document.body.style.overflow = 'hidden';
  };

  const close = () => {
    lightbox.classList.remove('open');
    document.body.style.overflow = '';
  };

  triggers.forEach((el, i) => {
    el.style.cursor = 'pointer';
    el.addEventListener('click', () => show(i));
  });

  lightbox.querySelector('.lightbox-close').addEventListener('click', close);
  lightbox.querySelector('.lightbox-prev').addEventListener('click', () => show(current - 1));
  lightbox.querySelector('.lightbox-next').addEventListener('click', () => show(current + 1));

  lightbox.addEventListener('click', (e) => {
    if (e.target === lightbox) close();
  });

  document.addEventListener('keydown', (e) => {
    if (!lightbox.classList.contains('open')) return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowLeft') show(current - 1);
    if (e.key === 'ArrowRight') show(current + 1);
  });
};

document.addEventListener('DOMContentLoaded', () => {
  initGalleryFilter();
  initLightbox();
});
