(() => {
  'use strict';
  const slides = [...document.querySelectorAll('.hero-slide')];
  const dots = [...document.querySelectorAll('.dot')];
  const hero = document.querySelector('.hero');
  if (!hero || !slides.length) return;
  const pauseButton = document.querySelector('[data-slider-pause]');
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  let current = 0;
  let timer;
  let paused = motion.matches;
  const duration = 5000;

  function show(index) {
    current = (index + slides.length) % slides.length;
    slides.forEach((slide, i) => {
      const active = i === current;
      slide.classList.toggle('active', active);
      slide.setAttribute('aria-hidden', String(!active));
      slide.inert = !active;
    });
    dots.forEach((dot, i) => dot.setAttribute('aria-current', String(i === current)));
    const label = document.querySelector('.slide-label');
    if (label) label.textContent = `${String(current + 1).padStart(2, '0')} / ${String(slides.length).padStart(2, '0')}`;
  }
  function stop() {
    clearTimeout(timer);
    timer = undefined;
  }
  function start() {
    stop();
    if (!paused && !document.hidden && slides.length > 1) {
      timer = setTimeout(() => {
        show(current + 1);
        start();
      }, duration);
    }
  }
  function updatePauseButton() {
    if (!pauseButton) return;
    pauseButton.textContent = paused ? '▶' : 'Ⅱ';
    pauseButton.setAttribute('aria-label', paused ? 'Play slideshow' : 'Pause slideshow');
  }
  function navigate(index) {
    show(index);
    start();
  }
  hero.querySelectorAll('.hero-photo').forEach(photo => {
    photo.loading = 'eager';
    photo.decoding = 'async';
  });
  show(0);
  updatePauseButton();
  start();
  dots.forEach((dot, index) => dot.addEventListener('click', () => navigate(index)));
  document.querySelector('[data-slider-prev]')?.addEventListener('click', () => navigate(current - 1));
  document.querySelector('[data-slider-next]')?.addEventListener('click', () => navigate(current + 1));
  pauseButton?.addEventListener('click', () => {
    paused = !paused;
    updatePauseButton();
    start();
  });
  // Pointer movement over the banner does not interrupt autoplay.
  hero.addEventListener('focusin', stop);
  hero.addEventListener('focusout', event => {
    if (!hero.contains(event.relatedTarget)) start();
  });
  hero.addEventListener('keydown', event => {
    if (event.key === 'ArrowRight') { event.preventDefault(); navigate(current + 1); }
    if (event.key === 'ArrowLeft') { event.preventDefault(); navigate(current - 1); }
  });
  document.addEventListener('visibilitychange', start);
  motion.addEventListener?.('change', event => {
    paused = event.matches;
    updatePauseButton();
    start();
  });
})();
