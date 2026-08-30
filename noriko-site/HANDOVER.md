# Handover — read this first

Orientation for anyone (human or AI) picking this project up cold. It records
**decisions and open questions**, not structure — for structure read `README.md`,
then `design-system/noriko/MASTER.md`, then `VERIFIED-FACTS.md`.

Last updated 28 Aug 2026.

---

## What exists

| | |
|---|---|
| `index.html` | Homepage — hero, audience split, Cook, editorial, JUZO, Snack, HoReCa spec table, How-to-use, About, Contact |
| `retail.html` | Retail hub — Cook, Snack, JUZO sections |
| `products/*.html` | **45 product pages. Generated — never hand-edit.** |
| `assets/data/products.json` | The single source for those pages |
| `tools/*.py` | Six build/check tools |

45 products = **32 Cook** (audience: HoReCa) + **13 Snack** (audience: Retail).

## The two rules that override normal instincts

**1. No invented facts.** Every weight, price, pack size, flavour and diet mark
must trace to `VERIFIED-FACTS.md`. Where a fact is missing the page shows a
**visible labelled gap** — never plausible filler. An invented origin story
("We started by supplying the kitchens that got it right") and a fake SKU count
("120+ Asian pantry SKUs") were both written once and had to be removed. Don't
re-create them.

**2. Generated files.** `products/*.html` and the Cook grid inside `retail.html`
are built from `products.json`. Edit the JSON, then:

```
python tools/build-products.py
python tools/build-cook-grid.py
python tools/apply-dish-images.py
python tools/check-links.py
```

`import-dish-images.py` needs Pillow (`pip install Pillow`) — a tooling
dependency only. The site itself still installs nothing and has no build step.

## Decisions already made — don't silently reverse these

- **Cook is HoReCa, not Retail.** Every Cook pack size comes from the Food
  Service Catalogue and is case-configured (1 kg rice, 1.8 L vinegar, 2 kg sushi
  ginger) against Snack's 12–260 g. Cook keeps a section on `retail.html` badged
  *Cook · HoReCa*, but its product pages are HoReCa. **No consumer pack size has
  ever been supplied for a Cook SKU.**
- **14 of the 32 Cook SKUs are not NORIKO** — Gold, Green Label, HOT, SinhoFOOD,
  JINJIN, SUZUKA, Jianhua, Zhaofenghe and two unbranded. Each is labelled on its
  card, page, `<title>` and JSON-LD. **Do not "tidy" those labels away.**
- **The card dish crop discards ~47% of the image width, deliberately.** Cards
  are 4:5, dish images 3:2; `dish_focus` pans the crop onto the food. `contain`
  was tried and reverted — it left the dish as a small thumbnail between white
  bars. The full image is shown uncropped on the product page.
- **Dish imagery is AI-generated brand artwork, not photography.** Captioned
  "Serving suggestion", provenance in `dish_source`.
- **JUZO has its own site, <https://drinkjuzo.com>.** Decision: cross-link only,
  both domains kept. This site is a gateway; drinkjuzo.com owns the depth.

## Open — needs the brand owner, not a developer

1. **8 dish images put the NORIKO logo over another brand's pack** (Green Label
   ramen/soba/udon/somen, Gold nori, JINJIN hondashi, unbranded pickled radish
   and salted black beans). The page says "not a NORIKO product" beside an image
   showing the NORIKO logo. Needs re-rendering without the lockup. Four others
   (SUZUKA, HOT, Zhaofenghe, Jianhua) are already correct — follow those.
2. **All five Weilong labels print an identical nutrition panel** — a konjac
   jelly and a wheat snack stick cannot share one. Published as printed with a
   visible "to confirm" note.
3. **"Manufactured By: xxxyyyzzz"** — unfilled placeholder on all five labels.
4. **No company background exists.** The About section is built and carries a
   labelled gap. Needs founding year, history, scale, certifications.
5. **drinkjuzo.com has no outbound links** — the cross-link is one-way until it
   links back.
6. **13 Snack products have no dish image**, and no shot was ever specified, so
   each needs a `dish_alt` written when its image arrives.
7. **Diet marks unconfirmed** for the 14 non-NORIKO Cook SKUs. Mayonnaise and
   hondashi matter most.
8. **Nori Sheet 10 and 50 share an image** whose pack reads "50 sheets".
9. Official logo red `#EC2427` vs site UI red `#E50607` — white on the logo red
   measures 4.35:1 and would fail AA, so it was not changed unilaterally.

## Quality bar to maintain

Verified across all 47 pages at 1280 and 375: **0 contrast failures, 0
horizontal scroll, 0 undersized pointer targets, 0 images missing alt or
dimensions, 0 broken links.** `tools/check-links.py` gates the last one; the
rest were measured in-browser. Please keep it there.

## Running it

```
python -m http.server 5177
```

Hard-refresh after CSS changes — the stylesheet carries a `?v=` cache-buster
(currently **v=29**); bump it when you edit `noriko.css`.
