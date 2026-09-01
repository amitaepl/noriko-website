# Dish imagery — drop files here

Put an image in this folder and it appears on the site at the next build.
**No page edits, no HTML.**

```
python tools/build-products.py
python tools/apply-dish-images.py
python tools/check-links.py
```

Delete a file and the labelled placeholder comes back. Both directions are safe
to re-run, and running with nothing here changes nothing.

---

## Naming

`<slug>.webp` — or `.jpg` / `.png`. The slug is the product page filename, so
`products/sushi-rice.html` takes `sushi-rice.webp`. Full list at the bottom.

## Specification

| | Spec |
|---|---|
| **Ratio** | **3:2 landscape.** The page crops to 3:2; anything else is centre-cropped. |
| **Size** | 1800×1200 px. Displays up to ~900px wide, so this covers retina. |
| **Content** | **Genuine use of that specific product** — the dish it makes, or the product in a real kitchen context. |
| **Not acceptable** | Another packshot, stock imagery, or an unrelated dish. |
| **Colour** | sRGB. |

---

## The four fields in `products.json`

Only `dish_alt` is required, and only when the shot has no `dish_needed` line.

| Field | What it does |
|---|---|
| `dish_alt` | Alt text. Falls back to `dish_needed`. **The build refuses to publish an image with neither** rather than ship it undescribed. |
| `dish_caption` | The caption under the image. Defaults to **"Serving suggestion"**. |
| `dish_source` | Provenance. Set it for anything that is not original photography. |
| `dish_focus` | `object-position` aiming the card's 4:5 crop at the food, e.g. `"88% 82%"`. Supplied images are 3:2 with the pack to one side, so a centred crop misses the dish. **Only the X value has any effect** at this ratio. |
| `dish_card` | `false` withholds the image from the cards but keeps it on the product page. A last resort — the hover crossfade is the point. |

---

## Currently supplied — AI-generated brand images, 28 Aug 2026

**28 images, covering 28 of the 32 Cook SKUs.** All captioned "Serving
suggestion". They drive the pack→dish hover crossfade on the cards and the
homepage's featured product, and appear as a 3:2 figure on the product page.

Because each shows the pack beside the dish, every one carries
`dish_focus: "100% 50%"` — panned hard right so the card crop lands on the food,
not the pack. The one exception is `wasabi-paste` (`30% 8%`), whose food sits
upper-left.

**The card deliberately crops ~47% of the image width away.** Cards are 4:5,
these images are 3:2; `object-fit: contain` was tried so nothing was cut and
reverted, because it left the dish as a small thumbnail between two white bars.
The pack is already the card's resting state, so the hover only needs the food.
**Supplying dish images cropped to 4:5, framed on the food, would remove the
trade-off entirely** — they would fill the card with nothing lost.

Import new files with:

```
python tools/import-dish-images.py "<source.png>" <slug>
```

which crops to 3:2, downscales to 1800px and writes WebP. It needs Pillow
(`pip install Pillow`) — a tooling dependency only; the site still has none.

### Still without an image

**Cook (4):** `dried-shiitake-mushroom` · `nori-sheet-10` · `nori-sheet-50` ·
`rice-vinegar-1-8l`

**Snack (all 13).** No shot was ever specified for these, so each will need a
`dish_alt` written when its image arrives.

### ⚠ Seven images carry NORIKO branding over another brand's pack

Ramen, soba, udon and somen (Green Label); pickled radish (unbranded); salted
black beans (Yangjiang Yuesheng); hondashi (JINJIN). The product pages correctly
say "This is not a NORIKO product" — but the image beside that line shows the
NORIKO logo. **These should be re-rendered without the lockup.** Mayonnaise,
wasabi powder, bean paste and sesame oil are already correct and carry no NORIKO
branding: that is the pattern to follow.

---

## Filenames

### Cook — 17 products

| Filename | Product | Shot |
|---|---|---|
| `sushi-rice.webp` | Sushi Rice | Cooked, seasoned sushi rice |
| `glutinous-rice.webp` | Glutinous Rice | A steamed glutinous rice dish |
| `rice-vinegar.webp` | Rice Vinegar | A dressing or dipping sauce |
| `sushi-vinegar.webp` | Sushi Vinegar | Sushi rice being seasoned |
| `gochujang.webp` | Gochujang | A finished Korean dish |
| `gochugaru.webp` | Gochugaru — Hot Pepper Flakes | Kimchi or a stew being made |
| `shichimi-togarashi.webp` | Shichimi Togarashi | Noodles or rice finished with togarashi |
| `kimchi-sauce.webp` | Kimchi Sauce | A finished kimchi dish |
| `wasabi-paste.webp` | Prepared Wasabi in Tube | Sushi or sashimi serving |
| `dried-shiitake-mushroom.webp` | Dried Shiitake Mushroom | A broth or stir-fry using shiitake |
| `dried-black-fungus.webp` | Dried Black Fungus | A stir-fry or salad using black fungus |
| `white-fungus.webp` | White Fungus | A soup or dessert using white fungus |
| `porcini-mushroom.webp` | Porcini Mushroom | A dish using rehydrated porcini |
| `canned-bamboo-shoots.webp` | Canned Bamboo Shoots | A stir-fry or braise using bamboo shoots |
| `canned-water-chestnuts.webp` | Canned Water Chestnuts | A stir-fry using water chestnuts |
| `sushi-ginger-white.webp` | Sushi Ginger (White) | Sushi served with pickled ginger |
| `sushi-ginger-pink.webp` | Sushi Ginger (Pink) | Sushi served with pickled ginger |

### Snack — 13 products

No shot was ever specified for these, so any image needs a `dish_alt` in
`products.json`.

`fried-fish-spicy` · `fried-fish-mala` · `fried-fish-pepper` ·
`fried-fish-sweet-sour` · `fried-squid-spicy` · `fermented-tofu-spicy` ·
`braised-lotus-root-slice` · `roasted-tofu-block` · `big-latiao` ·
`mini-latiao` · `kiss-burn` · `konjac-shuang-hot-spicy` ·
`konjac-shuang-sour-spicy`
