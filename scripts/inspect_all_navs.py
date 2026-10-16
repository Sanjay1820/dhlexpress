import glob
from pathlib import Path
import re

files = glob.glob('*.html')
print(f'Total HTML files: {len(files)}')

navs = set()
for f in files:
    content = Path(f).read_text(encoding='utf-8')
    m = re.search(r'<nav class="site-nav"[\s\S]*?</nav>', content)
    if m:
        clean_nav = re.sub(r'\s*class="active"|\s*aria-current="page"', '', m.group(0))
        navs.add(clean_nav)
    else:
        print(f'NO NAV in {f}')

print(f'Unique nav structures across all files: {len(navs)}')
