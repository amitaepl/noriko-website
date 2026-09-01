# Reference site analysis — what NORIKO takes, what it leaves

All seven sites were visited and inspected (DOM, computed type/colour, navigation
structure, content order) on 27 Aug 2026. Notes below are observations, then the
decision each one drove.

---

## 1. Yutaka — yutaka.london
**Observed.** Homepage leads with **Featured Recipes before Featured Products** — ten
recipes with difficulty (Easy/Medium/Expert) and time (15 min → over 1 hour) on every
card, then thirteen products. Nav is short: Recipes, Our Story, Where to Buy, a recipe
book, and Shop as a *separate* subdomain. Search is a prominent keyword field in the header.

**Take.** Recipes first, products second — for a pantry brand the dish is the demand
driver. Difficulty + time metadata on every recipe card. A prominent keyword search for
a large range. "Where to buy" as a top-level nav item, because a retail-distributed brand
is not primarily a shop.

**Leave.** The shop living on a different subdomain — it splits the experience. And the
homepage is a long undifferentiated list; there's no editorial breathing room.

---

## 2. Clearspring — clearspring.co.uk
**Observed.** Category tiles as the primary entry (TOFU / MATCHA / SEAVEG / UDON / MISO)
sitting directly under the hero. White ground, Cabin throughout, 17.6px body, 50.7px H1 at
weight **400** — the restraint is doing the premium work, not weight or decoration. Credential
strip: Organic, Family-Run, Plant-Based, Refined Sugar Free. Per-product customer quotes
attached to individual named products. Price ranges shown as min–max across pack sizes.

**Take.** Ingredient-word category tiles as navigation. Light-weight large headings.
A short credential strip near the top. Quotes bound to a specific product, not a generic
testimonial wall. Showing pack-size ranges rather than one price.

**Leave.** Everything on one white ground — NORIKO's three worlds need to feel different.
And the range reads as a single premium tier; NORIKO has a ₹30 snack alongside 1kg foodservice.

---

## 3. Kikkoman USA — kikkomanusa.com
**Observed — the single most important structural finding.** A persistent utility bar
*above* the main nav: **Home Cooking | Foodservice | Manufacturers**. Three audiences, three
doors, always visible, never nested. The main nav below it (Products, Recipes, About Us,
Where to Buy) then belongs to whichever audience you picked. Also: a stat strip — 140 products,
2,200+ recipes, 68+ years, 300+ years of tradition — and recipe *collections* framed by occasion
("30 Minutes or Less", "Rise & Dine", "Get Your Grill On") rather than by ingredient.

**Take.** The audience bar, adopted almost directly — it is the cleanest solution to
NORIKO's Retail/HoReCa split and it is proven at exactly this scale of range. Occasion-based
recipe collections. A quantified credibility strip.

**Leave.** The visual language is corporate-heritage and a little flat; NORIKO should feel
more contemporary. Three audiences is one too many for NORIKO — two doors, not three.

---

## 4. Fly By Jing — flybyjing.com
**Observed.** Full deep-green ground (`#046135`) with white type — the whole page commits
to one saturated brand colour. Custom display face (JeanLuc) set uppercase, body at 22px
(unusually large), buttons with 0px radius. Founder's first-person story ("HEY, JING HERE.")
placed high on the homepage. Membership programme as a major homepage block.

**Take.** The confidence to commit a full section to one saturated brand colour rather
than tinting it. Oversized body copy in editorial blocks. Founder/origin voice placed early.
Square-cornered buttons in the loud world.

**Leave.** The all-caps display for long strings hurts scanning. A single saturated ground
across the *entire* site would flatten NORIKO's three worlds. And the register is too
aggressive for HoReCa buyers.

---

## 5. Momofuku Goods — shop.momofuku.com
**Observed.** Graphik uppercase headings, 16px body, white ground. Every hero slide is a
product with a benefit line plus 2–3 bullet proofs ("Restaurant quality ingredients",
"Complimentary Chili Crunch Spoon"). Sampler/bundle merchandising ("try all and save 30%").
Testimonials attached per product line. Heavy carousel use.

**Take.** Bullet proofs on product cards. Bundle/sampler merchandising — directly applicable
to the ₹30 snack range and to JUZO multipacks. The "restaurant-grade, made easy" positioning
is a genuine bridge between NORIKO's HoReCa credibility and its retail range.

**Leave.** The carousel-heavy homepage (accessibility cost, and content hidden off-screen).
Uppercase everything.

---

## 6. Sempio — en.sempio.com
**Observed.** Authority built through news and corporate activity (expos, workshops,
contests) rather than decoration. Products organised by *line* (Yondu, Soy Sauce, Korean
Cuisine Sauce) with a one-line purpose statement each.

**Take.** One-line purpose statement per product line. Authority via demonstrated activity
rather than ornament.

**Leave.** The site is dated and corporate-newsroom-led; product discovery is weak. Also a
caution: Sempio is explicitly Korean, whereas NORIKO spans Japanese, Chinese, Korean and
Thai — NORIKO must not pretend to be single-nation.

---

## 7. Numata Nori — numatanori.com
**Observed.** Lusitana + Noto Serif JP, 55px headings against **14px** body — an extreme
size ratio that creates stillness. Near-empty homepage: a founding date (1937), a single
claim (first-harvest nori only), a store, and how it's made. Very generous whitespace.

**Take.** The large-heading/small-body ratio and generous vertical rhythm for the COOK
world and editorial sections. Provenance stated as a plain fact, not a badge. The confidence
to leave a section almost empty.

**Leave.** 14px body is too small for the web at NORIKO's scale. And this level of emptiness
would starve a catalogue of NORIKO's breadth — it is a *tone* for COOK, not a homepage model.

---

## Synthesis

| Site | Lesson extracted | Applied to |
|---|---|---|
| Yutaka | Recipes before products; recipe metadata; search | Homepage order, recipe cards |
| Clearspring | Ingredient-word tiles; light large headings; credential strip | Retail categories, type scale |
| **Kikkoman** | **Persistent audience bar** | **Site-wide IA — the core structural decision** |
| Fly By Jing | Full-colour section commitment; founder voice early | SNACK world, brand story |
| Momofuku | Bullet proofs; bundles; dish-not-pack | Product cards, hover interaction |
| Sempio | Purpose line per product line; authority via activity | Category descriptions |
| Numata | Heading/body ratio; generous rhythm; plain provenance | COOK world, editorial sections |

**The thing none of them do**, and NORIKO's own idea: a product card whose image
**crossfades from the pack to the dish it becomes** on hover/focus. Momofuku shows dishes,
Clearspring shows packs — none of them shows the transformation in a single component.
That is NORIKO's signature.
