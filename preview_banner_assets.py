"""Create compact image-only crop previews for banner asset inspection."""
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
import json, math
from set_page_banners import POSITIONS, asset_for

root=Path(__file__).resolve().parent
items=json.loads((root/'banner-generation.json').read_text(encoding='utf-8'))
width=600; height=113; padding=16; label=26
for batch in range(math.ceil(len(items)/12)):
    group=items[batch*12:(batch+1)*12]
    sheet=Image.new('RGB',(2*(width+padding)+padding,math.ceil(len(group)/2)*(height+label+padding)+padding),'#f3f4f6')
    draw=ImageDraw.Draw(sheet)
    for i,item in enumerate(group):
        x=padding+(i%2)*(width+padding); y=padding+(i//2)*(height+label+padding)
        image=Image.open(root/asset_for(item['topic'])).convert('RGB')
        image=ImageOps.fit(image,(width,height),centering=(.5,POSITIONS.get(item['topic'],36)/100))
        sheet.paste(image,(x,y+label)); draw.text((x,y+4),item['topic'],fill='#111f3a')
    out=root/'img/redesign'/f'banner-preview-{batch+1}.jpg'
    sheet.save(out,quality=90)
    print(str(out))
