# NORIKO — Website Prototype

Design direction prototype for the NORIKO website. Everything here is self-contained:
no build step, no npm, no dependencies to install.

---

## How to open it

**Option A — double-click `index.html`.**
Works for layout, colour and all imagery. The three brand fonts load from Google Fonts,
so you need an internet connection; without one the page falls back to system fonts and
the typography will look wrong (everything else stays correct).

**Option B — run a local server (recommended, matches production exactly).**
If you have Python installed, open a terminal in this folder and run:

```
python -m http.server 5177
```

Then open <http://localhost:5177>.

> **If you edit the CSS and see no change, hard-refresh (Ctrl+F5 / Cmd+Shift+R).**
> The stylesheet link carries a `?v=` cache-buster (currently `v=28`) — bump that number when you change
> `noriko.css` and the browser will always pick up the new file.

---

## What's in here

```
index.html                  The homepage. Commented by section.
retail.html                 The Retail hub — Cook / Snack / Drink.
products/*.html             45 product detail pages, one per SKU. Generated.
assets/data/products.json   Product data — the single source for those pages.
tools/build-products.py     Regenerates products/ from products.json.
tools/build-cook-grid.py    Regenerates the Cook grid + world-row counts in retail.html.
tools/apply-dish-images.py  Syncs dish photos into index.html + retail.html cards.
tools/import-dish-images.py Converts supplied imagery to web-ready WebP (needs Pillow).
tools/check-links.py        Verifies every local href and asset resolves.
tools/add-share-tags.py     Adds canonical + share-preview tags and writes sitemap.xml.
                            Re-run after build-products.py.
tools/make-thumbs.py       Makes small copies of dish, recipe, pack and poster images (needs Pillow).
tools/use-thumbs.py         Points card images at those copies. Run it LAST, after every generator.
tools/build-legal.py        Builds privacy.html and terms.html (text lives in the script).
                            The HoReCa product list + enquiry basket is edited in horeca.html.
assets/img/dishes/          Dish imagery — drop <slug>.webp in, see its README
assets/js/noriko.js         Shared behaviour for both pages.
assets/css/noriko.css       The whole design system. Tokens at the top.
assets/img/packshots/       Cook + HoReCa packshots
assets/img/snacks/          Snack range packshots
assets/img/juzo/            All six JUZO cups
assets/brand/               OFFICIAL logo + favicons (see BRAND-ASSETS.md)
favicon.ico                 Served at /favicon.ico
design-system/noriko/
  MASTER.md                 Design system source of truth — read this first
  BRAND-ASSETS.md           Logo rules + what official variants are still needed
  VERIFIED-FACTS.md         Every factual claim and where it came from
  PACKSHOT-SPEC.md          What to ask the designer for
  REFERENCE-ANALYSIS.md     Analysis of the seven reference sites
  pages/cook.md             Per-world overrides
  pages/snack.md
  pages/drink-juzo.md
  pages/horeca.md
```

**Read `design-system/noriko/MASTER.md` first.** It explains the three worlds, the
colour system, and the rules that hold them together.

### Changing a product

Product pages are generated, so **don't edit anything in `products/` by hand** — the
next build overwrites it. Edit `assets/data/products.json`, then:

```
python tools/build-products.py
python tools/apply-dish-images.py
python tools/check-links.py
```

The site itself still has no build step: `products/*.html` are committed as plain HTML
and open by double-click like every other page. The generator exists so thirty pages
can't drift apart, and so a weight or a price has one place to be wrong. A field that
isn't in the JSON does not appear on the page — there are no fallbacks.

---

## Ground rules before you change anything

**1. No invented facts.** This is the project's hardest rule. Every product name,
weight, pack size, price and flavour on this page traces to real packaging or the
Ashokasha Food Service Catalogue — all of it logged in `VERIFIED-FACTS.md`. If you
need a fact that isn't there, ask for it; don't fill the gap with something plausible.

