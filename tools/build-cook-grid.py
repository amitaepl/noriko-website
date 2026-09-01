# -*- coding: utf-8 -*-
"""
Regenerate the Cook product grid inside retail.html from products.json.

The grid was hand-written and drifted: products.json carried 32 Cook SKUs while
the page still showed the original 17. Card markup that repeats 32 times is not
something to maintain by hand.

    python tools/build-cook-grid.py

Only the <ul class="product-grid"> inside <section id="cook"> is replaced.
Everything else on the page is left alone. Run tools/apply-dish-images.py
afterwards to put the dish layers back.
"""
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PRODUCTS = json.loads((ROOT / "assets/data/products.json").read_text(encoding="utf-8"))["products"]
PAGE = ROOT / "retail.html"


def card(p):
    brand = p.get("brand", "NORIKO")
    # Non-NORIKO products are named as such on the card itself, not only on the
    # product page — a shopper scanning the grid must not read them as NORIKO.
    brand_line = ""
    if not brand.startswith("NORIKO"):
        brand_line = ('\n            <p class="product-card__brand">'
                      + brand.replace(" — not NORIKO", "") +
                      ' <span>· Imported &amp; distributed by NORIKO</span></p>')

    dish = ""
    if p.get("dish_needed"):
        dish = ('\n            <span class="dish needs-photo" aria-hidden="true">'
                '\n              <strong>Food photo required</strong><span>'
                + p["dish_needed"] + "</span>"
                "\n            </span>")

    diet = ""
    if p.get("diet"):
        lbl = "Veg" if p["diet"] == "veg" else "Non-veg"
        diet = ('\n              <span class="diet diet--' + p["diet"] +
                '"><i aria-hidden="true"></i>' + lbl + "</span>")

    use = ('\n            <p class="product-card__taste">' + p["use"] + "</p>") if p.get("use") else ""

    return """        <li class="product-card reveal">
          <div class="product-card__media">
            <span class="product-card__flag product-card__flag--cook">Cook</span>
            <img class="pack" src="{img}" alt="{alt}" width="{w}" height="{h}" loading="lazy">{dish}
          </div>
          <div class="product-card__body">{brand_line}
            <h3><a href="products/{slug}.html">{name}</a></h3>{use}
            <div class="product-card__meta">
              <span class="product-card__size num">{size}</span>{diet}
            </div>
          </div>
        </li>""".format(img=p["img"], alt=p["alt"], w=p["w"], h=p["h"], dish=dish,
                        brand_line=brand_line, slug=p["slug"], name=p["name"],
                        use=use, size=p["size"], diet=diet)


def main():
    src = PAGE.read_text(encoding="utf-8")
    cook = [p for p in PRODUCTS if p["world"] == "cook"]

    start = src.index('<section class="section" id="cook"')
    end = src.index("</section>", start)
    block = src[start:end]

    m = re.search(r'<ul class="product-grid">.*?</ul>', block, re.S)
    if not m:
        raise SystemExit("no product-grid found inside the Cook section")

    grid = '<ul class="product-grid">\n' + "\n".join(card(p) for p in cook) + "\n      </ul>"
    new_block = block[:m.start()] + grid + block[m.end():]
    PAGE.write_text(src[:start] + new_block + src[end:], encoding="utf-8")

    before = block.count('<li class="product-card reveal">')
    print("Cook grid: %d cards -> %d" % (before, len(cook)))
    other = [p for p in cook if not p.get("brand", "NORIKO").startswith("NORIKO")]
    print("  %d NORIKO, %d other brands (each labelled on the card)"
          % (len(cook) - len(other), len(other)))

    sync_counts()

    # Rebuilding the cards replaces their markup, including any dish-photo
    # hover layers. Restore those layers automatically so a routine catalogue
    # update cannot silently remove the food photography.
    subprocess.run([sys.executable, str(ROOT / "tools/apply-dish-images.py")],
                   cwd=ROOT, check=True)


def sync_counts():
    """Keep the world-row counts honest.

    These are hand-written and had already drifted — Snack read "8 products"
    against 13 cards. §4c-ii uses the range size as the marker precisely because
    it is a fact the reader can use, so a wrong number is worse than none.
    """
    src = PAGE.read_text(encoding="utf-8")
    n = {}
    for w in ("cook", "snack"):
        n[w] = len([p for p in PRODUCTS if p["world"] == w])

    changed = []
    for world, count in n.items():
        pat = (r'(<a class="world-row world-row--%s[^"]*"[^>]*>.*?'
               r'<span class="world-row__count">)([^<]*)(</span>)' % world)
        m = re.search(pat, src, re.S)
        if not m:
            continue
        want = "%d products" % count
        if m.group(2) != want:
            changed.append("%s: %s -> %s" % (world, m.group(2), want))
            src = src[:m.start(2)] + want + src[m.end(2):]

    if changed:
        PAGE.write_text(src, encoding="utf-8")
        for c in changed:
            print("  count %s" % c)
    else:
        print("  counts already correct")


if __name__ == "__main__":
    main()
