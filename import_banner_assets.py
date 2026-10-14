from pathlib import Path
from PIL import Image, ImageOps
import json, shutil

root=Path(__file__).resolve().parent
manifest=json.loads((root/'banner-generation.json').read_text(encoding='utf-8'))
dest=root/'img/redesign'
dest.mkdir(exist_ok=True)
for item in manifest:
    source=Path(item['source'])
    target=dest/(item['topic']+'.png')
    if not target.exists(): shutil.copy2(source,target)
    with Image.open(target) as image:
        image=ImageOps.exif_transpose(image).convert('RGB')
        if image.width>2400: image.thumbnail((2400,2400))
        image.save(dest/(item['topic']+'.jpg'),quality=90,optimize=True)
    print(item['topic']+' saved')
