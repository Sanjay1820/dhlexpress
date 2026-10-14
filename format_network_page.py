"""Present all existing network locations without dropping any destination."""
from pathlib import Path
from html import escape
import re

ROOT=Path(__file__).resolve().parent

def network_content():
    featured=[('Bangalore','city-bangalore-moving'),('Mumbai','city-coastal-moving'),('Delhi','city-metro-moving'),('Chennai','city-coastal-moving'),('Hyderabad','city-residential-moving'),('Pune','city-metro-moving')]
    cards=''.join(f'<a class="network-city-card" href="packers-and-movers-{city.lower()}.html"><img src="img/redesign/{theme}-branded.jpg" alt="Professional packing and moving services" loading="lazy" decoding="async"><div><span>PACKING &amp; RELOCATION</span><h3>{city}</h3><b aria-hidden="true">↗</b></div></a>' for city,theme in featured)
    locations=sorted(ROOT.glob('packers-and-movers-*.html'))
    links=''.join(f'<a class="network-location" href="{escape(p.name,quote=True)}"><span>{escape(p.stem.replace("packers-and-movers-","").replace("-"," ").title())}</span><b aria-hidden="true">↗</b></a>' for p in locations)
    return '''<div class="network-modern">
<section class="section network-intro" id="about-row"><div class="wrap"><div class="section-index"><span>01 / OUR NETWORK</span><span>LOCAL · ACROSS INDIA · INTERNATIONAL</span></div><div class="split"><div><span class="eyebrow">A NETWORK THAT MOVES WITH YOU</span><h2>Connected across India.<br><em>Moving with you.</em></h2><p class="network-statement">Strategic Solutions To All Your Packing, Relocation &amp; Logistics Needs.</p><p>Explore our packing and moving services in cities across India.</p><div class="network-help"><span>Helpline 24x7<br>Domestic &amp; International</span><div><a href="tel:+918050605542">080 5060 5542 ↗</a><a href="tel:+918010005551">080 1000 5551 ↗</a></div></div><a class="btn" href="#locations">Find your location ↗</a></div><div class="network-visual"><img src="img/redesign/nationwide-network-branded.jpg" width="2048" height="768" alt="DHLR Express nationwide transport and dispatch network" loading="lazy" decoding="async"><div class="network-photo-note"><span>FROM YOUR DOOR TO YOUR DESTINATION</span><strong>One journey.<br>Thoughtfully connected.</strong></div></div></div></div></section>
<section class="section section-soft network-featured"><div class="wrap"><div class="section-heading"><div><span class="eyebrow">EXPLORE YOUR NEXT MOVE</span><h2>Different cities.<br><em>The same care.</em></h2></div><a class="text-link" href="#locations">View all locations ↗</a></div><div class="network-city-grid">'''+cards+'''</div></div></section>
<section class="section network-directory" id="locations"><div class="wrap"><div class="section-index"><span>02 / EXPLORE ALL LOCATIONS</span><span>FIND YOUR WAY FORWARD</span></div><div class="section-heading"><div><span class="eyebrow">OUR MOVING LOCATIONS</span><h2>Closer to you.<br><em>Wherever you go.</em></h2></div><p>Explore our packing and moving services in cities across India.</p></div><div class="network-search-row"><div class="network-search"><label for="network-search">Find your location</label><div><input id="network-search" type="search" placeholder="Search a city or area…" autocomplete="off" aria-controls="network-location-list"><button type="button" id="network-search-clear" hidden>Clear</button></div></div><p class="network-results" role="status" aria-live="polite">'''+str(len(locations))+''' locations</p></div><h3 class="network-directory-label">Explore all locations</h3><div class="network-location-grid" id="network-location-list">'''+links+'''</div><p class="network-no-results" hidden>No matching locations. Try a different city or area, or <a href="contact.html">contact our team</a> to discuss your move.</p><div class="network-directory-footer"><span>Need help planning your route?</span><a class="text-link" href="#quote">Let’s talk about your move ↗</a></div></div></section></div>'''

def format_network_html(s,page):
    if page!='networks.html':return s
    # Retain the existing enquiry form in full; move the location directory ahead of it.
    quote=re.search(r'<section class="section quote-section"[\s\S]*?</form></div></section>',s)
    assert quote,'Existing network quote form not found'
    hero_end=s.index('</section>',s.index('<section class="page-hero"'))+len('</section>')
    main_end=s.index('</main>',hero_end)
    s=s[:hero_end]+network_content()+quote.group()+s[main_end:]
    s=s.replace('<h1>Networks</h1>','<h1>Our Network</h1>').replace('Home</a> / Networks','Home</a> / Our Network')
    s=re.sub(r'<title>[\s\S]*?</title>','<title>Our Network | DHLR Express Moving Locations</title>',s,count=1)
    if 'js/about-motion.js' not in s:s=s.replace('</head>','<script defer src="js/about-motion.js"></script></head>')
    if 'js/network.js' not in s:s=s.replace('</head>','<script defer src="js/network.js"></script></head>')
    return s

if __name__=='__main__':
    p=ROOT/'networks.html'
    p.write_text(format_network_html(p.read_text(encoding='utf-8'),p.name),encoding='utf-8')
    print('Network formatted with every existing city and area, plus the original enquiry form.')
