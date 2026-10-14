"""Apply the shared editorial skin and home composition without rebuilding content."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def premium_html(s, page):
    if 'css/premium.css' not in s:
        s = s.replace('<link rel="stylesheet" href="css/redesign.css">', '<link rel="stylesheet" href="css/redesign.css"><link rel="stylesheet" href="css/premium.css">')
    if '<div class="footer-signoff">' not in s:
        s = s.replace('<footer class="footer"><div class="wrap">', '<footer class="footer"><div class="wrap"><div class="footer-signoff">Your next chapter. <em>Delivered.</em></div>')
    s = s.replace('A fresh start.<br>A smoother move.', 'A fresh start.<br><em>Starts right here.</em>')
    if page == 'about-us.html':
        import re
        if 'js/about-motion.js' not in s:
            s=s.replace('</head>','<script defer src="js/about-motion.js"></script></head>')
        about=(ROOT/'templates'/'about-content.html').read_text(encoding='utf-8')
        s=re.sub(r'<div class="(?:wrap legacy-content|about-modern)"[\s\S]*?(?=<section class="section quote-section")',lambda m: about+'\n',s,count=1)
        s=s.replace('<h1>about us</h1>','<h1>About DHLR Express</h1>').replace('Home</a> / about us','Home</a> / About us')
        s=re.sub(r'<title>.*?</title>','<title>About DHLR Express | Thoughtful Moving &amp; Relocation</title>',s,count=1)
    if page != 'index.html':
        from format_service_pages import format_service_html
        from format_contact_page import format_contact_html
        from format_network_page import format_network_html
        return format_network_html(format_contact_html(format_service_html(s,page),page),page)
    replacements = {
        'MOVING YOU FORWARD':'A BETTER WAY TO MOVE',
        'Your next move.<br><em>Our responsibility.</em>':'Life moves.<br>We move<br><em>with you.</em>',
        'From your first box to your new beginning. Thoughtful packing, careful transport and a team that’s with you all the way.':'A new address. A bigger ambition. A fresh beginning. Wherever life takes you, we handle the move with care.',
        'New beginnings.<br><em>Handled with care.</em>':'New keys.<br>New stories.<br><em>Same care.</em>',
        'Big plans.<br><em>Seamless logistics.</em>':'Big ambitions.<br>Every detail<br><em>in motion.</em>',
        'Every move is different.<br>We make yours effortless.':'Different moves.<br><em>One thoughtful team.</em>',
        'We move belongings.<br>And peace of mind.':'Some things deserve<br><em>a little more care.</em>',
        'Four steps.<br>One smooth journey.':'From where you are.<br><em>To what comes next.</em>',
        'Closer to you.<br>Wherever you go.':'Rooted in care.<br><em>Connected across India.</em>',
    }
    for a,b in replacements.items():
        s=s.replace(a,b)
    # Additional details are static and independent of the accessible slide controls.
    if 'hero-image-caption' not in s:
        marker='<div class="wrap hero-controls">'
        s=s.replace(marker, '<div class="hero-image-caption"><span>DHLR EXPRESS / RELOCATION &amp; LOGISTICS</span><strong>Handled with care.<br>From here to anywhere.</strong></div>'+marker)
    # The same small assurance line belongs to each slide, including slide three.
    import re
    s=re.sub(r'(<div class="hero-actions">(?:(?!</div>).)*</div>)(?!<div class="hero-footnote">)',r'\1<div class="hero-footnote">Thoughtful packing. Personal support. Every step.</div>',s)
    note='<div class="hero-footnote">Thoughtful packing. Personal support. Every step.</div>'
    while note+note in s:
        s=s.replace(note+note,note)
    if 'moving-ribbon' not in s:
        items=''.join('<span>'+t+'</span><b aria-hidden="true">✳</b>' for t in ['A fresh start, beautifully handled','Home relocation','Business moves','Packing with purpose','Across India & beyond'])
        ribbon='<div class="moving-ribbon" aria-label="Home relocation, business moves and packing across India and beyond"><div class="ribbon-track" aria-hidden="true">'+items+items+'</div></div>'
        s=s.replace('<section class="section section-soft">',ribbon+'<section class="section section-soft">',1)
    if 'process-section' not in s:
        s=s.replace('<section class="section section-soft"><div class="wrap"><div class="section-heading"><div><span class="eyebrow">THE WAY WE MOVE', '<section class="section section-soft process-section"><div class="wrap"><div class="section-index"><span>02 / A WELL-PLANNED JOURNEY</span><span>THE DHLR WAY</span></div><div class="section-heading"><div><span class="eyebrow">THE WAY WE MOVE')
    if 'services-tail' not in s:
        s=s.replace('<div class="section-heading"><div><span class="eyebrow">WHAT WE DO', '<div class="section-index"><span>01 / SOLUTIONS THAT MOVE YOU</span><span>HOME · BUSINESS · BEYOND</span></div><div class="section-heading"><div><span class="eyebrow">WHAT WE DO',1)
        marker='</div></div></section><section class="section"><div class="wrap split">'
        s=s.replace(marker,'</div><div class="services-tail"><p>Around the corner or across the country. Let’s find your way forward.</p><a class="text-link" href="services.html">Discover all moving solutions ↗</a></div></div></section><section class="section"><div class="wrap split">',1)
    from polish_homepage import polish_home_html
    return polish_home_html(s)

if __name__ == '__main__':
    pages=list(ROOT.glob('*.html'))
    for p in pages:
        p.write_text(premium_html(p.read_text(encoding='utf-8'),p.name),encoding='utf-8')
    print(f'Applied premium design to {len(pages)} pages.')
