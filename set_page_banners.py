"""Assign topic-specific AI title images without rebuilding page content."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent
TOPICS = {
    'about-us': 'about-team',
    'contact': 'contact-support',
    'warehousing-and-storage': 'warehouse-storage',
    'car-transportation': 'vehicle-transport',
    'office-relocation': 'office-moving',
    'corporate-relocation': 'corporate-relocation',
    'industrial-relocation': 'industrial-moving',
    'exhibition-and-fine-art-moving': 'fine-art-moving',
    'commercial-moving': 'commercial-moving',
    'container-service': 'container-transport',
    'supply-chain': 'supply-chain',
    'odc': 'oversized-transport',
    'international': 'international-moving',
    'packaging-services': 'professional-packing',
    'wooden-packaging': 'wooden-crates',
    'export-packaging': 'export-packing',
    'logistics': 'logistics-hero',
    'house-relocation': 'home-hero',
    'domastic': 'domestic-moving',
    'relocation': 'relocation-moving',
    'services': 'moving-services',
    'networks': 'nationwide-network',
    'thanks': 'move-delivered',
}
METROS = {'mumbai','delhi','noida','gurgaon','hyderabad','pune','ahmedabad','kolkata','thane','ghaziabad','faridabad'}
COASTAL = {'chennai','kochi','mangalore','visakhapatnam','thiruvananthapuram'}
RESIDENTIAL = {'agra','bhopal','bhubaneswar','chandigarh','coimbatore','haryana','indore','jaipur','jamshedpur','kanpur','lucknow','madurai','patna','punjab','ranchi','surat','tiruchirappalli','vadodara','vijayawada'}
POSITIONS = {'about-team':18,'contact-support':22,'office-moving':10,'corporate-relocation':15,'fine-art-moving':15,'wooden-crates':15,'export-packing':20,'warehouse-storage':45,'vehicle-transport':45,'industrial-moving':15,'professional-packing':42,'home-hero':42,'logistics-hero':48,'supply-chain':10,'move-delivered':0,'city-metro-moving':20,'city-bangalore-moving':20}
def asset_for(topic):
    branded=ROOT/'img/redesign'/f'{topic}-branded.jpg'
    return f'img/redesign/{topic}-branded.jpg' if branded.is_file() else f'img/redesign/{topic}.jpg'

def prefer_branded_references(text):
    for branded in (ROOT/'img/redesign').glob('*-branded.jpg'):
        topic=branded.stem.removesuffix('-branded')
        text=text.replace(f'img/redesign/{topic}.jpg',f'img/redesign/{topic}-branded.jpg')
    return text
def banner_for(stem):
    if stem in TOPICS: return TOPICS[stem]
    if stem.startswith('packers-and-movers-'):
        city = stem.removeprefix('packers-and-movers-')
        if city in METROS: return 'city-metro-moving'
        if city in COASTAL: return 'city-coastal-moving'
        if city in RESIDENTIAL: return 'city-residential-moving'
        return 'city-bangalore-moving'
    raise ValueError(f'Unmapped title banner: {stem}')

def apply():
    assignments=[]
    for page in sorted(ROOT.glob('*.html')):
        text=page.read_text(encoding='utf-8')
        if 'class="page-hero"' not in text: continue
        topic=banner_for(page.stem)
        path=ROOT/asset_for(topic)
        if not path.is_file(): raise FileNotFoundError(f'AI image not yet saved: {path}')
        text=re.sub(r'<section class="page-hero"(?: data-banner="[^"]+")?', f'<section class="page-hero" data-banner="{topic}"', text)
        text=prefer_branded_references(text)
        page.write_text(text,encoding='utf-8')
        assignments.append({'page':page.name,'banner':str(path.relative_to(ROOT)).replace('\\','/')})
    topics=sorted({banner_for(p.stem) for p in ROOT.glob('*.html') if p.stem!='index'})
    rules='\n/* Topic-specific AI title backgrounds. Banner dimensions remain unchanged. */\n'
    rules+='\n'.join(f'.page-hero[data-banner="{t}"]{{--page-banner:url("../{asset_for(t)}");--banner-y:{POSITIONS.get(t,36)}%;}}' for t in topics)
    rules+='\n.page-hero{background-image:linear-gradient(90deg,rgba(10,23,43,.86) 0%,rgba(10,23,43,.60) 43%,rgba(10,23,43,.18) 100%),var(--page-banner);background-position:center var(--banner-y,36%);}\n'
    rules+='@media(max-width:760px){.page-hero{background-image:linear-gradient(90deg,rgba(10,23,43,.89),rgba(10,23,43,.40)),var(--page-banner);background-position:62% center;}}\n'
    css=ROOT/'css/redesign.css'
    previous=css.read_text(encoding='utf-8')
    marker='/* Topic-specific AI title backgrounds.'
    if marker in previous: previous=previous.split(marker)[0]
    css.write_text(previous+rules,encoding='utf-8')
    home=ROOT/'index.html'
    home.write_text(prefer_branded_references(home.read_text(encoding='utf-8')),encoding='utf-8')
    (ROOT/'page-banner-map.json').write_text(json.dumps(assignments,indent=2),encoding='utf-8')
    print(f'Assigned {len(topics)} topic-specific AI images to {len(assignments)} title banners.')

if __name__=='__main__': apply()
