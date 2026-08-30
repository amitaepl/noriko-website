# NORIKO — Design System (Master)

Source of truth for the NORIKO website. Page files in `pages/` override this document.

Derived from: NORIKO packaging artwork (sampled directly), plus structural analysis of
seven reference sites (see `REFERENCE-ANALYSIS.md`). This replaces the generic
auto-generated output — the tool's literal matches (Liquid Glass, Claymorphism,
Brutalism, legal-firm "Trust & Authority") were SaaS/startup patterns unsuited to a
food brand and were rejected. The accessibility and pre-delivery checklists from that
output are retained below.

---

## 0a. Brand assets — official artwork only

The logo is never recreated. `assets/brand/` is transcoded verbatim from
`noriko logo.ai` and verified pixel-identical to it. No substitute font, no
redrawn element, no recolouring, no reversed version invented. Full rules and
the list of variants still awaited: `BRAND-ASSETS.md`.

## 0b. Brand ownership rule

Ashokasha distributes products under several brands. **Only NORIKO-branded products
appear in NORIKO retail ranges** — Snack and JUZO. **The HoReCa catalogue is
different:** it spans brands by nature, so Cook carries all 32 catalogue SKUs and
each non-NORIKO product is named as such on its card, on its page, in its
`<title>` and in its JSON-LD. A product the reader could mistake for NORIKO is
the failure this rule exists to prevent — not the mere presence of another brand
in a trade listing. Check the packshot before placing any product in
Cook, Snack or Drink — Gold (nori), Green Label (noodles), HOT (wasabi powder) and
unbranded bulk lines are foodservice items, not NORIKO consumer products. The
verified split is in `VERIFIED-FACTS.md`.

## 0. The factual rule — above every design rule

**No claim appears on this site unless it traces to a source in `VERIFIED-FACTS.md`.**
No SKU counts, no company history, no pack sizes, no flavour names, no prices, no
country lists, no diet marks invented to fill a layout. Where a fact or an image
does not exist yet, the page shows a visible, labelled gap (`.needs-photo`, "TBC").
A visually incomplete but honest page is the correct output; a polished page
containing invented information is not.

## 1. The idea: One master brand, three worlds, two doors

NORIKO is a consumer brand that spans **Cook, Snack and Drink**, sold through both
**Retail** and **HoReCa**. It is not a pantry supplier that also does snacks. The
homepage must establish the master brand before any single world — the hero states
*Cook. Snack. Drink.* before a single ingredient is shown.

**The constant (what makes it NORIKO everywhere):**
- The **red rule** — a 3px NORIKO-red hairline that opens every section, echoing the
  chopstick stroke through the `O` of the wordmark.
- **Warm paper ground** (`#FBF8F3`), never clinical white.
- **Pack → what it becomes.** Every product surface shows the pack *and* the dish,
  snack occasion, or drink moment. Never a packshot alone.
- **Bricolage Grotesque** display type at tight tracking, sentence case.
- A **strict 12-column grid** with generous section padding.

**The variable (what makes each world its own):**
Only the *surface* and *accent* change. Type, grid, spacing, and components stay fixed.

**Which door each world belongs to.** *Corrected 28 Aug 2026.* Cook was originally
filed under Retail. It is **HoReCa**: every Cook pack size in `VERIFIED-FACTS.md`
comes from the Ashokasha Food Service Catalogue and is case-configured — 1 kg rice
(12 bags/case), 1.8 L vinegar (6 units/case), 2 kg sushi ginger. Compare Snack at
12–260 g. No consumer pack size has ever been supplied for a Cook SKU.

| World | Primary door | Why |
|---|---|---|
| COOK | **HoReCa** | Foodservice pack sizes, sold by the case |
| SNACK | Retail | 12–260 g consumer packs |
| DRINK / JUZO | Retail | 280 ml single-serve cups |

Each SKU has one **primary audience**, set as `audience` in `products.json`, and
that drives its page: breadcrumb, audience-bar `aria-current`, and primary CTA
(Retail → "Where to buy"; HoReCa → "Request pricing").

A SKU may still be *listed* in the other door's view. Cook keeps its section on
`retail.html`, badged **Cook · HoReCa** so the pack sizes are not mistaken for
consumer packs, while every Cook product page is HoReCa. The retail hub's stockist
CTA offers "Snack and JUZO" only, because those are the consumer ranges.

