"""Preserve complete service copy while applying the shared service layout."""
from pathlib import Path
from html import escape
import re

ROOT=Path(__file__).resolve().parent
SERVICE_PAGES={name+'.html' for name in (
    'services','relocation','house-relocation','office-relocation',
    'industrial-relocation','corporate-relocation','exhibition-and-fine-art-moving',
    'car-transportation','commercial-moving','container-service','supply-chain',
    'odc','logistics','packaging-services','wooden-packaging','export-packaging',
    'warehousing-and-storage','domastic','international'
)}

def format_service_html(s,page):
    if page not in SERVICE_PAGES:return s
    if 'js/about-motion.js' not in s:
        s=s.replace('</head>','<script defer src="js/about-motion.js"></script></head>')
    if page=='services.html':
        # Retain the existing directory cards and restore every original detailed section.
        if 'class="services-directory"' not in s:
            start=s.index('</section>',s.index('<section class="page-hero"'))+len('</section>')
            end=s.index('<section class="section quote-section"',start)
            directory=s[start:end]
            directory=directory.replace('<div class="wrap"><div class="cards">','<div class="wrap"><div class="section-heading"><div><span class="eyebrow">OUR MOVING SOLUTIONS</span><h2>Every moving need.<br><em>Carefully considered.</em></h2></div></div><div class="cards">',1)
            original=(ROOT/'.redesign-backup/services.html').read_text(encoding='utf-8')
            section=re.search(r'<section id="service-page">[\s\S]*?</section>',original).group()
            section=re.sub(r'\s+(?:data-toggle|role|aria-controls|data-tab-name)="[^"]*"','',section)
            section=section.replace('</ul>','<li><a href="#warehousing">warehousing</a></li></ul>',1)
            replacements={
                'img/service-2/vehichal.jpeg':'img/redesign/vehicle-transport-branded.jpg',
                'img/service-2/single-service-2.jpeg':'img/redesign/warehouse-storage-branded.jpg',
                'img/service-2/single-service-6.jpeg':'img/redesign/logistics-hero-branded.jpg',
                'img/service-2/single-service-4.jpeg':'img/redesign/supply-chain-branded.jpg',
                'img/service-2/single-service-5.jpeg':'img/redesign/warehouse-storage-branded.jpg',
            }
            for a,b in replacements.items():section=section.replace(a,b)
            names=['Car Transportation','Warehousing and Storage','Logistics','Supply Chain','Warehousing']
            for name in names:section=section.replace('alt="Awesome Image"',f'alt="{escape(name)}" loading="lazy"',1)
            # This sentence was bare text between paragraphs in the source; wrap it without rewriting.
            section=re.sub(r'(</p>\s*)(Customized and optimal solutions[\s\S]*?best suitable for you\.)(\s*<p>)',r'\1<p>\2</p>\3',section)
            content='<div class="services-directory">'+directory+'</div><div class="wrap legacy-content services-modern">'+section+'</div>'
            s=s[:start]+content+s[end:]
        s=s.replace('<h1>services</h1>','<h1>Our Services</h1>').replace('Home</a> / services','Home</a> / Our Services')
    else:
        s=s.replace('class="wrap legacy-content"','class="wrap legacy-content services-modern"',1)
    from service_images import apply_service_images
    return apply_service_images(s,page)

if __name__=='__main__':
    for name in sorted(SERVICE_PAGES):
        p=ROOT/name
        p.write_text(format_service_html(p.read_text(encoding='utf-8'),name),encoding='utf-8')
    print(f'Formatted {len(SERVICE_PAGES)} service pages without shortening their copy.')
