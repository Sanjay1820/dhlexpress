(() => {
  'use strict';
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  document.querySelectorAll('[data-content-carousel]').forEach(section => {
    const track = section.querySelector('[data-carousel-track]');
    const prev = section.querySelector('[data-carousel-prev]');
    const next = section.querySelector('[data-carousel-next]');
    const status = section.querySelector('[data-carousel-status]');
    const pause = section.querySelector('[data-carousel-pause]');
    const items = [...track.children];
    if (!items.length) return;
    const coverflow = section.id === 'customer-reviews';
    let allItems = items;
    let nearest = 0;
    let active = 0;
    let settleTimer;
    if (coverflow) {
      const clone = item => {
        const copy = item.cloneNode(true);
        copy.setAttribute('aria-hidden', 'true');
        copy.inert = true;
        copy.classList.add('review-clone');
        return copy;
      };
      track.prepend(...items.map(clone));
      track.append(...items.map(clone));
      allItems = [...track.children];
      section.classList.add('reviews-coverflow');
      nearest = items.length;
    }
    const duration = section.id === 'clients' ? 1800 : 3000;
    let timer;
    let paused = motion.matches;
    let hovered = false;
    let focused = false;
    const maximum = () => Math.max(0, track.scrollWidth - track.clientWidth);
    function stop() {
      clearTimeout(timer);
      timer = undefined;
    }
    function start() {
      stop();
      if (paused || hovered || focused || document.hidden || maximum() <= 2) return;
      timer = setTimeout(() => {
        move(1);
        start();
      }, duration);
    }
    function updatePause() {
      if (!pause) return;
      pause.textContent = paused ? '▶' : 'Ⅱ';
      pause.setAttribute('aria-label', paused ? 'Play automatic sliding' : 'Pause automatic sliding');
      pause.setAttribute('aria-pressed', String(paused));
    }
    function stepSize() {
      return items[0].offsetWidth + (parseFloat(getComputedStyle(track).columnGap) || 0);
    }
    function center(index, smooth = false) {
      const item = allItems[index];
      track.scrollTo({
        left: item.offsetLeft - (track.clientWidth - item.offsetWidth) / 2,
        behavior: smooth && !motion.matches ? 'smooth' : 'instant'
      });
    }
    function update() {
      const step = stepSize();
      if (coverflow) {
        const middle = track.scrollLeft + track.clientWidth / 2;
        nearest = Math.max(0, Math.min(allItems.length - 1,
          Math.round((middle - allItems[0].offsetLeft - items[0].offsetWidth / 2) / step)));
        active = ((nearest - items.length) % items.length + items.length) % items.length;
        allItems.forEach((item, index) => {
          const distance = (item.offsetLeft + item.offsetWidth / 2 - middle) / step;
          const amount = Math.abs(distance);
          item.style.setProperty('--review-scale', String(Math.max(.74, 1 - amount * .15)));
          item.style.setProperty('--review-turn', `${Math.max(-23, Math.min(23, -distance * 17))}deg`);
          item.style.setProperty('--review-drop', `${Math.min(28, amount * 18)}px`);
          item.style.setProperty('--review-opacity', String(Math.max(.45, 1 - amount * .22)));
          item.style.zIndex = String(Math.max(1, 20 - Math.round(amount * 5)));
          item.classList.toggle('review-centered', index === nearest);
        });
        prev.disabled = next.disabled = items.length <= 1;
        status.textContent = `${active + 1} / ${items.length}`;
        return;
      }
      const first = Math.max(0, Math.round(track.scrollLeft / step));
      const visible = Math.max(1, Math.round(track.clientWidth / step));
      prev.disabled = next.disabled = maximum() <= 2;
      status.textContent = `${first + 1}–${Math.min(items.length, first + visible)} / ${items.length}`;
    }
    function move(direction) {
      if (coverflow) {
        center(Math.max(0, Math.min(allItems.length - 1, nearest + direction)), true);
        return;
      }
      let left = track.scrollLeft + direction * stepSize();
      if (direction > 0 && track.scrollLeft >= maximum() - 2) left = 0;
      if (direction < 0 && track.scrollLeft <= 2) left = maximum();
      track.scrollTo({ left: Math.max(0, Math.min(maximum(), left)), behavior: motion.matches ? 'instant' : 'smooth' });
    }
    prev.addEventListener('click', () => { move(-1); start(); });
    next.addEventListener('click', () => { move(1); start(); });
    pause?.addEventListener('click', () => {
      paused = !paused;
      focused = false;
      updatePause();
      start();
    });
    section.addEventListener('pointerenter', event => {
      if (event.pointerType !== 'mouse') return;
      hovered = true;
      stop();
    });
    section.addEventListener('pointerleave', () => { hovered = false; start(); });
    section.addEventListener('focusin', () => { focused = true; stop(); });
    section.addEventListener('focusout', event => {
      if (!section.contains(event.relatedTarget)) { focused = false; start(); }
    });
    track.addEventListener('pointerdown', stop);
    track.addEventListener('pointerup', start);
    track.addEventListener('pointercancel', start);
    track.addEventListener('scroll', () => {
      update();
      if (!coverflow) return;
      clearTimeout(settleTimer);
      settleTimer = setTimeout(() => {
        // Jump between identical copies only after movement stops, for a continuous loop.
        if (nearest < items.length || nearest >= items.length * 2) {
          center(items.length + active);
          update();
        }
      }, 180);
    }, { passive: true });
    if (coverflow) track.addEventListener('keydown', event => {
      if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
      event.preventDefault();
      move(event.key === 'ArrowLeft' ? -1 : 1);
      start();
    });
    document.addEventListener('visibilitychange', start);
    motion.addEventListener?.('change', event => {
      paused = event.matches;
      updatePause();
      start();
    });
    const resize = () => {
      if (coverflow) center(items.length + active);
      update();
      start();
    };
    if ('ResizeObserver' in window) new ResizeObserver(resize).observe(track);
    else window.addEventListener('resize', resize);
    if (coverflow) center(items.length);
    update();
    updatePause();
    start();
  });
})();