| World | Ground | Accent | Feel |
|---|---|---|---|
| COOK | Deep green `#16362C` / paper | Red | Refined, culinary, ingredient-led |
| SNACK | Red `#E50607` | Flavour bands + heat scale | Energetic, bold, playful |
| DRINK / JUZO | Cream `#FFF6E6` | Six fruit flavour colours | Colourful, fruity, youthful |
| HoReCa | Steel `#1B2A31` / paper | Red (CTA only) | Professional, dependable, dense |

## 1b. Pan-Asian, not Japanese

NORIKO has a Japanese-sounding name but the range spans many Asian cuisines and
origins. The master brand language must not imply a single nation.

**Removed / forbidden at master-brand level:** decorative hiragana or kanji, sakura,
pagodas, torii, waves, koi, bamboo texture, red-and-black "Japanese" clichés, and
any fixed list of countries. Japanese references are allowed *inside* a specific
product story (Nori, sushi, wasabi) where they are factually the subject.

**Language to use:** "Asian pantry", "Asian cooking", "flavours from across Asia",
"ingredients for Asian kitchens". Never a closed country list.

---

## 2. Colour tokens

Brand reds sampled directly from NORIKO packaging artwork (`(229,6,7)`, `(245,22,23)`).

```css
--noriko-red:      #E50607;  /* brand signal red — white text passes AA at 4.81:1 */
--noriko-red-deep: #B00406;  /* red text on paper (AA on light) */
/* Neutrals are cool, and that is a decision, not an inheritance. NORIKO's
   packaging is white, gloss and high-contrast — a supermarket shelf, not a
   ceramics studio. The previous warm cream (#FBF8F3) sat within 7/7/9 RGB of
   the cream that AI-generated design has converged on, and it made the reds
   read dusty. */
--ink:             #0F1413;  /* cool near-black */
--ink-soft:        #414B49;
--ink-mute:        #5F6A68;  /* clears 4.5:1 on --paper-2, not only --paper */
--paper:           #F6F8F8;  /* cool near-white — the page ground */
--paper-2:         #EAEFEE;  /* tinted surface (was --paper-warm) */
--card:            #FFFFFF;
--line:            #D7DEDD;

--cook-deep:       #16362C;  /* COOK world ground */
--steel:           #1B2A31;  /* HoReCa ground */
--cream:           #FFF6E6;  /* JUZO ground */

/* Snack flavour bands — sampled from the actual packs, which already code
   flavour by band colour. The site reuses the range's own system. */
--band-spicy:      #E11B22;
--band-mala:       #E8A317;
--band-sweet:      #B5397F;
--band-pepper:     #7DBE3C;

/* JUZO — the six actual flavours, no others */
--juzo-strawberry: #E8386A;
--juzo-lychee:     #E86A9B;
--juzo-peach:      #F2894B;
--juzo-pineapple:  #E8B317;
--juzo-grape:      #8CBF3F;
--juzo-blueberry:  #5B5BC4;

--veg-green:       #1E8A3C;  /* India veg mark */
--nonveg-brown:    #8A4B2A;  /* India non-veg mark */
```

**Rules**
- White on `--noriko-red` only. Never black on red (4.36:1, fails).
- Red text on paper must use `--noriko-red-deep`.
- Red is a *signal*, not a wash: rules, CTAs, the wordmark, one section ground. If more
  than ~15% of a viewport is red outside the SNACK world, it is wrong.
- Never convey meaning by colour alone (pack size, veg mark, and stock state all carry text).

## 3. Typography

```css
--font-display: 'Bricolage Grotesque', 'Segoe UI', system-ui, sans-serif;
--font-body:    'Inter Tight', system-ui, -apple-system, sans-serif;
```

- **Display** — section heads and hero. Weight 700–800, `letter-spacing: -0.03em`,
  `line-height: 1.02`. Sentence case, never all-caps for long strings.
- **No display serif.** Instrument Serif was declared and loaded on every page but
  applied to nothing — a font request per page load for zero glyphs, and one of the
  most over-used faces in AI-generated design. Removed. Bricolage Grotesque carries
  the personality alone. If a second voice is ever wanted, pick a face with a reason
  to be there rather than the default editorial serif.
- **Body** — 17px base (not 16), `line-height: 1.6`, measure capped at 68ch.
- Scale: 13 / 15 / 17 / 21 / 27 / 36 / 52 / 76 / 104.
- Prices, pack sizes and weights use `font-variant-numeric: tabular-nums`.

