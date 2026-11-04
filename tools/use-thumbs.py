"""Point card images at their small thumbnails. Run LAST, after every generator.

Lazy-loaded pack images on the retail, home and HoReCa pages and on the cards of
the product pages are swapped for the 440 px copies made by tools/make-thumbs.py.
Hero and product-page main images (loading="eager") keep the full-size files.
Safe to re-run.

    python tools/make-thumbs.py && python tools/use-thumbs.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMG = re.compile(r"<img\b[^>]*>")
SRC = re.compile(r'(src=")((?:\.\./)?assets/img/(?:packshots/imported-brands|packshots|snacks)/)([^"/?]+)\.(?:webp|jpe?g|png)(\?[^"]*)?(")')

changed = 0
pages = [ROOT / n for n in ("retail.html", "index.html", "horeca.html")] + sorted((ROOT / "products").glob("*.html"))
for page in pages:
    text = page.read_text(encoding="utf-8")

    def fix(m):
        tag = m.group(0)
        if 'loading="lazy"' not in tag:
            return tag
        return SRC.sub(lambda s: s.group(1) + s.group(2) + "thumbs/" + s.group(3) + ".webp" + (s.group(4) or "") + s.group(5), tag)

    new = IMG.sub(fix, text)
    if new != text:
        page.write_text(new, encoding="utf-8")
        changed += 1
print("pages updated:", changed)
