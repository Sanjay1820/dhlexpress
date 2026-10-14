from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json, urllib.request

root=Path(__file__).resolve().parent
class Audit(HTMLParser):
    def __init__(self): super().__init__(); self.refs=[]; self.ids=[]; self.headings=0; self.forms=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get('id'): self.ids.append(a['id'])
        if tag=='h1': self.headings+=1
        if tag=='form': self.forms.append(a)
        for k in ('src','href','action'):
            if a.get(k): self.refs.append(a[k])
issues=[]
for p in root.glob('*.html'):
    parser=Audit(); parser.feed(p.read_text(encoding='utf-8'))
    for ref in parser.refs:
        url=urlsplit(ref)
        if url.scheme or url.netloc: continue
        if url.path and not (root/unquote(url.path)).is_file(): issues.append((p.name,'missing asset/link',ref))
        if not url.path and url.fragment and url.fragment not in parser.ids: issues.append((p.name,'missing anchor',ref))
    duplicate={x for x in parser.ids if parser.ids.count(x)>1}
    if duplicate: issues.append((p.name,'duplicate IDs',sorted(duplicate)))
    if not parser.headings: issues.append((p.name,'missing h1',''))
    for form in parser.forms:
        if form.get('action')!='contact-form-handler-side.php': issues.append((p.name,'unexpected form target',form))
for path in ('/','/css/redesign.css','/js/redesign.js','/img/redesign/home-hero.jpg','/img/redesign/logistics-hero.jpg','/contact.html','/house-relocation.html'):
    try:
        with urllib.request.urlopen('http://127.0.0.1:8080'+path) as response:
            print(f'HTTP {response.status} {path}')
    except Exception as e: issues.append(('HTTP',path,str(e)))
print('Audit issues:',json.dumps(issues,indent=2))
print('Pages audited:',len(list(root.glob('*.html'))))
raise SystemExit(bool(issues))
