"""Format the original About Us copy without changing or shortening its text."""
from pathlib import Path
from html import escape
from html.parser import HTMLParser
import re

ROOT = Path(__file__).resolve().parent

class Text(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.parts=[]
        self.feed(source)
    def handle_data(self, value):
        self.parts.append(value)
    def handle_starttag(self, tag, attrs):
        if tag in {'br','p','h2','h3','section','article','div'}:
            self.parts.append(' ')
    def handle_endtag(self, tag):
        if tag in {'p','h2','h3','section','article','div'}:
            self.parts.append(' ')
    def value(self):
        return re.sub(r'\s+', ' ', ''.join(self.parts)).strip()

def original_content():
    source=(ROOT/'.redesign-backup/about-us.html').read_text(encoding='utf-8')
    body=source.split('<div class="about-content">',1)[1].split('<!-- about-content -->',1)[0]
    intro=Text(body.split('<div class="bullet">',1)[0]).value()
    items=[]
    for item in re.split(r'<li\b[^>]*>',body,flags=re.I)[1:]:
        item=item.split('</li>',1)[0].split('</ul>',1)[0]
        match=re.search(r'<strong>(.*?)</strong>(.*)',item,re.S)
        title=Text(match.group(1)).value()
        description=Text(match.group(2)).value()
        items.append((title,description))
    assert len(items)==16, f'Expected 16 original topics; found {len(items)}'
    return intro, items

def render():
    intro,items=original_content()
    # Split paragraphs only at existing sentence boundaries; preserve every word.
    paragraphs=re.split(r'(?=We DHLR Express, Packers and Movers are certified|Our years of experience)',intro)
    intro_markup=''.join('<p>'+escape(p.strip())+'</p>' for p in paragraphs)
    values=''.join(f'<article class="about-value"><span class="about-value-number">0{i+1} / OUR VALUES</span><h3>{escape(title)}</h3><p>{escape(copy)}</p></article>' for i,(title,copy) in enumerate(items[1:5]))
    operations=''.join(f'<article class="about-original-topic"><span class="about-topic-number">{i+1:02}</span><div><h3>{escape(title)}</h3><p>{escape(copy)}</p></div></article>' for i,(title,copy) in enumerate(items[5:14]))
    purpose=''.join(f'<div><span class="eyebrow">OUR PURPOSE</span><h2>{escape(title)}</h2><p>{escape(copy)}</p></div>' for title,copy in items[14:])
    result=f'''<div class="about-modern about-original-copy">
<section class="section about-intro" id="about-row"><div class="wrap">
<div class="section-index"><span>01 / ABOUT DHLR EXPRESS</span><span>RELOCATION &amp; LOGISTICS</span></div>
<div class="split"><div class="about-story"><span class="eyebrow">GET TO KNOW US</span><h2>DHLR Express <em>– About Us</em></h2>{intro_markup}</div>
<div class="about-portrait"><img src="img/redesign/about-team-branded.jpg" alt="DHLR Express relocation team" width="1536" height="1024" loading="lazy"><div class="about-photo-note"><span>DHLR EXPRESS</span><strong>Relocation.<br>With care.</strong></div></div></div></div></section>
<section class="section section-soft about-values"><div class="wrap"><div class="section-index"><span>02 / OUR VALUES</span><span>PASSION · HONESTY · CARING · QUALITY</span></div><div class="about-values-intro"><h2>{escape(items[0][0])}</h2><p>{escape(items[0][1])}</p></div><div class="about-value-grid">{values}</div></div></section>
<section class="section about-approach"><div class="wrap"><div class="section-heading"><div><span class="eyebrow">OUR APPROACH</span><h2>The details behind<br><em>every move.</em></h2></div></div><div class="about-original-topics">{operations}</div></div></section>
<section class="section about-purpose"><div class="wrap"><div class="section-index"><span>03 / OUR DIRECTION</span><span>VISION &amp; MISSION</span></div><div class="about-purpose-grid">{purpose}</div></div></section>
</div>'''
    visible=Text(result).value()
    for title,copy in items:
        assert copy in visible, f'Content missing: {title}'
    assert intro in visible, 'Introduction text has changed'
    (ROOT/'templates/about-content.html').write_text(result,encoding='utf-8')
    from apply_premium_design import premium_html
    page=ROOT/'about-us.html'
    page.write_text(premium_html(page.read_text(encoding='utf-8'),page.name),encoding='utf-8')
    print('Restored and verified the full original introduction and all 16 topics, word for word (whitespace normalized).')

if __name__=='__main__':
    render()
