# -*- coding: utf-8 -*-
"""
Generate products/<slug>.html from assets/data/products.json.

The SITE has no build step — these pages are committed as plain HTML and open by
double-click like every other page. This script exists so 30 near-identical pages
stay consistent, and so the product data has one source rather than thirty.

    python tools/build-products.py

Rule, same as everywhere else in this project: a field that is not in
products.json does not appear on the page. Missing data renders as a visible,
labelled gap, never as plausible copy.
"""
import html
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from imgsize import img_size

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "assets/data/products.json").read_text(encoding="utf-8"))
PRODUCTS = DATA["products"]
CSS_V = "28"

DISH_DIR = ROOT / "assets/img/dishes"
DISH_EXT = (".webp", ".jpg", ".jpeg", ".png")
WARNINGS = []


def dish_of(p):
    """The dish photo for a product, or None.

    Convention over configuration: drop <slug>.webp into assets/img/dishes/ and
    it is picked up on the next build. Nothing to edit in products.json.

    An image is never used without alt text — 'dish_alt' in products.json, or
    the 'dish_needed' line that described the shot. If neither exists the image
    is skipped and the build says so, rather than shipping an undescribed photo.
    """
    for ext in DISH_EXT:
        f = DISH_DIR / (p["slug"] + ext)
        if not f.exists():
            continue
        alt = p.get("dish_alt") or p.get("dish_needed")
        if not alt:
            WARNINGS.append("%s: dish image found but no alt text — add 'dish_alt' "
                            "to products.json. Image not used." % p["slug"])
            return None
        size = img_size(f)
        if not size:
            WARNINGS.append("%s: could not read dimensions of %s. Image not used."
                            % (p["slug"], f.name))
            return None
        focus = p.get("dish_focus")
        return {"src": "assets/img/dishes/" + f.name, "alt": html.escape(alt, quote=True),
                "w": size[0], "h": size[1],
                "style": (' style="--dish-focus:%s"' % focus) if focus else "",
                # Brand marketing composites show the pack beside a plated idea, so
                # they are captioned as a serving suggestion, not as the dish the
                # product makes. Real usage photography can override per product.
                "caption": p.get("dish_caption", "Serving suggestion")}
    return None

WORLD = {
    "cook":  {"label": "Cook",  "hash": "cook",  "flag": "product-card__flag--cook"},
    "snack": {"label": "Snack", "hash": "snack", "flag": "product-card__flag--snack"},
}

# Where a SKU's canonical page sits. Cook is HoReCa: every Cook pack size in
# VERIFIED-FACTS comes from the Food Service Catalogue — 1 kg rice, 1.8 L
# vinegar, 2 kg sushi ginger — and each is case-configured. A SKU may still be
# listed in the other audience's view; this only decides its own page.
AUDIENCE = {
    "retail": {
        "label": "Retail",
        "crumb": ("../retail.html", "Retail"),
        "world_href": "../retail.html#",
        "cta": '<a class="btn btn--primary" href="../retail.html#where">Where to buy</a>',
    },
    "horeca": {
        "label": "HoReCa",
        "crumb": ("../index.html#horeca", "HoReCa"),
        "world_href": "../index.html#horeca",
        # MASTER §6: HoReCa's primary CTA is "Request pricing".
        "cta": ('<a class="btn btn--primary" href="../index.html#horeca">Request pricing</a>\n'
                '          <a class="btn btn--ghost" href="../retail.html">Retail range</a>'),
    },
}

ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" '
         'stroke-linecap="round" stroke-linejoin="round"><path d="M9 6l6 6-6 6"/></svg>')


def plain(s):
    """HTML-escaped source text -> plain text, for JSON-LD."""
    return html.unescape(s or "")