**2. Visible gaps are deliberate.** The dashed `.needs-photo` blocks mark photography
that doesn't exist yet and name the exact shot required. They're meant to be seen.
Don't replace them with stock imagery or an unrelated packshot.

**3. Contrast is verified, not eyeballed.** Three places have no headroom:
- **NORIKO red `#E50607`** — white text on it is exactly 4.81:1. Any transparency at
  all drops it below AA. Text on red must be fully opaque white.
- **Panels on red must darken** (`rgba(0,0,0,.22)`), never lighten. A white overlay
  raises the ground luminance and breaks the text above it.
- **JUZO flavour colours** — every flavour has a `-fill` token (the true cup colour,
  for backgrounds and boba) and an `-ink` token (darkened, for text). Pineapple and
  green grape are unreadable as text on cream. Never set text in a `-fill`.

The current page measures **0 contrast failures** across all breakpoints, both light
and dark colour schemes, and all six JUZO flavour states. Please keep it there.

**4. The logo is the official artwork — never recreate it.** `assets/brand/` is
transcoded directly from `noriko logo.ai`, verified pixel-identical to the original
(mean delta 2.68/255, exact alignment). Never substitute a font, redraw, recolour,
stretch, crop into it, or add shadow/glow/outline. Light grounds only — there is no
official reversed version, so dark sections use a light container instead. Full rules
and the list of variants still needed: `design-system/noriko/BRAND-ASSETS.md`.

> **Open: the official logo red is `#EC2427`; the site UI red is `#E50607`.** They
> differ visibly. White on `#EC2427` measures 4.35:1 and would fail AA, so the UI red
> was not changed unilaterally. Needs the brand owner to confirm.

**5. Pan-Asian, not Japanese.** NORIKO has a Japanese-sounding name but the range spans
many Asian cuisines and origins. No hiragana, sakura, pagodas or torii in master-brand
language, and no fixed country list. Japanese references are fine *inside* a product
story where they're factually the subject (nori, sushi, wasabi).

---

## The bits worth knowing about

**The audience bar.** The slim dark strip above the logo — `Retail | HoReCa` — is the
core structural decision. NORIKO serves two very different buyers and they must never
be funnelled through the same journey. Keep it visible on every page.

**Pack → food.** Hover or keyboard-focus the Cook feature or any Cook product card and
the packshot crossfades to what it becomes. This is NORIKO's signature interaction.
**28 of the 32 Cook products now have an image**; the rest, and all 13 Snack products,
still show labelled placeholders. The images in use are AI-generated brand artwork, not
photography — they are captioned "Serving suggestion" and their provenance is recorded.
**The second image must show genuine usage of that specific product**, never another
packshot.

**The spice scale.** The snack packs already print a 1×/2×/3× rating and code flavour
by band colour. The site's Snack world is built on those existing devices rather than a
price point, because prices change and the scale won't. Show the pack marking only —
do not add interpretive descriptions of what each level tastes like.

**JUZO flavour switcher.** Picking a flavour swaps the cup and repaints the section.
The *logo artwork* renders as JUZÖ with two boba as the umlaut; **in running text,
navigation and metadata the spelling is plain JUZO.** Keep those separate.

**Editorial rhythm.** Sections deliberately use different layout primitives — an
asymmetric Cook feature, a 4-up grid, a staggered snack rail, a dense HoReCa table, a
light inspiration grid, a slim positioning band. No two consecutive sections share a
shape or a background. If you add a section, give it a shape the neighbours don't have.

**Cook carries all 32 catalogue SKUs, and 14 of them are not NORIKO.** The
foodservice catalogue spans brands — Gold nori, Green Label noodles, SUZUKA
mayonnaise and so on. Each is labelled on its card and its page. Do not "tidy"
those labels away: a reader mistaking a Gold pack for NORIKO is exactly what
the brand-ownership rule exists to prevent.