## 4. Spacing, grid, radius

```css
--space-1: 4px;  --space-2: 8px;   --space-3: 12px; --space-4: 16px;
--space-5: 24px; --space-6: 32px;  --space-7: 48px; --space-8: 64px;
--space-9: 96px; --space-10: 128px;
--radius-sm: 4px; --radius: 10px; --radius-lg: 18px; --radius-pill: 999px;
--container: 1280px;
```

- Section vertical rhythm: `--space-9` desktop, `--space-7` mobile. Generous — this is
  where the premium read comes from.
- 12-column grid, 24px gutter desktop / 16px mobile.
- Photography ratios: hero 16:9 or 21:9 full-bleed; product card 4:5 portrait;
  editorial 3:2; recipe 1:1.

## 4b. Editorial rhythm — the page is not a stack of modules

Once the IA is solved, the risk is every section reading as
*heading → paragraph → grid → button → divider*. The system fights that with:

- **Alternating section grounds** — paper → paper-2 → dark → cream → red → steel →
  paper → ink. No two adjacent sections share a surface.
- **Alternating padding** — `.section--snug` / default / `.section--loose` so the page
  breathes unevenly rather than metronomically.
- **Varied heading placement** — `.section-head--center` breaks the left-aligned run;
  used twice only (Doors, About). *About had an `sr-only` heading until 28 Aug 2026,
  so the "About" link in every nav and footer — 64 of them — landed on an unlabelled
  band. A section reachable by name needs a visible heading with that name.*
- **Different shapes per section** — an asymmetric `.cook-feature`, a 4-up product
  grid, a staggered snack rail, a dense HoReCa spec table, a light 3-up inspiration
  grid, a slim `.positioning` band. No two consecutive sections use the same layout
  primitive, and `.section--tint` separates two otherwise-adjacent light sections.
- **Product scale and overlap** — `.world-row__media img` scales past its row
  (`transform: scale(1.06)`) so packs feel physical rather than catalogued; alternate
  snack cards are lifted `--space-6` so the row is not a flat line.

## 4c. Image sizing — a trap worth documenting

**Never size an image with a percentage height inside an `aspect-ratio` parent.**
The percentage resolves against a height that is itself derived from the ratio; the
computation is circular and the browser falls back to the image's *intrinsic* size.
This shipped a 666px-tall image inside a 157px card, and made inspiration cards ~50%
taller than intended.

Use `position: absolute; inset: 0` on the image inside a `position: relative` aspect
box, or a fixed `max-height` in px. Both are deterministic.

## 4c-ii. The hero is the shelf

The opening screen leads with the product, not with type about the product. The brand
line stays on top but compact; the three worlds run **full-bleed beneath it as a
triptych**, each panel on its world colour with the packshot dominant.

Measured: packshots went from **6% to 19.1%** of the first viewport at 1440×900
(14.9% at 375×812, where the panels go side-on so the pack still reads at size).
The headline dropped from 9.7% to 8.2% — the type gave up space to the product.

**No numbered markers.** Cook, Snack and Drink are three parallel worlds, not a
sequence — nobody cooks, then snacks, then drinks. The 01/02/03 that used to sit on
the Retail hub was decoration wearing the costume of structure. Replaced with the
range size (17 products · 8 products · 6 flavours), which is a fact the reader can
use. Only number things that are genuinely ordered.

## 4d. Homepage pacing — reach product fast

Cook / Snack / Drink appear **twice**, not three times: once in the hero tiles and
once in each world's own dedicated section. An additional "three worlds" band between
the audience split and the product content was removed — it restated the hero, and
pushed real products from ~1,500px down to ~3,200px on desktop. The `.world-row`
component is retained in CSS for the Retail hub page, where the introduction is the
point of the page.

Homepage order: **hero → Retail/HoReCa → Cook products → editorial → JUZO → Snack →
HoReCa → How to use → positioning → contact.**

**Audience wording.** Retail spans cooking, snacking *and* drinking, so a retail
visitor is not necessarily entering a "kitchen". The split is headed
**"For shelves. For kitchens."** — never "Two kitchens".

## 4e. Hiding elements — `[hidden]` needs a guard