def head(p):
    w = WORLD[p["world"]]
    a = AUDIENCE[p.get("audience", "retail")]
    is_retail = p.get("audience", "retail") == "retail"
    # aria-current marks the audience this page belongs to, so the switcher tells
    # the truth about where the visitor is (MASTER §6).
    aud_retail = ' aria-current="true"' if is_retail else ""
    aud_horeca = "" if is_retail else ' aria-current="true"'
    crumb_href, crumb_label = a["crumb"]
    brand = p.get("brand", "NORIKO")
    is_noriko = brand.startswith("NORIKO")
    # A Gold or Green Label pack must not be titled NORIKO just because it
    # sits on NORIKO's site (§0b).
    title = (p["name"] + " — NORIKO " + w["label"]) if is_noriko else (
        p["name"] + " — " + brand + " · NORIKO " + w["label"] + " catalogue")
    desc = plain(p.get("use") or (plain(p["name"]) + ", " + p["size"] + ". NORIKO " + w["label"] + "."))
    ld = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": plain(p.get("full_name") or
                      (("NORIKO " if is_noriko else "") + plain(p["name"]))),
        "image": "../" + p["img"],
        "brand": {"@type": "Brand", "name": brand.replace(" — not NORIKO", "")},
    }
    if p.get("use"):
        ld["description"] = plain(p["use"])

    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,600;12..96,700;12..96,800&family=Inter+Tight:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="icon" href="../favicon.ico" sizes="16x16 32x32 48x48">
<link rel="icon" type="image/png" sizes="192x192" href="../assets/brand/icon-192.png">
<link rel="icon" type="image/png" sizes="512x512" href="../assets/brand/icon-512.png">
<link rel="apple-touch-icon" sizes="180x180" href="../assets/brand/apple-touch-icon-180.png">
<link rel="stylesheet" href="../assets/css/noriko.css?v={cssv}">
<script type="application/ld+json">{ld}</script>
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>

<div class="audience-bar">
  <div class="container">
    <nav class="audience-switch" aria-label="Choose your audience">
      <span class="audience-switch__label" id="aud-label">I'm here for</span>
      <a href="../retail.html"{aud_retail} aria-describedby="aud-label">Retail</a>
      <a href="../index.html#horeca"{aud_horeca} aria-describedby="aud-label">HoReCa &amp; Professional Kitchen</a>
    </nav>
    <div class="audience-bar__aside">
      <a href="../index.html#contact">Trade &amp; stockist enquiries</a>
    </div>
  </div>
</div>

<header class="masthead">
  <div class="container">
    <a class="brand" href="../index.html" aria-label="NORIKO home">
      <img src="../assets/brand/noriko-logo-full.svg" alt="NORIKO" width="464" height="187">
    </a>

    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="primary-nav">
      <span class="sr-only">Menu</span>
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" width="22" height="22" aria-hidden="true">
        <path d="M4 7h16M4 12h16M4 17h16"/>
      </svg>
    </button>

    <nav class="nav" id="primary-nav" aria-label="Primary">
      <a href="../retail.html#cook">Cook</a>
      <a href="../retail.html#snack">Snack</a>
      <a href="../retail.html#drink">Drink</a>
      <a href="../index.html#horeca">HoReCa</a>
      <a href="../index.html#inspiration">How to use</a>
      <a href="../about.html">About</a>
      <a href="../index.html#contact">Contact</a>
    </nav>
  </div>
</header>

<main id="main">

  <nav class="crumbs container" aria-label="Breadcrumb">
    <ol>
      <li><a href="../index.html">Home</a></li>
      <li aria-hidden="true">{arrow}</li>
      <li><a href="{crumb_href}">{crumb_label}</a></li>
      <li aria-hidden="true">{arrow}</li>
      <li><a href="{world_href}">{wlabel}</a></li>
      <li aria-hidden="true">{arrow}</li>
      <li><span aria-current="page">{name}</span></li>
    </ol>
  </nav>
