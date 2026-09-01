# SNACK — page overrides

Inherits `../MASTER.md`. Only the deviations are listed here.
All product facts: `../VERIFIED-FACTS.md`.

## The positioning — built to outlive a price change

The range's own packaging already carries two ownable devices:

1. **Colour-coded flavour bands** — red (Spicy), gold (Mala), magenta (Sweet & Sour),
   green (Pepper). Flavour is legible before you read a word.
2. **A printed 1×–3× spice rating** — "1× Spicy", "2× Spicy", "3× Spicy / Super Spicy".

Snack's identity is built on these, not on a price. **₹30 is not a range-wide fact** —
verified MRPs in the range run ₹150–₹500 — and pricing will change. The homepage
therefore shows **no snack prices at all**; net weight and heat rating carry the cards.

Working headline: **"Ready to eat. Rated for heat."**
Rejected: "Thirty rupees. Serious heat." — too narrow, and factually unsupported.

## Surface
- Ground is `--noriko-red` (`#E50607`) at full bleed. Commit to it; do not tint it.
- Product cards sit on **white** so packshots read cleanly.
- The band strip at the top of each card mirrors the pack's own flavour band.

## Critical contrast rules
1. White on `#E50607` is exactly **4.81:1** — no headroom. All text on red must be
   **fully opaque white**; any alpha drops body copy below AA.
2. Panels on red must **darken** (`rgba(0,0,0,.22)`), never lighten. A white overlay
   raises the ground luminance and pushes white text under 4.5:1.
3. `.world-snack` colour overrides are scoped with child selectors so white cards on
   the red ground keep dark text — a blanket `.world-snack h3 { color:#fff }` produced
   white-on-white card titles.

## Components
- **Spice pips + text.** Always both. A colour or pip count alone fails
  "don't convey meaning by colour alone".
- **Print the pack marking only.** Show `1× Spicy`, `2× Spicy`, `3× Spicy` exactly as
  the packs do. Do **not** add interpretive descriptions — "mild, flavour-forward",
  "properly hot" and similar were written into an earlier draft and removed; nobody
  has verified what those levels taste like. The visual system carries the meaning.
- **Where a pack carries no rating, show none.** Sweet & Sour, Lotus Root, Roasted Tofu
  Block and Tofu Curd Skewer have no printed rating and must not be assigned one.
- **Mobile: horizontal snap rail.** Eight stacked cards ran to ~3,100px of scroll. The
  rail bleeds to the screen edge so the next card peeks, keeps packs large, and is
  keyboard-reachable (`tabindex="0"` with an `aria-labelledby` hint). The rail scrolls;
  the page body never does.
- **Diet mark on every card.** The fish and squid snacks are **non-veg**; the tofu and
  lotus root products are veg. Never apply one mark across the range.
- Buttons use `--radius-sm` (`.btn--square`) — squarer reads louder.

## Range shown on the homepage
Fried Fish (Spicy / Mala / Sweet & Sour / Pepper), Fried Squid, Fermented Tofu,
Roasted Tofu Block, Braised Lotus Root Slice. The Weilong-manufactured NORIKO
products (Big Latiao, Kiss Burn, Konjac Shuang) are part of the range but do not
lead the homepage.

## Avoid
- Cook green, JUZO fruit colours, HoReCa steel.
- Editorial serif — this world has no quiet register.
- Any price as a permanent brand device.