The UA rule `[hidden] { display: none }` has lower specificity than any class that
sets `display`. `.spec-row { display: grid }` beat it, so filtered rows kept
rendering while `row.hidden` reported `true`. The stylesheet now carries
`[hidden] { display: none !important; }` near the top.

**Test rendering, not state.** The filter bug survived several passes because the
checks measured `element.hidden` rather than `getBoundingClientRect().height > 0`.
Assert on what the browser actually paints.

## 5. Motion

Restrained. Motion carries meaning or it does not exist.

- Hover/state: 180ms `cubic-bezier(.2,.6,.2,1)`.
- Entrance: 420ms fade + 16px rise, staggered 60ms, **once**, via IntersectionObserver.
- Product card hover: image crossfades from packshot → the dish it makes. This is the
  brand's signature interaction and the Momofuku lesson made literal.
- Everything above is disabled under `prefers-reduced-motion: reduce`; the dish image
  is then reachable by keyboard focus instead.
- No parallax. No scroll-scrub. No autoplaying carousels without pause controls.

## 6. Components

- **Audience bar** — persistent slim bar above the masthead: `Retail | HoReCa`. Current
  audience marked with `aria-current="page"`, red underline, and a text label — not colour
  alone. (Verified pattern: Kikkoman USA uses exactly this for Home Cooking / Foodservice /
  Manufacturers.)
- **Hero world tiles** — three tiles under the brand statement, one per world, each
  carrying a real packshot. On mobile they stack and go horizontal so packshots stay
  large rather than shrinking into three small cards.
- **Spice scale** (`.spice`) — the range's own 1×/2×/3× rating, drawn as filled pips
  **plus** the text level. Never pips alone, never colour alone.
- **Diet mark** (`.diet`) — India veg (green circle) / non-veg (brown triangle), with
  a text label. Applied only where the pack actually carries the mark.
- **Snack card** — a flavour band across the top mirroring the physical pack's band
  colour, then packshot, name, net weight, heat rating, diet mark. No price: MRPs vary
  widely across the range and will change.
- **Product card (retail)** — 4:5 image, dish-on-hover, name, plain description of use,
  pack size, world tag. Appetite first, specification second.
- **About (`.about`)** — one centred column on `--paper-2`, between the 3-up
  inspiration grid and the 2-panel contact band, so it shares a shape with neither.
  Deliberately short: there is no verified company history, and the block is not
  padded out with copy that restates the rest of the page. That is what got the
  numeric credential strip removed. The missing background is a labelled gap.
- **`.needs-photo`** — a visible, labelled placeholder naming the exact shot required.
  Used wherever real photography does not exist. It is meant to be seen, not hidden.
- **Product detail page (`.pdp`)** — 5/7 split: sticky packshot figure left, name and
  facts right. Pack first, specification second, same order as the card. Sections run
  hero → *On the pack* → *Ingredients & nutrition* → *More from this world*, alternating
  ground and padding per §4b. **The dish placeholder is not a hover layer here.** On a
  card the pack→dish crossfade is the signature interaction; on a detail page the missing
  photography is stated outright, because hover-only information fails §7 and the gap is
  meant to be read. Generated by `tools/build-products.py` from
  `assets/data/products.json` — see §6b.
- **Spec row (HoReCa)** — dense horizontal row: thumbnail, name, pack size, case config,
  category, "Add to enquiry". Scannable, table-like, no marketing copy. A chef is scanning,
  not browsing.
- **Enquiry basket** — HoReCa's equivalent of a cart. Collects SKUs, submits one enquiry.
- **CTA hierarchy** — one primary per section. Retail primary = "Where to buy".
  HoReCa primary = "Request pricing".

## 6b. Product data has one source

Thirty product pages hand-maintained would drift within a week — a weight fixed on
one page and not another is exactly the kind of error §0 exists to prevent. So:

- **`assets/data/products.json`** is the single source of product truth. Every field
  in it traces to `VERIFIED-FACTS.md`.
- **`tools/build-products.py`** renders `products/<slug>.html` from it.
- **The site still has no build step.** The generated pages are committed as plain
  HTML and open by double-click like every other page; the generator is an authoring
  convenience, not a runtime dependency. Nothing on the site fetches the JSON.
- **A field absent from the JSON does not appear on the page.** No fallbacks, no
  default copy. Missing data renders as a labelled gap, per §0.

After editing either file, run `python tools/build-products.py`, then
`python tools/check-links.py` to confirm every href and asset still resolves.

