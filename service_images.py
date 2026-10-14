"""Use the existing high-resolution branded photographs for each service."""
from pathlib import Path
from html import escape
import re

ROOT=Path(__file__).resolve().parent
THEMES={
 'car-transportation':('vehicle-transport','Vehicle transportation on a DHLR Express car carrier',2027,776),
 'commercial-moving':('commercial-moving','DHLR Express commercial moving team',2172,724),
 'container-service':('container-transport','Container transport and freight handling',2117,743),
 'corporate-relocation':('corporate-relocation','DHLR Express corporate relocation team',2172,724),
 'domastic':('domestic-moving','DHLR Express domestic moving service',1961,802),
 'exhibition-and-fine-art-moving':('fine-art-moving','Careful packing and handling of fine art',2089,753),
 'export-packaging':('export-packing','Professional export packing and freight preparation',2172,724),
 'house-relocation':('home-hero','DHLR Express movers carefully packing a home',1671,941),
 'industrial-relocation':('industrial-moving','Specialist handling of industrial machinery',1983,793),
 'international':('international-moving','International relocation and export freight',2172,724),
 'logistics':('logistics-hero','DHLR Express logistics team loading a moving truck',1672,941),
 'odc':('oversized-transport','Specialist oversized cargo transportation',1983,793),
 'office-relocation':('office-moving','DHLR Express office furniture and equipment relocation',2172,724),
 'packaging-services':('professional-packing','Protective professional packing of fragile belongings',2172,724),
 'relocation':('relocation-moving','DHLR Express relocation and moving team',2048,768),
 'supply-chain':('supply-chain','Organised dispatch and supply chain handling',2172,724),
 'warehousing-and-storage':('warehouse-storage','Organised warehouse storage and forklift handling',2048,768),
 'wooden-packaging':('wooden-crates','Protective wooden crates for packing and transportation',2172,724),
}

def photo(theme):
    name,alt,width,height=theme
    return f'<img class="service-hd-image" src="img/redesign/{name}-branded.jpg" alt="{escape(alt,quote=True)}" width="{width}" height="{height}" loading="lazy" decoding="async">'

def apply_service_images(s,page):
    start=s.find('<div class="wrap legacy-content services-modern">')
    if start<0:return s
    end=s.index('<section class="section quote-section"',start)
    body=s[start:end]
    if page=='services.html':
        def upgrade(match):
            tag=match.group()
            for theme in THEMES.values():
                if f'/{theme[0]}-branded.jpg' in tag:return photo(theme)
            return tag
        body=re.sub(r'<img\b[^>]*>',upgrade,body)
    else:
        theme=THEMES[Path(page).stem]
        image=photo(theme)
        if page in {'packaging-services.html','wooden-packaging.html','export-packaging.html'}:
            if 'class="service-hd-image"' in body:
                body=re.sub(r'<img class="service-hd-image"[^>]*>',image,body,count=1)
            else:
                body=body.replace('<div class="image-box clearfix"></div>',f'<div class="image-box clearfix">{image}</div>',1)
        else:
            body=re.sub(r'<img\b[^>]*>',image,body,count=1)
    return s[:start]+body+s[end:]