**Cook is HoReCa, not Retail.** *Corrected 28 Aug 2026.* Every Cook pack size comes
from the Food Service Catalogue and is case-configured — 1 kg rice, 1.8 L vinegar,
2 kg sushi ginger — against Snack's 12–260 g. Cook product pages carry
`audience: "horeca"`, so their breadcrumb reads Home › HoReCa › Cook and their primary
CTA is "Request pricing". A SKU can still be *listed* in the other audience's view, but
it has one primary audience and that drives its own page. **No consumer pack size has
ever been supplied for a Cook product** — see `VERIFIED-FACTS.md`.

**Pacing.** Cook / Snack / Drink appear twice — hero tiles, then each world's own
section — not three times. Real product content starts ~1,500px down on desktop. Please
don't reintroduce a third category introduction between the audience split and Cook.

**HoReCa scales.** The category filter above the spec table is sized for the full
catalogue, not the seven sample rows; it wraps rather than scrolls, so new categories
drop in without a layout change. Most categories are legitimately empty right now.

**One image-sizing trap.** Never size an image with a percentage height inside an
`aspect-ratio` parent — the computation is circular and the browser falls back to the
image's intrinsic size. It shipped a 666px image inside a 157px card here. Use
`position:absolute; inset:0` in a relative aspect box, or a fixed px `max-height`.

---

## Still needed

1. **Food photography** *(highest priority — the page's main gap)*
   **28 AI-generated brand images** are in use across Cook, captioned "Serving
   suggestion" with their provenance recorded, driving the pack→dish hover.
   Still wanted:
   - Images for the last 4 Cook SKUs and **all 13 Snack products**
   - **Seven re-rendered without the NORIKO logo** — they currently put NORIKO
     branding over Green Label, JINJIN and unbranded packs
   - Genuine photography of the dish alone, which would replace all of these
   See `assets/img/dishes/README.md` for the spec and the full filename list.
2. **Back-of-pack artwork for 25 of the 30 retail SKUs** — only the five Weilong
   snacks have labels, so only they carry ingredients, allergens and nutrition. Every
   other product page shows a labelled gap where that data belongs.
3. **Corrected nutrition panels for those five** — all five labels print an identical
   panel, which cannot be right for both a konjac jelly and a wheat snack stick. The
   figures are shown as printed and flagged "to confirm" on each page.
4. Content for the three "How to use" guides — currently titles only, marked as such
5. **Verified company background for About** — the section is built and shows a
   labelled gap. Needed: founding year, history, scale and reach, certifications
   beyond FSSAI. The catalogue contains no company text to source it from.
6. Snack MRPs — which products carry which price
7. JUZO veg/non-veg mark — not legible on the supplied packshots
8. Where-to-buy — retailer and platform list
9. A backend for the enquiry form — the flow is built and working client-side, but
   submission is not wired up (the prototype says so on submit)

---

## Brand ownership — read before adding any product

Ashokasha distributes under several brands. **Only NORIKO-branded products belong in
the NORIKO retail ranges.** Verified from packshots: Gold (nori), Green Label
(noodles) and HOT (wasabi powder) are *not* NORIKO, nor are the unbranded bulk
shiitake and black fungus. Check the pack before placing anything in Cook, Snack or
Drink. Full split in `design-system/noriko/VERIFIED-FACTS.md`.

## Scope

Built so far: the **homepage**, the **Retail hub**, and **45 product detail pages**
— 32 Cook filed under HoReCa (18 NORIKO + 14 other brands, each attributed),
13 Snack under Retail. Still to come: Cook / Snack / Drink world pages, HoReCa category
and product pages, How-to-use articles, and a full About page. About and Contact
exist as homepage sections.

Four placeholder links remain on the homepage, all pointing at content that doesn't
exist yet: the three "How to use" articles (marked "content to be written") and
"Download the catalogue".

Built as plain HTML and CSS with no framework, so it can move to any stack later
without rework. Tested at 375 / 768 / 1024 / 1440px.
