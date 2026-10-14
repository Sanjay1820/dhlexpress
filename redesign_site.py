from apply_premium_design import premium_html
from pathlib import Path
from html.parser import HTMLParser
from html import escape, unescape
import re, shutil, json
from set_page_banners import banner_for, prefer_branded_references

ROOT=Path(__file__).resolve().parent
BACKUP=ROOT/'.redesign-backup'
BACKUP.mkdir(exist_ok=True)
VOID={'img','br','hr','input','meta','link','source','wbr','area','embed','param','col','base'}
class Node:
    def __init__(self,tag='',attrs=()): self.tag=tag; self.attrs=dict(attrs); self.children=[]
    def text(self): return ''.join(c.text() if isinstance(c,Node) else c for c in self.children)
    def walk(self):
        yield self
        for c in self.children:
            if isinstance(c,Node): yield from c.walk()
    def html(self):
        if self.tag in {'script','style','iframe','grammarly-desktop-integration'}: return ''
        attrs={k:v for k,v in self.attrs.items() if k!='style' and not k.startswith('on')}
        if self.tag=='img':
            replacements={'img/service-2/finart.jpeg':'img/service-2/finart-min.jpeg','img/service-2/industrial.jpeg':'img/service-2/industrial-min.jpeg','img/service-2/odc.jpeg':'img/service-2/odc-min.jpeg','img/service-2/blr packing.jpg':'img/service-2/blr packing(1).jpg'}
            attrs['src']=replacements.get(attrs.get('src'),attrs.get('src',''))
            from urllib.parse import unquote
            if not (ROOT/unquote(attrs['src'])).is_file() and not attrs['src'].startswith('http'): return ''
            attrs['loading']='lazy'
            if attrs.get('alt','') in ('','Awesome Image'): attrs['alt']='DHLR Express relocation and logistics services'
        if self.tag=='a' and attrs.get('href','').startswith('tel:'):
            nums=re.findall(r'\d+',attrs['href']); number=''.join(nums).lstrip('0')
            attrs['href']='tel:+'+(number if number.startswith('91') else '91'+number)
        a=''.join(' '+k+'="'+escape(v or '',quote=True)+'"' for k,v in attrs.items())
        content=''.join(c.html() if isinstance(c,Node) else escape(c,quote=False) for c in self.children)
        if not self.tag: return content
        return '<'+self.tag+a+'>'+('' if self.tag in VOID else content+'</'+self.tag+'>')
class Parser(HTMLParser):
    def __init__(self,s):
        super().__init__(convert_charrefs=True); self.root=Node(); self.stack=[self.root]; self.feed(s)
    def handle_starttag(self,t,a):
        if t=='li' and self.stack[-1].tag=='li': self.stack.pop()
        if t in {'p','div','section','h1','h2','h3','ul'} and self.stack[-1].tag=='p': self.stack.pop()
        n=Node(t,a); self.stack[-1].children.append(n)
        if t not in VOID: self.stack.append(n)
    def handle_startendtag(self,t,a): self.handle_starttag(t,a); self.handle_endtag(t)
    def handle_endtag(self,t):
        for i in range(len(self.stack)-1,0,-1):
            if self.stack[i].tag==t: self.stack=self.stack[:i]; break
    def handle_data(self,s): self.stack[-1].children.append(s)

services=[
('Household relocation','Your next chapter, carefully packed. Complete door-to-door home moving.','house-relocation.html','img/resources/home-moving-services.jpg'),
('Office & corporate moving','Organised business relocations that keep your next move on schedule.','office-relocation.html','img/service-2/corporate-shifting.jpeg'),
('Vehicle transportation','Specialised carriers and careful handling for your car or two-wheeler.','car-transportation.html','img/service-2/vehichal.jpeg'),
('Packing solutions','Purposeful protection for fragile items, furniture and commercial goods.','packaging-services.html','img/service-2/blr packing(1).jpg'),
('Logistics & supply chain','Connected transport solutions, from dispatch to the final destination.','logistics.html','img/service-2/container.jpg'),
('Warehousing & storage','Flexible storage solutions for your home and business requirements.','warehousing-and-storage.html','img/service-2/single-service-2.jpeg')]
def cards():
    return '<div class="cards">'+''.join(f'<a class="service-card" href="{url}"><div class="card-image"><img src="{img}" alt="{name}" loading="lazy"></div><div class="card-body"><span class="card-number">0{i+1} / OUR SERVICES</span><h3>{name}</h3><p>{desc}</p><div class="card-link">Explore service <span>↗</span></div></div></a>' for i,(name,desc,url,img) in enumerate(services))+'</div>'