""".format(title=title, desc=desc, cssv=CSS_V,
           ld=json.dumps(ld, ensure_ascii=False), arrow=ARROW,
           aud_retail=aud_retail, aud_horeca=aud_horeca,
           crumb_href=crumb_href, crumb_label=crumb_label,
           world_href=(a["world_href"] + w["hash"]) if p.get("audience") == "retail"
                      else a["world_href"],
           wlabel=w["label"], name=p["name"])


def chips(p):
    out = ['<span class="chip chip--size num">' + p["size"] + "</span>"]
    if p.get("diet"):
        lbl = "Veg" if p["diet"] == "veg" else "Non-veg"
        out.append('<span class="diet diet--' + p["diet"] + '"><i aria-hidden="true"></i>' + lbl + "</span>")
    if p.get("heat"):
        pips = ('<i class="on"></i>' * p["heat_pips"]) + ("<i></i>" * (3 - p["heat_pips"]))
        out.append('<span class="spice"><span class="spice__pips">' + pips + "</span>" + p["heat"] + "</span>")
    if p.get("ready_to_eat"):
        out.append('<span class="chip">Ready to eat</span>')
    return "\n          ".join(out)


def hero(p):
    w = WORLD[p["world"]]
    aud = p.get("audience", "retail")
    a = AUDIENCE[aud]

    # The foodservice catalogue spans brands. Anything that is not NORIKO says
    # so on its own page, in words, above the pack size.
    brand = p.get("brand", "NORIKO")
    brandbadge = ""
    if not brand.startswith("NORIKO"):
        label = brand.replace(" — not NORIKO", "")
        brandbadge = ("\n        <p class=\"pdp__brand\"><span>" + label +
                      "</span> Listed in the NORIKO foodservice catalogue. "
                      "This is not a NORIKO product.</p>")

    band = ""
    if p["world"] == "snack":
        band = ('<span class="pdp__band" style="background:var(' + p["band"] +
                ')" aria-hidden="true"></span>\n          ')

    # On a card the dish is a hover crossfade. On the product page both are shown
    # outright — hover-only information is not allowed (§7), and until the
    # photography exists the gap is the point.
    d = dish_of(p)
    dish = ""
    if d:
        # In the hero, at or just below the fold — eager, not lazy, so it is not
        # deferred behind the viewport check on the one screen that needs it.
        dish = ("""
        <figure class="pdp__dish">
          <img src="../{src}" alt="{alt}" width="{w}" height="{h}" loading="eager" decoding="async">
          <figcaption>{caption}</figcaption>
        </figure>""").format(**d)
    elif p.get("dish_needed"):
        dish = ("""
        <div class="needs-photo pdp__gap">
          <strong>Food photo required</strong><span>""" + p["dish_needed"] + "</span>\n        </div>")

    price = ""
    if p.get("mrp"):
        price = ("""
        <p class="pdp__price"><span class="num">""" + p["mrp"] + """</span>
          <span class="pdp__price-note">MRP, incl. of all taxes · <span class="num">""" +
                 p["usp"] + "</span></span></p>")

    # Snack packs carry no description we can source, so there is simply no lede.
    # Rendered inline so an absent one leaves no dangling blank line.
    use = ('\n        <p class="lede">' + p["use"] + "</p>") if p.get("use") else ""

    return """
  <!-- ============================================================
       Product hero — pack first, specification second.
       ============================================================ -->
  <section class="section section--snug pdp-head" aria-labelledby="pdp-h">
    <div class="container pdp">
      <div class="pdp__figure">
        <div class="pdp__media">
          {band}<img class="pack" src="../{img}" alt="{alt}" width="{w}" height="{h}" loading="eager">
        </div>{dish}
      </div>

      <div class="pdp__info">
        <hr class="rule">
        <p class="eyebrow"><a href="{world_href}">{wlabel} · {audlabel}</a></p>{brandbadge}
        <h1 id="pdp-h">{name}</h1>{use}
        <div class="pdp__chips">
          {chips}
        </div>{price}
        <div class="pdp__actions">
          {cta}
        </div>
      </div>
    </div>
  </section>
