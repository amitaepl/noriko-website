"""Add canonical + Open Graph / Twitter share tags and the Google Analytics tag
to every page, and write sitemap.xml.

Re-run after tools/build-products.py, since that regenerates products/*.html.
Safe to run repeatedly: the block between the share-tags markers is replaced.

    python tools/add-share-tags.py
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://noriko.in"
DEFAULT_IMAGE = "assets/img/share/noriko-share.jpg"
GA_ID = "G-V5WB7BP69N"  # Google Analytics 4: Ashokasha Exim account > NORIKO Website
SEARCH_CONSOLE = "sDDxuzAg_c3Ku_eTxL3InXbO6DQ7aLdJD_qW6IhNxU0"  # homepage only
GA_START, GA_END = "<!-- analytics -->", "<!-- /analytics -->"
GA_RE = re.compile(re.escape(GA_START) + r".*?" + re.escape(GA_END) + r"\n?", re.S)
START, END = "<!-- share-tags -->", "<!-- /share-tags -->"
BLOCK_RE = re.compile(re.escape(START) + r".*?" + re.escape(END) + r"\n?", re.S)


def page_url(rel):
    return SITE + "/" if rel == "index.html" else f"{SITE}/{rel}"


def absolute(src, rel):
    """Resolve an image path written relative to the page into a full URL."""
    src = src.split("?")[0]
    if src.startswith("http"):
        return src
    base = Path(rel).parent
    parts = []
    for part in (base / src).parts:
        if part == "..":
            parts.pop()
        elif part != ".":
            parts.append(part)
    return f"{SITE}/{'/'.join(parts)}"


def pick_image(text, rel):
    m = re.search(r'class="recipe-photo" src="([^"]+)"', text)
    if m:
        return absolute(m.group(1), rel)
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', text, re.S)
    if m:
        try:
            img = json.loads(m.group(1)).get("image")
            if isinstance(img, str):
                return absolute(img, rel)
        except ValueError:
            pass
    return f"{SITE}/{DEFAULT_IMAGE}"


def fix_ld_image(text, rel):
    """schema.org wants an absolute image URL, not a page-relative one."""
    def repl(m):
        try:
            data = json.loads(m.group(1))
        except ValueError:
            return m.group(0)
        img = data.get("image")
        if isinstance(img, str) and not img.startswith("http"):
            data["image"] = absolute(img, rel)
            return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'
        return m.group(0)
    return re.sub(r'<script type="application/ld\+json">(.*?)</script>', repl, text, flags=re.S)


def tags_for(text, rel):
    title = html.unescape(re.search(r"<title>(.*?)</title>", text, re.S).group(1).strip())
    m = re.search(r'<meta name="description" content="([^"]*)"', text)
    desc = html.unescape(m.group(1)) if m else ""
    is_product = rel.startswith("products/")
    is_recipe = rel.startswith("recipes/")
    url = page_url(rel)
    image = pick_image(text, rel)
    esc = lambda s: html.escape(s, quote=True)
    lines = [
        START,
        f'<link rel="canonical" href="{url}">',
        '<meta property="og:site_name" content="NORIKO">',
        f'<meta property="og:type" content="{"product" if is_product else "article" if is_recipe else "website"}">',
        f'<meta property="og:title" content="{esc(title)}">',
        f'<meta property="og:description" content="{esc(desc)}">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:image" content="{image}">',
        '<meta property="og:locale" content="en_IN">',
        '<meta name="twitter:card" content="summary_large_image">',
        END,
    ]
    return "\n".join(lines) + "\n"


LD_START, LD_END = "<!-- seo-data -->", "<!-- /seo-data -->"
LD_RE = re.compile(re.escape(LD_START) + r".*?" + re.escape(LD_END) + r"\n?", re.S)


def ld_script(data):
    body = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    return f'<script type="application/ld+json">{body}</script>'


def organization_ld():
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "NORIKO",
        "url": SITE + "/",
        "logo": f"{SITE}/assets/brand/icon-512.png",
        "sameAs": ["https://www.instagram.com/norikofoods/"],
        "parentOrganization": {"@type": "Organization", "name": "Ashokasha Exim Pvt. Ltd."},
        "contactPoint": [{
            "@type": "ContactPoint",
            "telephone": "+91-89282-27122",
            "contactType": "customer service",
            "areaServed": "IN",
            "availableLanguage": ["en", "hi"],
        }],
        "address": {"@type": "PostalAddress", "addressLocality": "Thane West", "addressRegion": "Maharashtra", "postalCode": "400604", "addressCountry": "IN"},
    }


def iso_minutes(n):
    return f"PT{n}M"


def recipe_ld(text, rel):
    strip = lambda s: html.unescape(re.sub(r"<[^>]+>", "", s)).strip()
    name = strip(re.search(r"<h1>(.*?)</h1>", text, re.S).group(1))
    lede = strip(re.search(r'<p class="lede">(.*?)</p>', text, re.S).group(1))
    diet = re.search(r'<p class="eyebrow">Recipe · (\w+)</p>', text)
    summary = re.search(r'<div class="recipe-summary">(.*?)</div>', text, re.S).group(1)
    ingredients = [strip(i) for i in re.findall(r"<li>(.*?)</li>", re.search(r'<ul class="recipe-ingredients">(.*?)</ul>', text, re.S).group(1), re.S)]
    method = re.search(r'<div class="recipe-method" id="method">(.*?)(?:<div class="recipe-note">|<div class="recipe-products">|$)', text, re.S).group(1)
    steps = []
    for li in re.findall(r"<li>(.*?)</li>", method, re.S):
        m = re.match(r"\s*<strong>(.*?)</strong>\s*(.*)", li, re.S)
        steps.append({"@type": "HowToStep", "name": strip(m.group(1)), "text": strip(m.group(2))} if m else {"@type": "HowToStep", "text": strip(li)})
    data = {
        "@context": "https://schema.org",
        "@type": "Recipe",
        "name": name,
        "description": lede,
        "image": pick_image(text, rel),
        "author": {"@type": "Organization", "name": "NORIKO"},
        "publisher": {"@type": "Organization", "name": "NORIKO"},
        "recipeCuisine": "Asian",
        "recipeIngredient": ingredients,
        "recipeInstructions": steps,
        "mainEntityOfPage": page_url(rel),
    }
    if diet:
        data["suitableForDiet"] = "https://schema.org/VeganDiet" if diet.group(1) == "Vegan" else "https://schema.org/VegetarianDiet"
    prep = re.search(r"Prep (\d+) min", summary)
    cook = re.search(r"Cook (\d+) min", summary)
    if prep:
        data["prepTime"] = iso_minutes(int(prep.group(1)))
    if cook:
        data["cookTime"] = iso_minutes(int(cook.group(1)))
    if prep and cook:
        data["totalTime"] = iso_minutes(int(prep.group(1)) + int(cook.group(1)))
    serves = re.search(r"(?:Serves|Makes) (\d+)", summary)
    if serves:
        data["recipeYield"] = serves.group(0).split(" ", 1)[1]
    return data


def faq_ld(text):
    qa = re.findall(r'<summary>(.*?)</summary><p>(.*?)</p>', text, re.S)
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": html.unescape(q), "acceptedAnswer": {"@type": "Answer", "text": html.unescape(a)}}
            for q, a in qa
        ],
    }


def seo_data_block(text, rel):
    if rel == "horeca.html":
        return f"{LD_START}\n{ld_script(faq_ld(text))}\n{LD_END}\n"
    if rel == "index.html":
        data = organization_ld()
    elif rel.startswith("recipes/"):
        data = recipe_ld(text, rel)
    else:
        return ""
    return f"{LD_START}\n{ld_script(data)}\n{LD_END}\n"


def analytics_block(rel):
    lines = [GA_START]
    if rel == "index.html":
        lines.append(f'<meta name="google-site-verification" content="{SEARCH_CONSOLE}">')
    lines += [
        f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>',
        f"<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA_ID}');</script>",
        GA_END,
    ]
    return "\n".join(lines) + "\n"


def add_analytics(text, rel):
    text = GA_RE.sub("", text)
    i = text.index("</head>")
    return text[:i] + analytics_block(rel) + text[i:]


def main():
    pages = sorted(
        p for p in ROOT.rglob("*.html")
        if not any(part in {".git", "design-system", "tools", "private", "netlify"} for part in p.relative_to(ROOT).parts)
    )
    urls = []
    for path in pages:
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        if "<title>" not in text:
            continue
        text = add_analytics(text, rel)
        if rel == "404.html":
            path.write_text(text, encoding="utf-8")
            continue
        text = BLOCK_RE.sub("", text)
        text = LD_RE.sub("", text)
        text = fix_ld_image(text, rel)
        block = tags_for(text, rel)
        m = re.search(r'<meta name="description"[^>]*>\n', text)
        anchor = m.end() if m else text.index("</title>") + len("</title>\n")
        text = text[:anchor] + block + seo_data_block(text, rel) + text[anchor:]
        path.write_text(text, encoding="utf-8")
        urls.append(page_url(rel))
        print(rel)

    entries = "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls)
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{entries}</urlset>\n",
        encoding="utf-8",
    )
    print(f"sitemap.xml: {len(urls)} pages")


if __name__ == "__main__":
    main()