def header(page):
    links=[('Home','index.html'),('About us','about-us.html')]
    nav=''.join(f'<a href="{u}"'+(' class="active" aria-current="page"' if u==page else '')+f'>{n}</a>' for n,u in links)
    nav+='<details><summary>Our services</summary><div class="nav-dropdown">'+''.join(f'<a href="{u}">{n}</a>' for n,_,u,_ in services)+'<a href="international.html">International relocation</a><a href="services.html">All services</a></div></details>'
    nav+='<a href="networks.html">Our network</a><a href="contact.html">Contact</a>'
    return '<a class="skip-link" href="#main">Skip to content</a><div class="topline"><div class="wrap"><span>Care in every move. Since 1998.</span><span>Local · Across India · International</span><a href="tel:+918010005551">24/7 support: +91 80100 05551</a></div></div><header class="site-header"><div class="wrap header-inner"><a class="brand" href="index.html" aria-label="DHLR Express home"><img src="img/resources/transtar logo.jpg" alt="DHLR Express — Relocation & Logistics Solution" width="350" height="55"></a><nav class="site-nav" id="site-nav" aria-label="Main navigation">'+nav+'</nav><a class="btn header-cta" href="#quote">Get a free quote ↗</a><button class="menu-toggle" type="button" aria-label="Toggle menu" aria-controls="site-nav" aria-expanded="false">☰</button></div></header>'
def quote():
    return '''<section class="section quote-section" id="quote"><div class="wrap split"><div><span class="eyebrow">LET'S PLAN YOUR MOVE</span><h2>A fresh start.<br>A smoother move.</h2><p>Tell us where you’re headed. Our team will help you plan the packing, transport and delivery around your needs.</p><p>Prefer to talk? Call our moving team<br><a href="tel:+918010005551" style="color:white;font-size:24px;font-weight:bold">+91 80100 05551 ↗</a></p><p>Or write to <a href="mailto:info@dhlrexpress.com">info@dhlrexpress.com</a></p></div><form class="quote-form" action="contact-form-handler-side.php" method="post"><label>Your name<input name="name" autocomplete="name" placeholder="Full name" required maxlength="100"></label><label>Phone number<input type="tel" name="mobile" autocomplete="tel" placeholder="Your phone number" required minlength="10" maxlength="18" pattern="[+0-9 ()-]{10,18}"></label><label class="full">Email address<input type="email" name="email" autocomplete="email" placeholder="you@example.com" required maxlength="180"></label><label>Moving from<input name="movingfrom" placeholder="Current city / area" required maxlength="150"></label><label>Moving to<input name="movingto" placeholder="Destination city / area" required maxlength="150"></label><label class="full">Tell us about your move<textarea name="message" rows="3" placeholder="What are you moving? When would you like to move?" required maxlength="3000"></textarea></label><button class="btn full" type="submit">Request my free quote <span>↗</span></button><small class="full">By submitting, you agree that DHLR Express may contact you about your enquiry.</small></form></div></section>'''
def cities():
    names=['Bangalore','Mumbai','Delhi','Chennai','Hyderabad','Pune','Ahmedabad','Kolkata','Jaipur','Surat','Noida','Gurgaon']
    return '<section class="section"><div class="wrap"><span class="eyebrow">A NETWORK THAT MOVES WITH YOU</span><div class="section-heading"><h2>Closer to you.<br>Wherever you go.</h2><p>Explore our packing and moving services in cities across India.</p></div><div class="city-links">'+''.join(f'<a href="packers-and-movers-{n.lower()}.html">{n} ↗</a>' for n in names)+'</div><details style="margin-top:24px"><summary>Explore all locations</summary><div class="city-links">'+''.join(f'<a href="{escape(p.name)}">{escape(p.stem.replace("packers-and-movers-", "").replace("-"," ").title())}</a>' for p in sorted(ROOT.glob('packers-and-movers-*.html')))+'</div></details></div></section>'