""".format(band=band, img=p["img"], alt=p["alt"], w=p["w"], h=p["h"], dish=dish,
           world_href=(a["world_href"] + w["hash"]) if aud == "retail" else a["world_href"],
           wlabel=w["label"], audlabel=a["label"], cta=a["cta"],
           name=p["name"], use=use, chips=chips(p), price=price,
           brandbadge=brandbadge)


def factlist(p):
    """On-pack facts. Only rows we can source."""
    rows = []
    rows.append(("Brand", p.get("brand", "NORIKO").replace(
        " — not NORIKO", " <em>(not NORIKO)</em>")))
    if p.get("full_name"):
        rows.append(("Full name on pack", p["full_name"]))
    rows.append(("Net weight" if p["world"] == "snack" else "Pack size", p["size"]))
    if p.get("diet"):
        rows.append(("Diet mark", "Veg" if p["diet"] == "veg" else "Non-veg"))
    if p.get("heat"):
        rows.append(("Heat rating printed on pack", p["heat"]))
    if p.get("ready_to_eat"):
        rows.append(("Preparation", "Ready to eat"))
    if p.get("category"):
        rows.append(("Food category", p["category"]))
    if p.get("origin"):
        rows.append(("Origin", p["origin"]))
    if p.get("storage"):
        rows.append(("Storage", p["storage"]))
    if p.get("case"):
        rows.append(("Foodservice case", p["case"]))
    if p.get("fssai"):
        rows.append(("FSSAI licence", '<span class="num">' + p["fssai"] + "</span>"))
    if p.get("importer"):
        rows.append(("Imported in India by", p["importer"]))

    items = "\n".join(
        '        <div class="factlist__row"><dt>' + k + "</dt><dd>" + v + "</dd></div>"
        for k, v in rows)

    conflict = ""
    if p.get("conflict"):
        conflict = ('\n      <p class="note note--warn"><strong>To confirm.</strong> ' +
                    p["conflict"] + "</p>")

    src = ""
    if p.get("source"):
        src = '\n      <p class="note">Source: ' + p["source"] + ".</p>"

    return """
  <!-- ============================================================
       What the pack says
       ============================================================ -->
  <section class="section section--tint" aria-labelledby="pack-h">
    <div class="container pdp-cols">
      <div class="section-head">
        <div>
          <hr class="rule">
          <h2 id="pack-h">On the pack</h2>
        </div>
      </div>
      <dl class="factlist">
{items}
      </dl>{conflict}{src}
    </div>
  </section>
""".format(items=items, conflict=conflict, src=src)


def ingredients(p):
    if not p.get("ingredients"):
        # Honest gap — this SKU's back-of-pack artwork has not been supplied.
        return """
  <!-- Ingredients not supplied for this SKU — visible, labelled gap. -->
  <section class="section section--snug" aria-labelledby="ing-h">
    <div class="container pdp-cols">
      <div class="section-head">
        <div>
          <hr class="rule">
          <h2 id="ing-h">Ingredients &amp; nutrition</h2>
        </div>
      </div>
      <div class="needs-photo" style="max-width:62ch">
        <strong>Back-of-pack artwork not yet supplied</strong>
        <span>Ingredients, allergen declaration and the nutrition panel for {name} will be published here once the regulatory label is provided.</span>
      </div>
    </div>
  </section>
