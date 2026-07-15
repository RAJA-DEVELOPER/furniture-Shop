/**
 * LUMIÈRE HOME — Hero Slider
 * Auto-play, drag/swipe, dots, keyboard navigation
 */

'use strict';

const initHeroSlider = (sliderEl) => {
  if (!sliderEl) return;

  const track = sliderEl.querySelector('.hero-slider__track');
  const slides = sliderEl.querySelectorAll('.hero-slider__slide');
  const dotsContainer = sliderEl.querySelector('.hero-slider__dots');
  const prevBtn = sliderEl.querySelector('.hero-slider__prev');
  const nextBtn = sliderEl.querySelector('.hero-slider__next');

  if (!track || slides.length === 0) return;

  let current = 0;
  let autoplayTimer = null;
  let isTransitioning = false;
  const total = slides.length;

  /* ── Build Dots ── */
  if (dotsContainer) {
    slides.forEach((_, i) => {
      const dot = document.createElement('button');
      dot.className = `dot ${i === 0 ? 'active' : ''}`;
      dot.setAttribute('aria-label', `Slide ${i + 1}`);
      dot.addEventListener('click', () => goTo(i));
      dotsContainer.appendChild(dot);
    });
  }

  const getDots = () => dotsContainer?.querySelectorAll('.dot') || [];

  /* ── Go To Slide ── */
  const goTo = (index) => {
    if (isTransitioning) return;
    isTransitioning = true;

    const prev = current;
    current = (index + total) % total;

    slides[prev].classList.remove('active');
    slides[current].classList.add('active');

    getDots().forEach((d, i) => d.classList.toggle('active', i === current));

    setTimeout(() => { isTransitioning = false; }, 800);
  };

  const next = () => goTo(current + 1);
  const prev = () => goTo(current - 1);

  /* ── Auto-play ── */
  const startAutoplay = () => {
    stopAutoplay();
    autoplayTimer = setInterval(next, 5500);
  };

  const stopAutoplay = () => {
    if (autoplayTimer) clearInterval(autoplayTimer);
  };

  /* ── Controls ── */
  prevBtn?.addEventListener('click', () => { prev(); startAutoplay(); });
  nextBtn?.addEventListener('click', () => { next(); startAutoplay(); });

  // Keyboard
  sliderEl.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft') { prev(); startAutoplay(); }
    if (e.key === 'ArrowRight') { next(); startAutoplay(); }
  });

  // Touch / swipe
  let touchStartX = 0;
  sliderEl.addEventListener('touchstart', (e) => {
    touchStartX = e.touches[0].clientX;
  }, { passive: true });

  sliderEl.addEventListener('touchend', (e) => {
    const delta = touchStartX - e.changedTouches[0].clientX;
    if (Math.abs(delta) > 50) {
      delta > 0 ? next() : prev();
      startAutoplay();
    }
  }, { passive: true });

  // Pause on hover
  sliderEl.addEventListener('mouseenter', stopAutoplay);
  sliderEl.addEventListener('mouseleave', startAutoplay);

  /* ── Init ── */
  slides[0]?.classList.add('active');
  startAutoplay();
};

const initGenericSlider = (containerEl) => {
  if (!containerEl) return;

  const track = containerEl.querySelector('.slider-track');
  const items = track?.querySelectorAll('.slider-item');
  const prevBtn = containerEl.querySelector('.slider-prev');
  const nextBtn = containerEl.querySelector('.slider-next');
  const dotsWrap = containerEl.querySelector('.slider-dots');

  if (!track || !items?.length) return;

  let currentIndex = 0;
  const total = items.length;
  const getVisibleCount = () => {
    if (window.innerWidth >= 1024) return parseInt(containerEl.dataset.desktop || 3, 10);
    if (window.innerWidth >= 768)  return parseInt(containerEl.dataset.tablet || 2, 10);
    return 1;
  };

  const getMaxIndex = () => Math.max(0, total - getVisibleCount());

  const update = () => {
    const visible = getVisibleCount();
    const pct = 100 / visible;
    track.style.transform = `translateX(-${currentIndex * pct}%)`;
    dotsWrap?.querySelectorAll('.dot').forEach((d, i) => {
      d.classList.toggle('active', i === currentIndex);
    });
  };

  if (dotsWrap) {
    const numDots = getMaxIndex() + 1;
    for (let i = 0; i < numDots; i++) {
      const dot = document.createElement('button');
      dot.className = `dot ${i === 0 ? 'active' : ''}`;
      dot.addEventListener('click', () => { currentIndex = i; update(); });
      dotsWrap.appendChild(dot);
    }
  }

  prevBtn?.addEventListener('click', () => {
    currentIndex = Math.max(0, currentIndex - 1);
    update();
  });

  nextBtn?.addEventListener('click', () => {
    currentIndex = Math.min(getMaxIndex(), currentIndex + 1);
    update();
  });

  window.addEventListener('resize', update, { passive: true });
  update();
};

document.addEventListener('DOMContentLoaded', () => {
  initHeroSlider(document.querySelector('.hero-slider'));
  document.querySelectorAll('.generic-slider').forEach(initGenericSlider);
});
