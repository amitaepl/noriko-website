"""Add canonical + Open Graph / Twitter share tags to every page, and write sitemap.xml.

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


def main():
    pages = sorted(
        p for p in ROOT.rglob("*.html")
        if not any(part in {".git", "design-system", "tools", "private", "netlify"} for part in p.relative_to(ROOT).parts)
    )
    urls = []
    for path in pages:
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        if "<title>" not in text or rel == "404.html":
            continue
        text = BLOCK_RE.sub("", text)
        text = fix_ld_image(text, rel)
        block = tags_for(text, rel)
        m = re.search(r'<meta name="description"[^>]*>\n', text)
        anchor = m.end() if m else text.index("</title>") + len("</title>\n")
        text = text[:anchor] + block + text[anchor:]
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
