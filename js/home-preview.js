// Used only in the generated homepage-only Vercel preview.
(() => {
  const form = document.querySelector('[data-home-preview-form]');
  if (!form) return;
  form.addEventListener('submit', event => {
    event.preventDefault();
    const data = new FormData(form);
    const fields = [
      ['Name', 'name'], ['Phone', 'mobile'], ['Email', 'email'],
      ['Moving from', 'movingfrom'], ['Moving to', 'movingto'], ['Message', 'message']
    ];
    const body = fields.map(([label, key]) => `${label}: ${data.get(key) || ''}`).join('\n');
    window.location.href = 'mailto:info@dhlrexpress.com?subject=' +
      encodeURIComponent('Moving enquiry — DHLR Express') + '&body=' + encodeURIComponent(body);
  });
})();
