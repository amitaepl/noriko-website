# DRINK / JUZO — page overrides

Inherits `../MASTER.md`. Only the deviations are listed here.
All product facts: `../VERIFIED-FACTS.md`.

## Verified product
**JUZO by NORIKO** — a **280 ml** popping boba drink with juice. **MRP ₹90.**
Six flavours: **Strawberry, Lychee, Peach, Pineapple, Green Grape, Blueberry.**

Line in use: **"See it. Sip it. Pop it."**
Also available and unused: "Burst. Sip. Enjoy." · "Something Fun is Popping" ·
"Boba. The Way It Should Be." One line per page — do not stack them.

All six packshots supplied 27 Aug 2026 and in use (`assets/img/juzo/`).
Brand mark is **JUZÖ** — the umlaut is styled as two boba. Use the umlaut.

## The section's idea: the flavour repaints the page

The six cups are already six saturated colours. Rather than showing them as a static
grid, the section makes **flavour the control**: choosing one swaps the cup and
repaints the section's ground and headline accent to that flavour. It turns a product
line-up into the most colourful, most interactive moment on the homepage, using
nothing but the real packshots.

## Surface
- Base ground `--cream` (`#FFF6E6`), overlaid with a radial wash in the **active
  flavour**, driven by `--juzo-active` on the section element.
- Cup colours sampled from the artwork — see `../VERIFIED-FACTS.md` for the table.

## Critical contrast rule
Every flavour has a **`-fill`** and an **`-ink`** token. `-fill` is the true cup colour
and is for backgrounds, chips and boba only. `-ink` is the darkened tone used for any
text. Pineapple `#FCC000` and green grape `#84B400` in particular are unreadable as
text on cream; their ink tones (`#8A6800`, `#4F6B00`) are not. **Never set text in a
`-fill` token.** All six states verified at 0 contrast failures.

## Components
- **Spec strip** — 280 ml · ₹90 · 6 flavours. The one world where a price is both
  stable and verified.
- **Flavour switcher** — real `<button>`s with `aria-pressed`, 48px minimum height.
  Selection is carried by border colour, a checkmark **and** `aria-pressed` — never
  colour alone. Three across desktop, two tablet, one on small mobile.
- **Cup stage** — all six cups stacked, crossfading on selection. `loading="lazy"`
  on the five inactive cups.

## Motion
- Cup crossfade 420ms; ground and accent transition with it.
- Decorative boba drift gently behind the cup (7s ease-in-out).
- Both fully disabled under `prefers-reduced-motion`. No scroll-scrub, no parallax.

## Tone
Youthful and fun, not childish. No baby-talk, no cartoon mascots, no comic fonts.

## Tone
Youthful and fun, not childish. No baby-talk, no cartoon mascots, no comic fonts.
