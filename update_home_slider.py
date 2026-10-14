from pathlib import Path
import re
from set_page_banners import asset_for

root=Path(__file__).resolve().parent
js=root/'js/redesign.js'
text=js.read_text(encoding='utf-8')
start=text.find('const slides=')
end=text.find("document.querySelectorAll('a[data-toggle",start)
if start>=0 and end>start:
    text=text[:start]+text[end:]
    js.write_text(text,encoding='utf-8')

page=root/'index.html'
html=page.read_text(encoding='utf-8')
pattern=r'(<img class="hero-photo"[^>]*src=")([^"]+)(")'
matches=list(re.finditer(pattern,html))
assert len(matches)==3
third=matches[2]
html=html[:third.start(2)]+asset_for('business-logistics-hero')+html[third.end(2):]
if 'js/hero-slider.js' not in html:
    html=html.replace('</head>','<script defer src="js/hero-slider.js"></script></head>')
page.write_text(html,encoding='utf-8')

generator=root/'redesign_site.py'
source=generator.read_text(encoding='utf-8')
source=source.replace("'business.','img/redesign/logistics-hero.jpg'", "'business.','img/redesign/business-logistics-hero.jpg'")
# Replace only the photo belonging to the third slide, preserving the first slide.
source=source.replace("'img/redesign/logistics-hero.jpg','Explore logistics'", "'img/redesign/business-logistics-hero.jpg','Explore logistics'")
if 'js/hero-slider.js' not in source:
    source=source.replace("    if p.name=='thanks.html': out=", "    if p.name=='index.html': out=out.replace('</head>', '<script defer src=\"js/hero-slider.js\"></script></head>')\n    if p.name=='thanks.html': out=")
generator.write_text(source,encoding='utf-8')
print('Home slider: three distinct photos; one autoplay controller at 5-second intervals.')