**Dish imagery is convention, not configuration.** Drop `<slug>.webp` into
`assets/img/dishes/` and it appears; delete it and the labelled gap returns.
`tools/apply-dish-images.py` does the same for the two hand-written hub pages,
matching cards by the slug in their own link. Three rules hold:

- **No image ships without alt text.** `dish_alt`, or the `dish_needed` line that
  described the shot. With neither, the build skips the image and says so.
- **`dish_focus` aims the crop.** Supplied imagery is 3:2 with the pack on one
  side; the card is 4:5, so a centred `object-fit: cover` crop lands in the gap
  between pack and dish. `dish_focus` is an `object-position` that points the
  card at the food — `100% 50%` on every supplied image, panning hard right so
  the pack falls out of frame and the dish fills the card. Note that at
  3:2-into-4:5 the height fits exactly, so **only the X value has any effect**
  — panning vertically does nothing.
- **The card crop is deliberate; do not "fix" it with `contain`.** It discards
  ~47% of the image width. `contain` was tried on 28 Aug 2026 to show the whole
  frame and reverted: at 244×162 inside a 305px box it left 71px bars top and
  bottom and the dish read as a small floating thumbnail. **The pack is the
  card's resting state, so cropping the pack out of the hover loses nothing the
  reader has not just seen** — the hover exists to show the food. The full 3:2
  image is shown uncropped on the product page, which is where it belongs.
- **`dish_card: false`** withholds an image from the cards while keeping it on
  the product page. A last resort, not a default: the crossfade is the point.
- **Captions state what the image is.** AI-generated brand imagery is captioned
  "Serving suggestion", never "what it makes", and carries a `dish_source`. §0
  applies to imagery as much as to copy.

The homepage's featured product is a `.cook-feature`, **not** a card — a separate
component with its own crossfade and no product link to read a slug from.
`tools/apply-dish-images.py` matches it on its packshot filename instead. If a
new feature component is added, teach the tool about it or it will silently keep
its placeholder.

## 7. Accessibility (non-negotiable)

- Text contrast ≥ 4.5:1; large text and non-text UI ≥ 3:1. Verified per surface, light and dark.
- Visible focus ring: 3px `--noriko-red` at 2px offset, on every interactive element.
- Touch targets ≥ 44×44px; web pointer targets ≥ 24×24 CSS px minimum.
- Full keyboard operation, skip link, sequential headings, no hover-only information.
- `prefers-reduced-motion` respected throughout.
- Every meaningful image has descriptive alt text; decorative marks are `aria-hidden`.

## 8. Anti-patterns — explicitly rejected

- ❌ **Inventing any fact to complete a layout.** See §0.
- ❌ Leading the homepage with Cook, or with 1 kg foodservice packs. The master brand
  and all three worlds come first.
- ❌ Japanese script or motifs as master-brand decoration; any closed country list.
- ❌ Building Snack's identity on a price point. Prices change; the heat scale and
  flavour bands do not.
- ❌ Generic "Asian grocery" clichés: dragon motifs, faux-brush display fonts for UI,
  bamboo textures, red-gold gradients, cherry-blossom borders.
- ❌ Emoji as icons. SVG only.
- ❌ Burying HoReCa inside the retail catalogue.
- ❌ Making retail feel like a wholesale price list, or HoReCa feel like a consumer shop.
- ❌ Packshot-only grids with no dish context; substituting an unrelated packshot as
  the "dish" image.
- ❌ Replacing a missing product photo with an illustrated or abstract stand-in.
- ❌ Glassmorphism, heavy gradients, novelty cursors, decorative motion everywhere,
  complex page transitions, or any effect that competes with the food and packaging.
- ❌ Ashokasha branding competing with NORIKO on the homepage. Footer only.

## 9. Pre-delivery checklist

- [ ] No emoji as icons (SVG only)
- [ ] `cursor: pointer` on all clickable elements
- [ ] Hover states transition 150–300ms
- [ ] Text contrast ≥ 4.5:1 on every surface
- [ ] Visible keyboard focus on every interactive element
- [ ] `prefers-reduced-motion` respected
- [ ] Responsive verified at 375 / 768 / 1024 / 1440px
- [ ] No horizontal scroll at 375px
- [ ] Images have width/height or aspect-ratio (CLS)
- [ ] Both audience doors reachable within one interaction from any page
