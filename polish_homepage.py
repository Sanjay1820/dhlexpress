"""Apply the final homepage presentation details without replacing its content."""
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parent

def polish_home_html(s):
    s=s.replace('<body>','<body class="home-premium">',1)
    s=s.replace('<section class="section section-soft">','<section class="section section-soft home-services" id="home-services">',1)
    if 'class="hero-scroll"' not in s:
        s=s.replace('<div class="wrap hero-controls">','<a class="hero-scroll" href="#home-services"><span>EXPLORE THE WAY WE MOVE</span><b aria-hidden="true">↓</b></a><div class="wrap hero-controls">',1)
    if 'home-roadmap' not in s:
        pattern=r'<section class="section section-soft process-section">([\s\S]*?)</section>'
        def roadmap(match):
            body=match.group(1)
            heading=re.search(r'<h2>([\s\S]*?)</h2>',body).group(1)
            intro=re.search(r'<p>([\s\S]*?)</p>',body).group(1)
            steps=re.findall(r'<div class="step"><span class="step-num">(.*?)</span><h3>(.*?)</h3><p>(.*?)</p></div>',body,re.S)
            assert len(steps)==4,'Expected all four original moving steps'
            labels=['PLAN YOUR MOVE','PACK &amp; PROTECT','TRANSPORT &amp; COORDINATE','DELIVER &amp; SETTLE']
            timeline=''.join(f'<li class="step roadmap-step"><span class="roadmap-number" aria-hidden="true">{number}</span><div class="roadmap-step-copy"><span class="roadmap-stage">{label}</span><h3>{title}</h3><p>{copy}</p></div></li>' for (number,title,copy),label in zip(steps,labels))
            return '<section class="section section-soft process-section home-roadmap" id="moving-roadmap"><div class="wrap"><div class="roadmap-layout"><div class="roadmap-intro"><span class="eyebrow">A CLEAR WAY FORWARD</span><h2>'+heading+'</h2><p>'+intro+'</p><a class="btn roadmap-cta" href="#quote">Plan your next move ↗</a><span class="roadmap-note">THE DHLR WAY<br>Home, office and commercial relocation.</span></div><ol class="roadmap-list" aria-label="Your moving journey in four steps">'+timeline+'</ol></div></div></section>'
        s=re.sub(pattern,roadmap,s,count=1)
    from restore_home_sections import restore_home_sections
    from restore_home_welcome import restore_home_welcome
    return restore_home_welcome(restore_home_sections(s))

if __name__=='__main__':
    p=ROOT/'index.html'
    p.write_text(polish_home_html(p.read_text(encoding='utf-8')),encoding='utf-8')
    print('Homepage presentation polished; all existing content retained.')
