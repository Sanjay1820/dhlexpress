"""Contact sheets of branded image assets for visual review."""
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
import json, math

root=Path(__file__).resolve().parent
items=json.loads((root/'branded-image-generation.json').read_text(encoding='utf-8'))
width=800; height=300; padding=16; label=25
for batch in range(math.ceil(len(items)/8)):
    group=items[batch*8:(batch+1)*8]
    sheet=Image.new('RGB',(2*(width+padding)+padding,math.ceil(len(group)/2)*(height+label+padding)+padding),'#f3f4f6')
    draw=ImageDraw.Draw(sheet)
    for i,item in enumerate(group):
        x=padding+(i%2)*(width+padding); y=padding+(i//2)*(height+label+padding)
        image=Image.open(root/item['target']).convert('RGB')
        image=ImageOps.contain(image,(width,height))
        sheet.paste(image,(x,y+label)); draw.text((x,y+4),item['topic'],fill='#111f3a')
    out=root/'img/redesign'/f'branded-preview-{batch+1}.jpg'
    sheet.save(out,quality=92)
    print(str(out))
