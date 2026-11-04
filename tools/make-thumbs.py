"""Make small copies of the big food photos for cards and grids.

Cards show these photos at ~400 px wide, so loading the 1536 px originals
(150-230 KB each) wastes time. The thumbnails are 800 px wide (~30-60 KB).
Product and recipe pages still use the full-size originals.

    python tools/make-thumbs.py        (needs Pillow)

Writes thumbs/ folders next to the dishes, recipes, packshots and snacks, and
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
    im = Image.open(src)
    # Packshots are cut-outs: keep their transparency instead of turning it black.
    im = im.convert("RGBA") if (im.mode in ("RGBA", "LA", "P") and "A" in im.convert("RGBA").getbands() and im.convert("RGBA").getchannel("A").getextrema()[0] < 255) else im.convert("RGB")
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    im.save(dst, "WEBP", quality=quality, method=4, alpha_quality=70)
    return True


made = 0
for folder, pattern in (("assets/img/dishes", "*.webp"), ("assets/img/recipes", "*-final.webp")):
    for src in sorted((ROOT / folder).glob(pattern)):
        made += thumb(src, src.parent / "thumbs" / src.name, 800, 74)
# Packs on cards are shown ~220 px wide: 440 px is plenty, even on phones.
for folder in ("assets/img/packshots", "assets/img/packshots/imported-brands", "assets/img/snacks"):
    for src in sorted((ROOT / folder).iterdir()):
        if src.suffix.lower() in (".webp", ".jpg", ".jpeg", ".png"):
            made += thumb(src, src.parent / "thumbs" / (src.stem + ".webp"), 440, 72)
made += thumb(ROOT / "assets/img/noriko-horeca-banner.jpeg", ROOT / "assets/img/noriko-horeca-banner-800.webp", 800, 66)
print("thumbnails written:", made)