""".format(name=p["name"])

    allerg = ""
    if p.get("allergens"):
        allerg = ('\n      <p class="allergens"><strong>Allergens.</strong> ' +
                  p["allergens"] + "</p>")

    nrows = "\n".join(
        '          <tr><th scope="row">' + n + '</th><td class="num">' + a +
        '</td><td class="num">' + r + "</td></tr>"
        for n, a, r in p["nutrition"])

    warns = "\n".join("        <li>" + w + "</li>" for w in p["warnings"])

    return """
  <!-- ============================================================
       Ingredients, nutrition and the statutory warnings, transcribed
       from the back-of-pack artwork. Nothing here is paraphrased.
       ============================================================ -->
  <section class="section section--snug" aria-labelledby="ing-h">
    <div class="container pdp-cols">
      <div class="section-head">
        <div>
          <hr class="rule">
          <h2 id="ing-h">Ingredients &amp; nutrition</h2>
        </div>
      </div>

      <h3 class="pdp__sub">Ingredients</h3>
      <p class="ingredients">{ing}</p>{allerg}

      <h3 class="pdp__sub">Nutrition information</h3>
      <p class="note">Servings per pack {servings} · serving size <span class="num">{ss}</span>.</p>
      <div class="nutri-wrap">
        <table class="nutri">
          <caption class="sr-only">Nutrition information per serving</caption>
          <thead>
            <tr><th scope="col">Per serving</th><th scope="col">Amount</th><th scope="col">%RDA</th></tr>
          </thead>
          <tbody>
{nrows}
          </tbody>
        </table>
      </div>
      <p class="note">Percent Recommended Dietary Allowance is based on a 2,000 kcal a day diet and is used for general nutrition advice; calorie needs may vary.</p>
      <p class="note note--warn">{nnote}</p>

      <h3 class="pdp__sub">Warnings on the pack</h3>
      <ul class="warnings">
{warns}
      </ul>
    </div>
  </section>
""".format(ing=p["ingredients"], allerg=allerg, servings=p["servings"],
           ss=p["serving_size"], nrows=nrows, nnote=p["nutrition_note"], warns=warns)


def related(p):
    aud = p.get("audience", "retail")
    a = AUDIENCE[aud]
    sibs = [q for q in PRODUCTS if q["world"] == p["world"] and q["slug"] != p["slug"]]
    order = [q["slug"] for q in PRODUCTS if q["world"] == p["world"]]
    start = order.index(p["slug"])
    picks = (sibs + sibs)[start:start + 4]
    w = WORLD[p["world"]]

    cards = []
    for q in picks:
        dish = ""
        qd = dish_of(q) if q.get("dish_card", True) else None
        if qd:
            # Real photography: the card's pack→dish crossfade, the signature
            # interaction. Focus reveals it too, so it is not hover-only.
            dish = ('\n            <img class="dish" src="../{src}" alt="{alt}" '
                    'width="{w}" height="{h}" loading="lazy"{style}>').format(**qd)
        elif q.get("dish_needed"):
            dish = ("""
            <span class="dish needs-photo" aria-hidden="true">
              <strong>Food photo required</strong><span>""" + q["dish_needed"] +
                    "</span>\n            </span>")
        diet = ""
        if q.get("diet"):
            lbl = "Veg" if q["diet"] == "veg" else "Non-veg"
            diet = ('<span class="diet diet--' + q["diet"] +
                    '"><i aria-hidden="true"></i>' + lbl + "</span>")
        qb = q.get("brand", "NORIKO")
        qbrand = ("" if qb.startswith("NORIKO") else
                  '\n            <p class="product-card__brand">' +
                  qb.replace(" — not NORIKO", "") + "</p>")
        cards.append("""        <li class="product-card reveal">
          <div class="product-card__media">
            <span class="product-card__flag {flag}">{wlabel}</span>
            <img class="pack" src="../{img}" alt="{alt}" width="{iw}" height="{ih}" loading="lazy">{dish}
          </div>
          <div class="product-card__body">
            <h3><a href="{slug}.html">{name}</a></h3>{qbrand}
            <div class="product-card__meta">
              <span class="product-card__size num">{size}</span>
              {diet}
            </div>
          </div>
        </li>""".format(flag=w["flag"], wlabel=w["label"], img=q["img"], alt=q["alt"],
                        iw=q["w"], ih=q["h"], dish=dish, slug=q["slug"],
                        name=q["name"], size=q["size"], diet=diet, qbrand=qbrand))

    return """
  <!-- ============================================================
       More from this world
       ============================================================ -->
  <section class="section section--tint" aria-labelledby="rel-h">
    <div class="container">
      <div class="section-head">
        <div>
          <hr class="rule">
          <h2 id="rel-h">More from {wlabel}</h2>
        </div>
        <a class="link-arrow" href="{world_href}">See the whole {wlabel} range
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
        </a>
      </div>
      <ul class="product-grid">
{cards}
      </ul>
    </div>
  </section>