def footer():
    return '''<footer class="footer"><div class="wrap"><div class="footer-grid"><div><a class="brand" href="index.html"><img class="footer-logo" src="img/resources/transtar logo.jpg" alt="DHLR Express"></a><p>Dynamic Home Logistics & Relocation Express. Thoughtful packing, moving and logistics for your next chapter.</p></div><div><h3>Explore</h3><a href="about-us.html">About DHLR Express</a><a href="services.html">Our services</a><a href="networks.html">Our network</a><a href="contact.html">Contact us</a></div><div><h3>Moving solutions</h3><a href="house-relocation.html">Home relocation</a><a href="office-relocation.html">Office relocation</a><a href="car-transportation.html">Vehicle transportation</a><a href="international.html">International moving</a><a href="warehousing-and-storage.html">Warehousing</a></div><div><h3>Let's talk</h3><a href="tel:+918010005551">+91 80100 05551</a><a href="tel:+918550055100">+91 85500 55100</a><a href="mailto:info@dhlrexpress.com">info@dhlrexpress.com</a><a href="https://www.facebook.com/dhlrelocationexpress/" target="_blank" rel="noopener noreferrer">Follow us on Facebook ↗</a><a href="https://www.payumoney.com/paybypayumoney/#/0BB9B09D6961AB5097BDBFBE5B0D1799">Pay online ↗</a></div></div><div class="footer-bottom"><span>© 2026 DHLR Express. All rights reserved.</span><span>Relocation & logistics, with care.</span></div></div></footer><div class="float-contact"><a href="#quote">Free quote ↗</a><a href="https://wa.me/918010005551" aria-label="Chat with DHLR Express on WhatsApp">WhatsApp ↗</a></div>'''
def home():
    slides=[('MOVING YOU FORWARD','Your next move.<br><em>Our responsibility.</em>','From your first box to your new beginning. Thoughtful packing, careful transport and a team that’s with you all the way.','img/redesign/logistics-hero.jpg','Plan your move','house-relocation.html'),('HOME, SWEET NEW HOME','New beginnings.<br><em>Handled with care.</em>','Move your home with a team that understands what matters. Personal attention, careful packing and door-to-door relocation.','img/redesign/home-hero.jpg','Explore home moving','house-relocation.html'),('BUSINESS WITHOUT BOUNDARIES','Big plans.<br><em>Seamless logistics.</em>','From office relocations to storage and supply chains, discover moving solutions built around your business.','img/redesign/business-logistics-hero.jpg','Explore logistics','logistics.html')]
    s='<section class="hero" aria-roledescription="carousel" aria-label="Our moving solutions">'
    for i,(tag,title,desc,img,cta,url) in enumerate(slides):
        heading='h1' if i==0 else 'h2'
        s+=f'<div class="hero-slide {"active" if i==0 else ""}" role="group" aria-roledescription="slide" aria-label="{i+1} of 3"><img class="hero-photo" src="{img}" alt="Professional DHLR Express moving and logistics"'+(' fetchpriority="high"' if i==0 else ' loading="lazy"')+f'><div class="wrap"><div class="hero-copy"><span class="eyebrow">{tag}</span><{heading}>{title}</{heading}><p>{desc}</p><div class="hero-actions"><a class="btn" href="#quote">Get a free quote ↗</a><a class="btn btn-outline" href="{url}">{cta} ↗</a></div></div></div></div>'
    s+='<div class="wrap hero-controls"><div style="display:flex;align-items:center"><div class="dots">'+''.join(f'<button class="dot" type="button" aria-label="Show slide {i+1}" aria-current="{str(i==0).lower()}"></button>' for i in range(3))+'</div><span class="slide-label">01 / 03</span></div><div class="arrows"><button type="button" data-slider-prev aria-label="Previous slide">←</button><button type="button" data-slider-pause aria-label="Pause slideshow">Ⅱ</button><button type="button" data-slider-next aria-label="Next slide">→</button></div></div></section>'
    s+='<div class="trustbar"><div class="wrap trust-grid">'+''.join(f'<div><span class="trust-icon">{icon}</span><div><strong>{t}</strong><small>{d}</small></div></div>' for icon,t,d in [('↗','Since 1998','Experience that matters'),('◇','Careful handling','Protection at every step'),('◎','Pan-India network','Local to long-distance'),('◷','24/7 assistance','A team you can reach')])+'</div></div>'
    s+='<section class="section section-soft"><div class="wrap"><div class="section-heading"><div><span class="eyebrow">WHAT WE DO</span><h2>Every move is different.<br>We make yours effortless.</h2></div><p>One trusted team for your home, business and everything in between. Discover a solution that fits your move.</p></div>'+cards()+'</div></section>'
    s+='''<section class="section"><div class="wrap split"><div class="image-composition"><img src="img/redesign/home-hero.jpg" alt="Professional movers carefully packing a home" loading="lazy"><div class="experience"><strong>Since 1998</strong><span>BUILT ON EXPERIENCE. MOVING WITH CARE.</span></div></div><div><span class="eyebrow">MORE THAN A MOVING COMPANY</span><h2>We move belongings.<br>And peace of mind.</h2><p>Your move is personal. So is our approach. At DHLR Express, we bring careful planning, professional packing and dedicated support to every relocation.</p><ul class="checklist"><li>Moving plans tailored to your requirements</li><li>Professional packing and careful handling</li><li>Home, office and commercial relocation</li><li>Dedicated and shared transport options</li></ul><a class="btn" href="about-us.html">Get to know us ↗</a></div></div></section><section class="section section-soft"><div class="wrap"><div class="section-heading"><div><span class="eyebrow">THE WAY WE MOVE</span><h2>Four steps.<br>One smooth journey.</h2></div><p>Clear communication from the first conversation to the final delivery.</p></div><div class="steps">'''
    s+=''.join(f'<div class="step"><span class="step-num">0{i+1}</span><h3>{t}</h3><p>{d}</p></div>' for i,(t,d) in enumerate([('Tell us your plans','Share your destination, schedule and requirements. We help you plan the details.'),('We pack with care','Our team prepares and protects your belongings for the journey ahead.'),('On the move','Coordinated transport and helpful communication throughout your relocation.'),('Welcome to your next','Careful delivery to your destination, so you can settle into your next chapter.')]))
    return s+'</div></div></section>'+quote()+cities()

