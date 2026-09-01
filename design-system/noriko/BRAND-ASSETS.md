# NORIKO brand assets — official artwork only

`noriko logo.ai` is the single source of truth. Everything in `assets/brand/`
derives from it mechanically. **No approximation, substitute font, or redrawn
element exists in this project any more.**

---

## How the files were produced

The `.ai` is PDF-compatible and contains **pure vector paths** — no text, no
embedded images. The SVG was produced by a **mechanical transcode** of the PDF
content stream: every path operator was re-emitted as SVG path data with the
identical coordinates, applying only the PDF→SVG y-axis flip and the `cm`
transforms already present in the file.

Nothing was redrawn, smoothed, simplified or re-interpreted.

**Operators transcoded, all of them:**
3,875 moveto · 2,900 lineto · 8,902 curveto · 330 v · 460 y · 44 rect · 725 closepath

**Verification.** The transcoded SVG was rendered and pixel-compared against a
render of the original `.ai` at 904×365:

| Measure | Result |
|---|---|
| Best alignment offset | **dx 0, dy 0** — exact |
| Mean channel delta | **2.68 / 255** (1.05%) |
| Pixels differing >30 | 5.6% — anti-aliasing on brush-texture edges only |
| Ink bounding box | matches within 1px on all four edges |
| Ink coverage | within 0.11% |
| Colours | exact match, both fills |

## Colour

The artwork uses two CMYK fills. A naive `1-(c+k)` conversion produces visibly
wrong values, so the sRGB equivalents were taken from a **colour-managed render**
of the file's embedded ICC profile:

| Element | CMYK in file | sRGB used | Naive conversion (wrong) |
|---|---|---|---|
| Wordmark | 0.746 0.676 0.668 0.898 | `#030505` | `#000000` |
| Red | 0.004 0.988 0.969 0 | `#EC2427` | `#FE0308` |

> **⚠ Open question for the brand owner.** The official logo red `#EC2427` does
> **not** match the site's UI red `#E50607` (sampled from packaging photography).
> They are visibly different. This has not been resolved unilaterally because:
> - White text on `#EC2427` measures **4.35:1 — below the 4.5:1 AA floor.**
>   Adopting it as the UI red would break contrast across the Snack world.
> - White text on `#E50607` measures 4.81:1 and passes.
>
> **Please confirm the official brand red** (a Pantone or hex spec would settle
> it). Until then the logo keeps its own faithful colour and the UI keeps
> `#E50607`. Do not "harmonise" these by editing the logo.

---

## Files

| File | Use |
|---|---|
| `noriko-logo-full.svg` | The complete official lockup — kana + wordmark + O-device. 421KB raw, **106KB gzipped**. |
| `noriko-o-device.svg` | The red O-device alone, isolated by **selecting existing subpaths** (24 of the 29 red subpaths). No geometry altered. |
| `o-device-1024.png` | 1024px master raster of the device, transparent. |
| `icon-16/32/48/192/512.png` | Favicons, transparent. |
| `apple-touch-icon-180.png` | Opaque white ground, per Apple convention. |
| `favicon.ico` | Multi-size 16/32/48. |
| *(project root)* `favicon.ico` | Served at `/favicon.ico`. |

The O-device was isolated by rendering **only** its subpaths — an earlier attempt
that cropped the region from the full artwork pulled in part of the black
wordmark, which sits immediately alongside it.

Device centring verified: margins 77/78px horizontal, 258/257px vertical in the
1024 master. Only red ink present.

---

## Usage rules

**Never**: redraw, substitute a font, recolour, stretch, compress, skew, rotate,
crop into the artwork, separate elements (other than the approved O-device for
small formats), or apply shadow, glow, bevel, gradient, outline or stroke. The
logo does not animate — motion happens around it, never to it.

**Aspect ratio** is 464.32 : 187.48 = **2.4766**. Enforced in CSS with
`height: <n>px; width: auto`. Verified at every breakpoint.

**Light grounds only.** The wordmark is near-black. No reversed/white official
version has been supplied and one must not be invented, so where the logo sits
on a dark surface it gets its own light container (`.brand--on-dark`) rather
than a recoloured logo. This is how the footer works today.

**Clear space** is built into `.brand` as padding and is never reduced to save
header height.

**Accessible name** is `NORIKO home` on the linked logo — never the filename and
never the Japanese lettering.

**Japanese lettering.** のりこ is part of the official lockup and stays there.
It must **not** be lifted out and used as decoration elsewhere. The site around
the logo stays pan-Asian: no sakura, pagodas, rising-sun motifs or Japanese
red/black styling unless a specific Japanese product story warrants it.

---

## Measured sizing

| Breakpoint | Logo rendered | Kana height | Aspect | Clipping |
|---|---|---|---|---|
| 375px | 114 × 46 | 11.5px | 2.4766 ✓ | none |
| 768px | 114 × 46 | 11.5px | 2.4766 ✓ | none |
| 1024px | 129 × 52 | 13.0px | 2.4764 ✓ | none |
| 1440px | 129 × 52 | 13.0px | 2.4764 ✓ | none |

**Legibility test.** The five kana strokes were rendered at candidate sizes and
counted as connected ink regions. They remain **five separate regions down to
11px**, so they are not merging into blobs at header size. 52px was chosen over
the 44px first tried so the kana sits at 13px with margin rather than on the
limit; the masthead grew from 76px to 88px to accommodate it rather than
squeezing the logo.

---

## Variants still required from the brand owner

1. **Reversed / light logo** for dark grounds. Currently worked around with a
   light container. Needed for the footer and any dark section.
2. **Compact or responsive wordmark.** The full lockup is 2.48:1 and carries the
   kana; a horizontal-only or kana-free variant would sit better in tight
   mobile headers. **Not invented here** — must be supplied officially.
3. **Confirmed brand red** — see the colour warning above. This is the most
   consequential open item.
4. **A square or compact icon mark.** The O-device is 869 × 509 in the 1024
   master — it is wide, because the chopsticks extend well past the circle. At
   16px the circle itself is only ~5px. Cropping to just the circle would mean
   cutting the chopstick strokes mid-stroke, i.e. cropping into the artwork, so
   it has not been done. A purpose-drawn square icon mark would serve favicons
   far better.
5. **An optimised SVG.** 106KB gzipped is heavy for a header asset. The brush
   texture genuinely needs 3,889 subpaths, but a designer-simplified production
   version (approved by the brand owner) would reduce it.

---

## Product photography

Source: `noriko horeca high images` (32 PNGs, 65 MB). Processed into
`assets/img/packshots/` as **WebP with alpha**, cropped to the artwork's alpha
bounding box and capped at 900px on the long edge.

**65 MB → 3.4 MB**, no visible quality loss at display sizes. WebP was chosen over
PNG because it is ~7× smaller with alpha intact (109 KB vs 791 KB on a test file).

The source PNGs carry real transparency with a soft contact shadow — they composite
cleanly onto the white product cards and onto the coloured world grounds alike. They
are *not* flat-background images, despite appearing so in some preview tools.

Every `<img>` now carries its true intrinsic `width`/`height`, so nothing shifts as
images load. Verified: 0 dimension mismatches on both pages.
