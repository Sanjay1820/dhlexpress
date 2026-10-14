import { readFile, writeFile, mkdir, copyFile, readdir, stat } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const output = path.join(root, 'dist');
await mkdir(output, { recursive: true });

// Refuse unexpected server/page files in the generated output instead of deleting them.
async function checkOutput(directory) {
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const file = path.join(directory, entry.name);
    if (entry.isDirectory()) await checkOutput(file);
    else if (/\.(?:html?|php\d*|py|mjs|json)$/i.test(entry.name) && file !== path.join(output, 'index.html')) {
      throw new Error(`Unexpected non-homepage file in deployment output: ${file}`);
    }
  }
}
await checkOutput(output);

let html = await readFile(path.join(root, 'index.html'), 'utf8');
html = html.replace('<section class="section"><div class="wrap split"><div class="image-composition">',
  '<section class="section" id="home-about"><div class="wrap split"><div class="image-composition">');
html = html.replace('<section class="section"><div class="wrap"><span class="eyebrow">A NETWORK THAT MOVES WITH YOU',
  '<section class="section" id="home-network"><div class="wrap"><span class="eyebrow">A NETWORK THAT MOVES WITH YOU');

// Only the generated preview changes its navigation; the full source stays intact.
html = html.replace(/(<a\b[^>]*\bhref=")([^"#]+\.html)(#[^"]*)?("[^>]*>)/gi, (_, before, target, fragment, after) => {
  if (/^(?:https?:)?\/\//i.test(target)) return before + target + (fragment || '') + after;
  const name = path.posix.basename(target);
  const destination = name === 'index.html' ? (fragment || '/')
    : name === 'about-us.html' ? '#home-about'
    : name === 'contact.html' ? '#quote'
    : name === 'networks.html' || name.startsWith('packers-and-movers-') ? '#home-network'
    : '#home-services';
  return before + destination + after;
});

html = html.replace('action="contact-form-handler-side.php" method="post"',
  'action="mailto:info@dhlrexpress.com" method="get" data-home-preview-form');
html = html.replace('Request my free quote <span>', 'Email my moving enquiry <span>');
html = html.replace('By submitting, you agree that DHLR Express may contact you about your enquiry.',
  'Opens your email app to send this enquiry to DHLR Express.');
html = html.replace('</head>', '<script defer src="js/home-preview.js"></script></head>');

const assetQueue = [];
const copied = new Set();
function addAsset(reference, parent = '') {
  if (!reference || /^(?:[a-z][a-z\d+.-]*:|\/\/|#)/i.test(reference)) return;
  const clean = decodeURIComponent(reference.split(/[?#]/)[0]);
  const relative = path.posix.normalize(path.posix.join(path.posix.dirname(parent || 'index.html'), clean));
  if (relative.startsWith('../') || path.posix.isAbsolute(relative)) throw new Error(`Unsafe asset: ${reference}`);
  if (!/\.(?:css|js|jpe?g|png|gif|svg|webp|avif|ico|woff2?|ttf|eot|mp4)$/i.test(relative)) return;
  if (!copied.has(relative)) { copied.add(relative); assetQueue.push(relative); }
}
for (const tag of html.matchAll(/<(?:img|script|link|source)\b[^>]*>/gi)) {
  for (const attribute of tag[0].matchAll(/\b(?:src|href)="([^"]+)"/gi)) addAsset(attribute[1]);
}
while (assetQueue.length) {
  const relative = assetQueue.shift();
  const source = path.join(root, ...relative.split('/'));
  const destination = path.join(output, ...relative.split('/'));
  if (!(await stat(source)).isFile()) throw new Error(`Missing asset: ${relative}`);
  await mkdir(path.dirname(destination), { recursive: true });
  await copyFile(source, destination);
  if (relative.endsWith('.css')) {
    const css = await readFile(source, 'utf8');
    for (const match of css.matchAll(/url\(\s*["']?([^\s"')]+)["']?\s*\)/gi)) addAsset(match[1], relative);
  }
}
const ids = new Set([...html.matchAll(/\bid="([^"]+)"/g)].map(match => match[1]));
for (const match of html.matchAll(/\bhref="#([^"]+)"/g)) {
  if (!ids.has(match[1])) throw new Error(`Missing homepage section: ${match[1]}`);
}
if (/action="[^"#]*\.php/.test(html) || /href="(?!https?:)[^"#]*\.html/.test(html)) {
  throw new Error('The preview still references a server endpoint or another local page.');
}
await writeFile(path.join(output, 'index.html'), html, 'utf8');
console.log(`Homepage-only build ready: dist/index.html + ${copied.size} local assets.`);
