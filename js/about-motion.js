(() => {
  'use strict';
  if (!document.querySelector('.about-modern, .services-modern, .contact-modern, .network-modern, .home-welcome')) return;

  const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
  if (motion.matches || !('IntersectionObserver' in window)) return;

  const targets = document.querySelectorAll(
    '.page-hero .breadcrumb, .page-hero .eyebrow, .page-hero h1, ' +
    '.about-modern .eyebrow, .about-modern h2, .about-modern h3, ' +
    '.about-modern p, .about-modern .section-index > span, ' +
    '.about-modern .about-value-number, .about-modern .about-topic-number, ' +
    '.about-modern .about-photo-note > span, .about-modern .about-photo-note strong, ' +
    '.services-modern .tab-content h2, .services-modern .tab-content h3, ' +
    '.services-modern .tab-content h4, .services-modern .tab-content p, ' +
    '.services-modern .tab-content li, ' +
    '.services-directory .eyebrow, .services-directory h2, ' +
    '.services-directory .card-number, .services-directory h3, .services-directory p, ' +
    '.contact-modern .eyebrow, .contact-modern h2, .contact-modern h3, ' +
    '.contact-modern p, .contact-modern .section-index > span, ' +
    '.contact-modern .contact-channel, .contact-modern .contact-office-body, ' +
    '.contact-modern .contact-office-top, .contact-enquiry h2, .contact-enquiry p, ' +
    '.network-modern .eyebrow, .network-modern h2, .network-modern p:not(.network-results), ' +
    '.network-modern .section-index > span, .network-modern .network-help, ' +
    '.network-modern .network-city-card h3, ' +
    '.home-welcome .eyebrow, .home-welcome h2, .home-welcome p, ' +
    '.home-welcome .home-welcome-banner > span:not([aria-hidden])'
  );
  const directions = ['left', 'bottom', 'right', 'top'];
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('text-visible');
      observer.unobserve(entry.target);
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -18px 0px' });

  targets.forEach((element, index) => {
    element.dataset.textDirection = directions[index % directions.length];
    element.style.setProperty('--text-delay', `${(index % 3) * 65}ms`);
    element.classList.add('text-reveal');
    observer.observe(element);
  });

  function revealAll() {
    targets.forEach(element => element.classList.add('text-visible'));
    observer.disconnect();
  }
  motion.addEventListener?.('change', event => {
    if (event.matches) revealAll();
  });
  // Print the complete copy even when some sections have not been scrolled into view.
  window.addEventListener('beforeprint', revealAll);
})();
