# -*- coding: utf-8 -*-
"""
Check every local href/src in the site resolves, and that in-page anchors exist.

    python tools/check-links.py

Exits non-zero if anything is broken, so it can gate a commit.
"""
import glob
import os
import posixpath
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = sorted(glob.glob("index.html") + glob.glob("retail.html") +
               glob.glob("products/*.html"))

ASSET_RE = re.compile(r"\.(webp|png|jpe?g|svg|ico|css|js|json|pdf)$", re.I)
REF_RE = re.compile(r'(?:src|href)="([^"]+)"')
ID_RE = re.compile(r'\sid="([^"]+)"')


def ids_in(path):
    return set(ID_RE.findall(open(path, encoding="utf-8").read()))


def main():
    os.chdir(ROOT)
    missing, bad_anchor, placeholder = [], [], []
    id_cache = {}

    for page in PAGES:
        base = os.path.dirname(page)
        src = open(page, encoding="utf-8").read()

        for ref in REF_RE.findall(src):
            if ref.startswith(("http://", "https://", "mailto:", "tel:", "data:")):
                continue
            if ref == "#":
                placeholder.append((page, ref))
                continue

            path, _, frag = ref.partition("#")
            if path:
                clean = path.split("?")[0]
                target = posixpath.normpath(posixpath.join(base.replace(os.sep, "/"), clean))
                if not os.path.exists(target):
                    missing.append((page, ref))
                    continue
            else:
                target = page

            if frag:
                if target not in id_cache:
                    id_cache[target] = ids_in(target) if target.endswith(".html") else set()
                if frag not in id_cache[target]:
                    bad_anchor.append((page, ref))

    def report(title, rows):
        print("%s: %d" % (title, len(rows)))
        for page, ref in rows[:15]:
            print("    %s  ->  %s" % (page, ref))
        if len(rows) > 15:
            print("    ... and %d more" % (len(rows) - 15))

    print("pages checked: %d" % len(PAGES))
    report("missing targets", missing)
    report("dead anchors", bad_anchor)
    report('placeholder href="#" (expected where content is not written yet)', placeholder)

    return 1 if (missing or bad_anchor) else 0


if __name__ == "__main__":
    sys.exit(main())
