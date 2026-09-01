# Packshot spec — what to ask the designer for

Every packshot currently on the site is **cropped out of a PDF** (the launch deck
or the HoReCa artwork set). That works, but it is the source of every clipping
problem so far, and it caps quality at whatever resolution the deck embedded.

Supplying these properly removes the guesswork permanently.

---

## The ask, in one line

**Front-of-pack packshot, PNG with transparency, 2000px on the long edge,
product filling ~90% of frame, nothing cropped.**

## The detail

| | Spec | Why |
|---|---|---|
| **Format** | **PNG-24 with alpha** (transparent background) | Lets a pack sit on white cards, the red Snack ground, the green Cook ground and the coloured JUZO block without a visible box. Site converts to WebP; supply PNG. |
| **Background** | **Fully transparent.** If transparency isn't possible, **pure white `#FFFFFF`**, flat — no gradient, no vignette, no studio backdrop | A soft grey or gradient backdrop cannot be keyed out without eating into the pack. This is exactly what blocked three of the Weilong packs. |
| **Size** | **2000px on the long edge** minimum | Site displays up to ~900px; 2000px covers retina and future use. |
| **Framing** | Product fills **~90%** of the frame, centred, with **at least 5% clear margin on all four sides** | No element — flash, tab, corner seal — should touch a frame edge. |
| **Cropping** | **Nothing cut.** Include hang tab, corner flashes ("Extra 60%"), and the full seal | The clipped Kiss Burn and Konjac packs were missing exactly these. |
| **Angle** | Straight-on front, upright, consistent across the range | Cards sit side by side; mixed angles read as inconsistent. |
| **Shadow** | Either none, or a soft contact shadow **on the alpha** (not painted onto a background) | A baked shadow becomes a grey rectangle on coloured grounds. |
| **Colour** | sRGB | Everything else on the site is sRGB. |
| **Naming** | `noriko-<product>-<variant>.png`, e.g. `noriko-konjac-shuang-hot-spicy.png` | Predictable, no spaces. |

## Priority order

1. **The 5 Weilong SKUs** — Big Latiao, Mini Latiao, Kiss Burn, Konjac Shuang
   Hot & Spicy, Konjac Shuang Sour & Spicy. Currently the weakest assets: cropped
   from deck photography and kept on white because three cannot be cut out.
2. **JUZO, all six flavours** — currently cut out from JPEGs; usable, but a native
   transparent original would be cleaner.
3. **Anything new** — supply to this spec from the start.

## What is already fine

The HoReCa artwork set (`noriko horeca high images`) arrived as PNGs with real
alpha and a soft contact shadow. **That set is the reference — ask for the same
treatment.** If the designer asks "like what?", point them at
`shiitake mushroom.png` from that folder.

## Also worth requesting, separately

- **Reversed / light NORIKO logo** for dark grounds (currently worked around with
  a light container).
- **Compact wordmark** for tight mobile headers.
- **Confirmed brand red** — the official logo red is `#EC2427`; the site UI red is
  `#E50607`. White text on `#EC2427` measures 4.35:1 and would fail AA.
