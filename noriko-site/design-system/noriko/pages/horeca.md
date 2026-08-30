# HoReCa — page overrides

Inherits `../MASTER.md`. Only the deviations are listed here.

**Reference lineage:** Kikkoman (the audience bar, and a genuinely separate foodservice
section), Sempio (authority through demonstrated capability).

## The governing principle
A chef or purchase manager is **scanning, not browsing**. Lead with specification;
recipe inspiration is a distraction here. This world should be visibly denser and more
serious than anything in Retail — that contrast is the point, and it is how a visitor
knows instantly which side of the business they are on.

**Tone caution.** Do not assume the buyer already knows exactly what they need — a chef
exploring a new cuisine is as valid a visitor as a purchase manager reordering. Copy
should offer specifications, not presume expertise. Rejected: "You already know what you
need." In use: *"Product specifications, professional pack sizes and case configurations
upfront, so you can find what your kitchen needs quickly."*

## Surface
- Ground is `--steel` (`#1B2A31`). Panels at `rgba(255,255,255,.05)` with
  `rgba(255,255,255,.14)` borders.
- Red is reserved strictly for CTAs and the active-state marker. Nothing decorative.

## Density
- Tightest in the system: section padding `--space-8`, row padding `--space-3`/`--space-4`.
- Spec rows, not product cards. 56px thumbnail, name + sub-spec, pack size, action.

## Type
- Body one step down (15–16px) — more information per screen.
- Pack sizes, case counts and weights always `font-variant-numeric: tabular-nums`.
- No editorial serif in this world.

## Components
- **Spec row** — `56px | name+spec | pack size | enquiry`. On mobile it reflows to a
  stacked grid; it must never become a horizontally scrolling table.
- **Enquiry basket** — replaces the cart, because NORIKO is not a B2B e-commerce store.
  Full flow: **browse → add → review → details → submit → team responds.**
  - Row toggles carry `aria-pressed` and change label to "Added ✓" — state by text,
    not colour alone. Count announced through a polite live region.
  - The review list shows product **name + pack/case config**, each with its own
    Remove control; removing there resets the corresponding row button.
  - Details captured: name, business name, city, phone, email. All with visible
    `<label>`s and correct `autocomplete` / `type` attributes.
  - **No prices anywhere.** The form states that pricing comes back from the team.
- **Category filter** (`.filters`) — pill buttons above the spec table, sized for the
  full catalogue rather than the seven sample rows. It wraps instead of scrolling, so
  adding categories never breaks the layout. Active state carries fill, colour **and**
  `aria-pressed`. Categories with no products yet return a plain "No products in this
  category yet" message rather than an empty table — expected while the visible rows
  are a sample. Filtering does not disturb the enquiry basket.
- Categories: Sushi & Nori · Mushrooms & Vegetables · Sauces & Pastes · Oils & Vinegars ·
  Rice & Noodles · Flours & Coatings.
- Primary CTA is always "Request pricing". Secondary is "Download the catalogue".

## Avoid
- Consumer merchandising language: bundles, "save 30%", impulse framing.
- Recipe cards. Usage guidance here is yield and application, not dinner ideas.
- Hiding pack sizes behind a product-detail click. The spec is the headline.

---

## Catalogue listing (updated)

The spec table now carries the **full foodservice range** — 32 rows across
Sushi & Nori, Mushrooms & Vegetables, Sauces & Pastes, Oils & Vinegars and
Rice & Noodles. Flours & Coatings is empty: tempura flour is in the catalogue but
no packshot has been supplied, so the filter honestly returns "no products yet".

**Brand labels.** Ashokasha's foodservice range spans several brands. Rows that are
not NORIKO now carry a small brand tag — Gold, Green Label, HOT, JINJIN, SUZUKA,
Zhaofenghe, Jianhua, or "Other brand" where the maker is unclear. 13 of 32 rows are
labelled. This resolves the open question in the honest direction: nothing on a
NORIKO site reads as NORIKO when it isn't. Reversible if the brand owner prefers
a different treatment.

**Preview cap.** The homepage shows the first 10 rows with a "Show all 32 products"
control, so the section stays proportionate (1,743px rather than 3,524px). When a
dedicated HoReCa page exists, the homepage should show a curated subset and link
through; the full table belongs on that page.
