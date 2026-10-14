from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
from PIL import Image
import json, re

root=Path(__file__).resolve().parent
assignments=json.loads((root/'page-banner-map.json').read_text(encoding='utf-8'))
css=(root/'css/redesign.css').read_text(encoding='utf-8')
class Links(HTMLParser):
    def __init__(self): super().__init__(); self.refs=[]
    def handle_starttag(self,t,attrs):
        a=dict(attrs)
        for k in ('href','src','action'):
            if a.get(k): self.refs.append(a[k])
for item in assignments:
    text=(root/item['page']).read_text(encoding='utf-8')
    topic=Path(item['banner']).stem.removesuffix('-branded')
    assert f'data-banner="{topic}"' in text, item['page']
    assert f'.page-hero[data-banner="{topic}"]' in css, topic
    assert (root/item['banner']).is_file(), item['banner']
    parser=Links(); parser.feed(text)
    for ref in parser.refs:
        url=urlsplit(ref)
        if not url.scheme and not url.netloc and url.path:
            assert (root/unquote(url.path)).is_file(), (item['page'],ref)
for ref in re.findall(r'url\("([^\"]+)"\)',css):
    assert (root/'css'/unquote(ref)).is_file(), ref
themes=sorted({Path(i['banner']).stem.removesuffix('-branded') for i in assignments})
sizes=[]
for theme in themes:
    from set_page_banners import asset_for
    path=root/asset_for(theme)
    with Image.open(path) as image:
        image.verify()
    sizes.append(path.stat().st_size)
assert '.page-hero{padding:65px 0 70px;' in css
assert '.page-hero{padding:45px 0}' in css
assert len(assignments)==93
assert len(themes)==27
print(f'PASS: {len(assignments)} title pages, {len(themes)} related AI themes, all asset references resolve.')
print('PASS: Existing desktop/mobile banner padding retained.')
print(f'Optimized title JPEG sizes: {min(sizes)//1024}–{max(sizes)//1024} KB.')
