"""Check local page, asset and fragment links in the static site."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
SKIP = ("http://", "https://", "mailto:", "tel:", "javascript:", "data:")


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        for key in ("href", "src"):
            if attrs.get(key):
                self.links.append(attrs[key])


pages = {}
for page in ROOT.rglob("*.html"):
    if "chrome-qa-profile" in page.parts:
        continue
    parsed = Links()
    parsed.feed(page.read_text(encoding="utf-8"))
    pages[page.resolve()] = parsed

errors = []
for page, parsed in pages.items():
    for raw in parsed.links:
        if raw.startswith(SKIP):
            continue
        parts = urlsplit(raw)
        target = (page.parent / unquote(parts.path)).resolve() if parts.path else page
        if not target.exists():
            errors.append(f"{page.relative_to(ROOT)}: missing {raw}")
            continue
        if parts.fragment and target.suffix.lower() == ".html":
            target_page = pages.get(target)
            if target_page and parts.fragment not in target_page.ids:
                errors.append(f"{page.relative_to(ROOT)}: missing fragment {raw}")

if errors:
    print("\n".join(errors))
    raise SystemExit(1)
print(f"Checked {len(pages)} HTML pages: all local links and fragments resolve.")
