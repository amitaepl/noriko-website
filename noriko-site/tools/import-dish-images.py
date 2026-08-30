# -*- coding: utf-8 -*-
"""
Import supplied dish imagery into assets/img/dishes/ as web-ready WebP.

    python tools/import-dish-images.py <source-file> <slug> [<source-file> <slug> ...]

The supplied files are 2.4-3 MB PNGs. The rest of the site ships WebP at roughly
100-200 KB, and a 2.5 MB hero on every product page would undo that, so each is
converted to WebP and cropped to the 3:2 the page expects.

Requires Pillow (a tooling dependency only — the site itself still has none, and
the build reads image dimensions with tools/imgsize.py).
"""
import os
import pathlib
import sys

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets/img/dishes"
TARGET_W = 1800
RATIO = 3 / 2
QUALITY = 82


def convert(src, slug):
    im = Image.open(src)
    im = im.convert("RGB")
    w, h = im.size

    # Centre-crop to 3:2 so the page never crops something unexpected later.
    if abs((w / h) - RATIO) > 0.001:
        if w / h > RATIO:
            new_w = int(round(h * RATIO))
            left = (w - new_w) // 2
            im = im.crop((left, 0, left + new_w, h))
        else:
            new_h = int(round(w / RATIO))
            top = (h - new_h) // 2
            im = im.crop((0, top, w, top + new_h))

    # Only ever downscale — never invent pixels that were not supplied.
    if im.width > TARGET_W:
        im = im.resize((TARGET_W, int(round(TARGET_W / RATIO))), Image.LANCZOS)

    OUT.mkdir(parents=True, exist_ok=True)
    dest = OUT / (slug + ".webp")
    im.save(dest, "WEBP", quality=QUALITY, method=6)

    before = os.path.getsize(src) / 1024
    after = os.path.getsize(dest) / 1024
    print("  %-24s %5dx%-5d %7.0f KB  ->  %6.0f KB  (%.0f%% smaller)"
          % (dest.name, im.width, im.height, before, after,
             100 * (1 - after / before)))


def main(argv):
    if len(argv) < 2 or len(argv) % 2:
        print(__doc__)
        return 1
    pairs = list(zip(argv[0::2], argv[1::2]))
    print("converting %d image(s) to WebP, 3:2, max %dpx wide:" % (len(pairs), TARGET_W))
    for src, slug in pairs:
        if not os.path.exists(src):
            print("  ! missing: %s" % src)
            continue
        convert(src, slug)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
