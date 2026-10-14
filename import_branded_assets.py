from pathlib import Path
from PIL import Image, ImageOps
import shutil, json

root=Path(__file__).resolve().parent
items=json.loads((root/'branded-image-generation.json').read_text(encoding='utf-8'))
for item in items:
    png=root/'img/redesign'/(item['topic']+'-branded.png')
    shutil.copy2(Path(item['source']),png)
    with Image.open(png) as image:
        image=ImageOps.exif_transpose(image).convert('RGB')
        image.save(root/item['target'],quality=92,optimize=True)
    print(item['topic']+' branded image saved')
