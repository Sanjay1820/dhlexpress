"""Format the Contact page while retaining all six offices and enquiry fields."""
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parent
TEMPLATE=ROOT/'templates/contact-content.html'

def build_template(source):
    offices=re.findall(r'<div class="well text-center">([\s\S]*?)</div>',source)
    assert len(offices)==6,'Expected all six original contact offices'
    emails=['info@dhlrexpress.com','contact@dhlrexpress.com','quiry@dhlrexpress.com']
    email_links=', '.join(f'<a href="mailto:{e}">{e}</a>' for e in emails)
    cards=[]
    for i,(city,body) in enumerate(zip(['Mumbai','Pune','Kolkata','New Delhi','Gurugram','Bangalore'],offices)):
        heading=re.search(r'<h4>([\s\S]*?)</h4>',body).group(1)
        body=re.sub(r'<h4>[\s\S]*?</h4>','',body,count=1).strip()
        body=re.sub(r'<a href="mailto:[^"]*">[\s\S]*?</a>',email_links,body)
        cards.append(f'<article class="contact-office"><div class="contact-office-top"><span class="contact-office-city">{city}</span><span class="contact-office-number">0{i+1} / OFFICE</span></div><h3>{heading}</h3><div class="contact-office-body">{body}</div></article>')
    result='''<div class="contact-modern">
<section class="section contact-intro" id="contact-page"><div class="wrap"><div class="section-index"><span>01 / LET’S TALK ABOUT YOUR MOVE</span><span>DHLR EXPRESS</span></div><div class="split"><div><span class="eyebrow">A CONVERSATION IS A GOOD START</span><h2>Get in touch<br><em>with us.</em></h2><p class="contact-lead">A new home, a new office or a journey across cities. Tell us what you have in mind, and let’s plan the details together.</p><div class="contact-channels">
<div class="contact-channel"><span>Phone. No.:</span><a href="tel:+918010005551">+91 - 80 1000 5551 <b aria-hidden="true">↗</b></a></div>
<div class="contact-channel"><span>Helpline No.:</span><a href="tel:+918550055100">+91 - 85 5005 5100 <b aria-hidden="true">↗</b></a></div>
<div class="contact-channel contact-channel-wide"><span>E-mail :</span><div class="contact-email-links">'''+email_links+'''</div></div>
<div class="contact-channel contact-channel-wide"><span>Website :</span><a class="contact-website" href="https://dhlrexpress.com">https://dhlrexpress.com <b aria-hidden="true">↗</b></a></div></div><a class="btn" href="#quote">Send a moving enquiry ↗</a></div><div class="contact-visual"><img src="img/redesign/contact-support.jpg" width="2048" height="768" alt="Customer support team ready to discuss your relocation" loading="lazy" decoding="async"><div class="contact-visual-note"><span>PERSONAL SUPPORT</span><strong>Every good move<br>starts with a hello.</strong><a href="https://wa.me/918010005551">Chat on WhatsApp ↗</a></div></div></div></div></section>
<section class="section section-soft contact-offices"><div class="wrap"><div class="section-index"><span>02 / FIND YOUR NEAREST TEAM</span><span>OUR OFFICE NETWORK</span></div><div class="section-heading"><div><span class="eyebrow">LOCAL CONNECTIONS. PERSONAL ATTENTION.</span><h2>Our Zone Wise<br><em>Main Head Offices :</em></h2></div><p>Reach the team closest to your move. Explore our office addresses and contact details below.</p></div><div class="contact-office-grid">'''+''.join(cards)+'''</div></div></section></div>'''
    TEMPLATE.write_text(result,encoding='utf-8')

def format_contact_html(s,page):
    if page!='contact.html':return s
    if not TEMPLATE.exists():build_template(s)
    s=re.sub(r'<div class="(?:wrap legacy-content|contact-modern)">[\s\S]*?(?=<section class="section quote-section)',lambda m:TEMPLATE.read_text(encoding='utf-8'),s,count=1)
    s=s.replace('<h1>contact</h1>','<h1>Contact Us</h1>').replace('Home</a> / contact','Home</a> / Contact Us')
    s=re.sub(r'<title>[\s\S]*?</title>','<title>Contact DHLR Express | Moving Enquiries &amp; Office Locations</title>',s,count=1)
    s=s.replace('class="section quote-section"','class="section quote-section contact-enquiry"')
    if 'js/about-motion.js' not in s:s=s.replace('</head>','<script defer src="js/about-motion.js"></script></head>')
    return s

if __name__=='__main__':
    p=ROOT/'contact.html'
    p.write_text(format_contact_html(p.read_text(encoding='utf-8'),p.name),encoding='utf-8')
    print('Contact page formatted; all six original offices and enquiry fields retained.')
