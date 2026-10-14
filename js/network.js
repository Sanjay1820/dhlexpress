(() => {
  'use strict';
  const input = document.querySelector('#network-search');
  if (!input) return;
  const locations = [...document.querySelectorAll('.network-location')];
  const clear = document.querySelector('#network-search-clear');
  const status = document.querySelector('.network-results');
  const empty = document.querySelector('.network-no-results');
  const normalize = value => value.toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();
  function filter() {
    const words = normalize(input.value).split(' ').filter(Boolean);
    let count = 0;
    locations.forEach(location => {
      const match = words.every(word => normalize(location.textContent).includes(word));
      location.hidden = !match;
      if (match) count++;
    });
    status.textContent = `${count} ${count === 1 ? 'location' : 'locations'}`;
    clear.hidden = !input.value;
    empty.hidden = count !== 0;
  }
  input.addEventListener('input', filter);
  clear.addEventListener('click', () => {
    input.value = '';
    filter();
    input.focus();
  });
  filter();
})();