""".format(wlabel=w["label"], cards="\n".join(cards),
           world_href=(a["world_href"] + w["hash"]) if aud == "retail"
                      else a["world_href"])


TAIL = """
  <!-- ============================================================ CTA ============================================================ -->
  <section class="section cta-band on-dark" aria-labelledby="cta-h">
    <div class="container">
      <hr class="rule">
      <h2 id="cta-h">Stock NORIKO</h2>
      <p class="lede" style="margin-bottom:var(--space-7)">For supermarkets, modern trade, quick commerce and e-commerce platforms.</p>
      <div class="cta-band__grid">
        <div class="cta-panel">
          <p class="eyebrow">Retail</p>
          <h3>Become a stockist</h3>
          <p>Consumer packs across Snack and JUZO.</p>
          <a class="btn btn--primary" href="mailto:info@aepl.biz?subject=NORIKO%20retail%20stockist%20enquiry">Become a stockist</a>
        </div>
        <div class="cta-panel">
          <p class="eyebrow">HoReCa</p>
          <h3>Supplying a kitchen instead?</h3>
          <p>Professional pack sizes and case configurations are in the foodservice catalogue.</p>
          <a class="btn btn--ghost" href="../index.html#horeca">Go to HoReCa</a>
        </div>
      </div>
    </div>
  </section>

</main>

<footer class="footer on-dark">
  <div class="container">
    <div class="footer__grid">
      <div>
        <span class="brand brand--on-dark brand--footer">
          <img src="../assets/brand/noriko-logo-full.svg" alt="NORIKO" width="464" height="187">
        </span>
        <p class="footer__note">Asian cooking ingredients for professional kitchens, ready-to-eat snacks and JUZO popping boba drinks.</p>
      </div>
      <div>
        <h4>Retail</h4>
        <ul>
          <li><a href="../retail.html#cook">Cook</a></li>
          <li><a href="../retail.html#snack">Snack</a></li>
          <li><a href="../retail.html#drink">Drink · JUZO</a></li>
          <li><a href="../retail.html#where">Where to buy</a></li>
        </ul>
      </div>
      <div>
        <h4>HoReCa</h4>
        <ul>
          <li><a href="../index.html#horeca">Professional catalogue</a></li>
          <li><a href="../index.html#horeca">Pack sizes</a></li>
          <li><a href="../index.html#horeca">Build an enquiry</a></li>
        </ul>
      </div>
      <div>
        <h4>Company</h4>
        <ul>
          <li><a href="../about.html">About NORIKO</a></li>
          <li><a href="../index.html#inspiration">How to use</a></li>
          <li><a href="../index.html#contact">Contact</a></li>
        </ul>
      </div>
    </div>
    <div class="footer__base">
      <span>NORIKO India · Thane West 400604 · MH (INDIA)</span>
      <span>Helpline <a href="tel:+918928227122" class="num">89282 27122</a> · <a href="mailto:info@aepl.biz">info@aepl.biz</a></span>
    </div>
  </div>
</footer>

<script src="../assets/js/noriko.js"></script>
</body>
</html>
"""


def build():
    outdir = ROOT / "products"
    outdir.mkdir(exist_ok=True)
    for p in PRODUCTS:
        page = head(p) + hero(p) + factlist(p) + ingredients(p) + related(p) + TAIL
        (outdir / (p["slug"] + ".html")).write_text(page, encoding="utf-8")

    have = sum(1 for p in PRODUCTS if dish_of(p))
    print("wrote %d pages to products/  ·  dish photos in use: %d/%d"
          % (len(PRODUCTS), have, len(PRODUCTS)))
    for w in dict.fromkeys(WARNINGS):
        print("  ! " + w)


if __name__ == "__main__":
    build()