def content(raw):
    # Parse only the original main region so invalid legacy navigation cannot swallow it.
    region=re.split(r'</header\s*>',raw,flags=re.I)[-1]
    region=re.split(r'<section\s+class=["\']reviews|<footer\b|<div\s+id=["\']slider2',region,flags=re.I)[0]
    tree=Parser(region).root
    candidates=[n for n in tree.walk() if n.attrs.get('id') in {'service-page','contact-page','about-row','our-mission','featured-service','contact-content','network','networks'}]
    if candidates: return ''.join(n.html() for n in candidates)
    # Preserve other page-specific blocks while discarding obsolete banners and breadcrumbs.
    for n in tree.walk():
        n.children=[c for c in n.children if not (isinstance(c,Node) and (c.attrs.get('id')=='breadcrumb-area' or 'color:#ffed4e' in c.attrs.get('style','').replace(' ','') or c.tag=='script'))]
    return tree.html()

report=[]
for p in sorted(ROOT.glob('*.html')):
    if not (BACKUP/p.name).exists(): shutil.copy2(p,BACKUP/p.name)
    raw=(BACKUP/p.name).read_text(encoding='utf-8',errors='replace')
    title=re.search(r'<title>(.*?)</title>',raw,re.S|re.I)
    title=title.group(1).strip() if title else 'DHLR Express — Relocation & Logistics'
    desc=re.search(r'<meta\s+name="description"\s+content="([^"]*)"',raw,re.I)
    desc=desc.group(1) if desc else 'Professional packing, moving, relocation and logistics solutions from DHLR Express.'
    heads=re.findall(r'<h1[^>]*>(.*?)</h1>',raw,re.S|re.I)
    label=unescape(re.sub('<[^>]+>','',heads[0])).strip() if heads else p.stem.replace('-',' ').title()
    if p.name=='index.html': main=home()
    else:
        if p.name=='services.html': details='<section class="section"><div class="wrap">'+cards()+'</div></section>'
        elif p.name=='thanks.html':
            label='Thank you for your enquiry'; details='<section class="section"><div class="wrap"><h2>Your enquiry has been submitted.</h2><p>Our team will contact you to discuss your move. For immediate assistance, call <a href="tel:+918010005551">+91 80100 05551</a>.</p><a class="btn" href="index.html">Back to home ↗</a></div></section>'
        else: details='<div class="wrap legacy-content">'+content(raw)+'</div>'
        main=f'<section class="page-hero" data-banner="{banner_for(p.stem)}"><div class="wrap"><div class="breadcrumb"><a href="index.html">Home</a> / {escape(label)}</div><span class="eyebrow">DHLR EXPRESS · MOVING WITH CARE</span><h1>{escape(label)}</h1></div></section>'+details
        if p.name!='thanks.html': main+=quote()
        if p.name=='networks.html': main+=cities()
    out=f'<!DOCTYPE html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{escape(unescape(title))}</title><meta name="description" content="{escape(desc,quote=True)}"><meta name="theme-color" content="#111f3a"><link rel="stylesheet" href="css/redesign.css"><script defer src="js/redesign.js"></script></head><body>'+header(p.name)+'<main id="main">'+main+'</main>'+footer()+'</body></html>'
    if p.name=='index.html': out=out.replace('</head>', '<script defer src="js/hero-slider.js"></script></head>')
    if p.name=='thanks.html': out=out.replace('href="#quote"','href="index.html#quote"')
    p.write_text(premium_html(prefer_branded_references(out),p.name),encoding='utf-8'); report.append({'page':p.name,'content_length':len(main)})
(ROOT/'redesign-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(f'Redesigned {len(report)} pages. Original HTML saved in .redesign-backup/.')
