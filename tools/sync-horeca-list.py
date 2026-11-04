"""Copy the HoReCa product list + enquiry basket from index.html into horeca.html.

The list is maintained once, in index.html, between the horeca-list markers.
Run this after editing it:

    python tools/sync-horeca-list.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLOCK = re.compile(r"( *<!-- horeca-list[^>]*-->\n)(.*?)( *<!-- /horeca-list -->)", re.S)

source = BLOCK.search((ROOT / "index.html").read_text(encoding="utf-8")).group(2)
target_path = ROOT / "horeca.html"
target = target_path.read_text(encoding="utf-8")
target = BLOCK.sub(lambda m: m.group(1) + source + m.group(3), target, count=1)
target_path.write_text(target, encoding="utf-8")
print("horeca.html: product list synced")
