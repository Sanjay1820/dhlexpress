"""Restore the full original welcome and service-quality copy below the slider."""
from pathlib import Path
from html import escape
import re
from restore_about_content import Text

ROOT=Path(__file__).resolve().parent

def original_welcome():
    raw=(ROOT/'.redesign-backup/index.html').read_text(encoding='utf-8')
    welcome=re.search(r'<h1>Welcome To DHLR Express</h1>[\s\S]*?<div class="about-content">([\s\S]*?)</div>',raw,re.I)
    quality=re.search(r'<h1>(Our Quality[\s\S]*?)</h1>[\s\S]*?<div class="about-content">([\s\S]*?)</div>',raw,re.I)
    assert welcome and quality,'Both original introduction blocks must be available'
    return Text(welcome.group(1)).value(),Text(quality.group(1)).value(),Text(quality.group(2)).value()

def welcome_html():
    intro,heading,quality=original_welcome()
    parts=re.split(r'(?=By using the best grade|We strategize our operations|We DHLR Express are known)',intro)
    paragraphs=''.join('<p>'+escape(p.strip())+'</p>' for p in parts)
    title=escape(heading).replace('Make Your Relocation','<br>Make Your Relocation').replace('Hassle-free !','<em>Hassle-free !</em>')
    return '''<section class="section home-welcome" id="welcome"><div class="wrap"><div class="home-welcome-banner"><span class="home-welcome-dot" aria-hidden="true"></span><span>Reliable Relocation Services Since 1998</span><a href="about-us.html">GET TO KNOW DHLR EXPRESS ↗</a></div><div class="home-welcome-layout"><div class="home-welcome-heading"><span class="eyebrow">MOVING WITH EXPERIENCE. HANDLING WITH CARE.</span><h2>Welcome To<br><em>DHLR Express</em></h2><span class="home-welcome-rule" aria-hidden="true"></span><a class="text-link" href="services.html">Explore our moving services ↗</a></div><div class="home-welcome-copy">'''+paragraphs+'''</div></div><div class="home-quality-panel"><div><span class="eyebrow">OUR COMMITMENT TO YOUR MOVE</span><h2>'''+title+'''</h2></div><div class="home-quality-copy"><p>'''+escape(quality)+'''</p></div></div></div></section>'''

def restore_home_welcome(s):
    if 'class="section home-welcome"' not in s:
        assert '<div class="moving-ribbon"' in s
        s=s.replace('<div class="moving-ribbon"',welcome_html()+'<div class="moving-ribbon"',1)
    if 'js/about-motion.js' not in s:
        s=s.replace('</head>','<script defer src="js/about-motion.js"></script></head>')
    return s

if __name__=='__main__':
    p=ROOT/'index.html'
    p.write_text(restore_home_welcome(p.read_text(encoding='utf-8')),encoding='utf-8')
    print('Restored complete original Welcome and Quality content below the homepage slider/trust strip.')
