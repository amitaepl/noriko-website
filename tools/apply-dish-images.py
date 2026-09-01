# -*- coding: utf-8 -*-
"""
Sync dish photography into the two hand-written hub pages (index.html,
retail.html), which the product-page generator does not own.

    python tools/apply-dish-images.py

For every product card it finds, this swaps the dish layer to match what is on
disk in assets/img/dishes/:

    photo present  ->  <img class="dish" ...>      (the pack->dish crossfade)
    photo absent   ->  <span class="dish needs-photo">  (the labelled gap)

It is idempotent and runs in both directions, so removing a photo restores the
placeholder. Cards are matched by the product slug in their own link, so this
does not depend on matching display names.

Safe to run repeatedly. Run it after adding or removing anything in
assets/img/dishes/, then run tools/check-links.py.
"""
import html
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from imgsize import img_size

ROOT = pathlib.Path(__file__).resolve().parent.parent
PRODUCTS = json.loads((ROOT / "assets/data/products.json").read_text(encoding="utf-8"))["products"]
BY_SLUG = {p["slug"]: p for p in PRODUCTS}
DISH_DIR = ROOT / "assets/img/dishes"
DISH_EXT = (".webp", ".jpg", ".jpeg", ".png")

PAGES = ["index.html", "retail.html"]

# A card is anything from a <li ...card...> up to its </li>, and we locate the
# product by the slug in its own product link.
CARD_RE = re.compile(r'<li class="(product-card|snack-card) reveal">.*?</li>', re.S)
SLUG_RE = re.compile(r'href="products/([a-z0-9-]+)\.html"')
DISH_LAYER_RE = re.compile(
    r'\n\s*(?:<span class="dish needs-photo"[^>]*>.*?</span>\s*</span>'
    r'|<img class="dish"[^>]*>)', re.S)


def dish_for(slug):
    """The dish image for a CARD, or None.

    'dish_card': false means the image is a pack-and-dish composite — the pack is
    already in frame, so a pack→dish crossfade would fade the pack into itself.
    Those images are used on the product page only.
    """
    p = BY_SLUG.get(slug)
    if not p or not p.get("dish_card", True):
        return None
    for ext in DISH_EXT:
        f = DISH_DIR / (slug + ext)
        if not f.exists():
            continue
        alt = p.get("dish_alt") or p.get("dish_needed")
        if not alt:
            print("  ! %s: image present but no alt text (add 'dish_alt'). Skipped." % slug)
            return None
        size = img_size(f)
        if not size:
            print("  ! %s: unreadable image dimensions. Skipped." % slug)
            return None
        focus = p.get("dish_focus")
        return {"src": "assets/img/dishes/" + f.name,
                "alt": html.escape(alt, quote=True), "w": size[0], "h": size[1],
                "style": (' style="--dish-focus:%s"' % focus) if focus else ""}
    return None


def layer_for(slug, indent):
    """The markup the card should carry, given what is on disk."""
    d = dish_for(slug)
    if d:
        return ('\n{i}<img class="dish" src="{src}" alt="{alt}" '
                'width="{w}" height="{h}" loading="lazy"{style}>').format(i=indent, **d)
    p = BY_SLUG.get(slug)
    if p and p.get("dish_needed"):
        return ('\n{i}<span class="dish needs-photo" aria-hidden="true">'
                '\n{i}  <strong>Food photo required</strong><span>{d}</span>'
                '\n{i}</span>').format(i=indent, d=p["dish_needed"])
    return ""


# The homepage's featured product is a .cook-feature, not a card — a different
# component with its own hover crossfade. It has no product link to read a slug
# from, so it is matched on its packshot filename instead.
FEATURE_RE = re.compile(r'<div class="cook-feature__media">.*?</div>', re.S)
PACK_SRC_RE = re.compile(r'class="pack" src="([^"]+)"')


def fix_feature(src, page):
    def fix(m):
        block = m.group(0)
        pm = PACK_SRC_RE.search(block)
        if not pm:
            return block
        pack = pm.group(1)
        slug = next((s for s, p in BY_SLUG.items() if p["img"] == pack), None)
        if not slug:
            print("  ! %s: featured packshot %s matches no product" % (page, pack))
            return block
        existing = DISH_LAYER_RE.search(block)
        if not existing:
            return block
        indent = re.match(r"\n(\s*)", existing.group(0)).group(1)
        if not dish_for(slug) and 'needs-photo' in existing.group(0):
            return block
        new_layer = layer_for(slug, indent)
        print("  featured product %-18s -> %s" % (
            slug, "photo" if '<img class="dish"' in new_layer else "placeholder"))
        return block[:existing.start()] + new_layer + block[existing.end():]

    return FEATURE_RE.sub(fix, src)


def main():
    total = {"photo": 0, "gap": 0, "untouched": 0}
    for page in PAGES:
        path = ROOT / page
        src = path.read_text(encoding="utf-8")
        original = src

        def fix(m):
            card = m.group(0)
            sm = SLUG_RE.search(card)
            if not sm:
                total["untouched"] += 1
                return card
            slug = sm.group(1)
            existing = DISH_LAYER_RE.search(card)
            indent = " " * 12
            if existing:
                indent = re.match(r"\n(\s*)", existing.group(0)).group(1)

            has_photo = dish_for(slug) is not None
            # Leave hand-written placeholders exactly as they are. The shot
            # descriptions on index.html and retail.html were written per page
            # and differ deliberately; this tool swaps layers, it does not
            # normalise copy.
            if not has_photo and existing and 'needs-photo' in existing.group(0):
                total["untouched"] += 1
                return card

            new_layer = layer_for(slug, indent)
            if existing:
                card = card[:existing.start()] + new_layer + card[existing.end():]
            elif new_layer:
                # No dish layer yet (snack cards) — insert after the packshot.
                img = re.search(r'<img [^>]*?>', card)
                if img:
                    card = card[:img.end()] + new_layer + card[img.end():]
            total["photo" if '<img class="dish"' in new_layer else
                  ("gap" if new_layer else "untouched")] += 1
            return card

        src = CARD_RE.sub(fix, src)
        src = fix_feature(src, page)
        if src != original:
            path.write_text(src, encoding="utf-8")
            print("%-12s updated" % page)
        else:
            print("%-12s already in sync" % page)

    print("cards: %d with photo, %d showing the gap, %d untouched"
          % (total["photo"], total["gap"], total["untouched"]))


if __name__ == "__main__":
    main()
