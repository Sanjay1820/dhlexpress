"""Restore complete customer reviews, original client logos and helpline content."""
from pathlib import Path
from html import escape,unescape
import re

ROOT=Path(__file__).resolve().parent

def original_sections():
    raw=(ROOT/'.redesign-backup/index.html').read_text(encoding='utf-8')
    reviews=re.search(r'<section class="reviews">([\s\S]*?)</section>',raw).group(1)
    pattern=r'<h4 class="title">(.*?)</h4>[\s\S]*?<h6 class="sub-title">(.*?)</h6>[\s\S]*?background-image: url\(\x27(.*?)\x27\)[\s\S]*?<p>(.*?)</p>'
    items=re.findall(pattern,reviews,re.S)
    logos=re.findall(r'<img[^>]*src="([^"]+)"',re.search(r'<section id="clients">([\s\S]*?)</section>',raw).group(1))
    assert len(items)==6 and len(logos)==15
    return items,logos

def sections_html():
    reviews,logos=original_sections()
    cards=''.join(f'<article class="home-review-card"><div class="review-person"><div><h3>{name}</h3><span>{job}</span></div><img src="{escape(photo,quote=True)}" alt="Original review image for {escape(unescape(name),quote=True)}" width="64" height="64" loading="lazy"></div><span class="review-quote-mark" aria-hidden="true">“</span><blockquote><p>{copy}</p></blockquote></article>' for name,job,photo,copy in reviews)
    logo_cards=''.join(f'<div class="home-client-logo"><img src="{escape(src,quote=True)}" alt="Original client logo {i+1}" loading="lazy" decoding="async"></div>' for i,src in enumerate(logos))
    return '''<div class="home-restored-sections">
<section class="section home-reviews" id="customer-reviews" data-content-carousel><div class="wrap"><div class="section-index"><span>OUR VALUABLE CUSTOMERS REVIEWS</span><span>IN THEIR OWN WORDS</span></div><div class="section-heading"><div><span class="eyebrow">THE PEOPLE BEHIND THE MOVES</span><h2>Real moves.<br><em>Personal experiences.</em></h2></div><div class="content-carousel-controls"><button type="button" data-carousel-prev aria-label="Previous customer review" aria-controls="home-review-track">←</button><span data-carousel-status role="status" aria-live="polite">6 customer reviews</span><button type="button" data-carousel-next aria-label="Next customer review" aria-controls="home-review-track">→</button></div></div><div class="home-review-track content-carousel-track" id="home-review-track" data-carousel-track tabindex="0" role="region" aria-label="Customer reviews">'''+cards+'''</div></div></section>
<section class="section home-clients" id="clients" data-content-carousel><div class="wrap"><div class="section-heading"><div><span class="eyebrow">DHLR EXPRESS SINCE 1998</span><h2>The names in<br><em>our journey.</em></h2></div><div class="content-carousel-controls"><button type="button" data-carousel-prev aria-label="Previous client logos" aria-controls="home-client-track">←</button><span data-carousel-status role="status" aria-live="polite">15 client logos</span><button type="button" data-carousel-next aria-label="Next client logos" aria-controls="home-client-track">→</button></div></div><div class="home-client-track content-carousel-track" id="home-client-track" data-carousel-track tabindex="0" role="region" aria-label="Original client logos">'''+logo_cards+'''</div></div></section>
<section class="section home-helpline" id="btm-call"><div class="wrap home-helpline-inner"><div class="home-helpline-copy"><span class="eyebrow">AFFORDABLE &amp; PROFESSIONAL SERVICES</span><h2>Strategic Solutions To All Your<br><em>Relocation &amp; Logistics Needs.</em></h2><p>Helpline 24x7<br>Domestic &amp; International</p><div class="home-helpline-numbers"><a href="tel:+918010005551">080 1000 5551 ↗</a><a href="tel:+918550055100">085 5005 5100 ↗</a></div><a class="btn" href="#quote">Plan your move with us ↗</a></div><div class="home-helpline-visual"><img src="img/resources/mover-man-4.png" alt="DHLR Express moving team representative" loading="lazy"></div></div></section>
</div>'''

def restore_home_sections(s):
    if 'home-restored-sections' not in s:
        s=s.replace('<section class="section quote-section"',sections_html()+'<section class="section quote-section"',1)
    if 'js/home-carousels.js' not in s:
        s=s.replace('</head>','<script defer src="js/home-carousels.js"></script></head>')
    if 'data-carousel-pause' not in s:
        s=s.replace('<button type="button" data-carousel-next', '<button type="button" data-carousel-pause aria-label="Pause automatic sliding" aria-pressed="false">Ⅱ</button><button type="button" data-carousel-next')
    return s

if __name__=='__main__':
    p=ROOT/'index.html'
    p.write_text(restore_home_sections(p.read_text(encoding='utf-8')),encoding='utf-8')
    print('Restored all 6 complete reviews, 15 original logos and the original helpline section.')
