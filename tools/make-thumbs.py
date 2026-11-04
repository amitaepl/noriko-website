"""Make small copies of the big food photos for cards and grids.

Cards show these photos at ~400 px wide, so loading the 1536 px originals
(150-230 KB each) wastes time. The thumbnails are 800 px wide (~30-60 KB).
Product and recipe pages still use the full-size originals.

    python tools/make-thumbs.py        (needs Pillow)

Writes assets/img/dishes/thumbs/, assets/img/recipes/thumbs/ and
assets/img/noriko-horeca-banner-800.webp. Safe to re-run: existing thumbs that
are newer than their source are skipped.
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent


def thumb(src, dst, width, quality):
    if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    im = Image.open(src).convert("RGB")
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    im.save(dst, "WEBP", quality=quality, method=6)
    return True


made = 0
for folder, pattern in (("assets/img/dishes", "*.webp"), ("assets/img/recipes", "*-final.webp")):
    for src in sorted((ROOT / folder).glob(pattern)):
        made += thumb(src, src.parent / "thumbs" / src.name, 800, 74)
made += thumb(ROOT / "assets/img/noriko-horeca-banner.jpeg", ROOT / "assets/img/noriko-horeca-banner-800.webp", 800, 66)
print("thumbnails written:", made)
