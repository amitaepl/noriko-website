#!/usr/bin/env python3
"""Rebuild _redirects: every extensionless page address redirects (301, forced) to its .html page.
Run after adding or removing a page in /, products/ or recipes/."""
import glob, os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
rows = [('/index.html', '/')]
for p in ['about', 'retail', 'horeca', 'recipes', 'privacy', 'terms']:
    rows.append(('/' + p, '/' + p + '.html'))
for d in ['products', 'recipes']:
    for f in sorted(glob.glob(d + '/*.html')):
        slug = os.path.basename(f)[:-5]
        rows.append((f'/{d}/{slug}', f'/{d}/{slug}.html'))
head = '\n'.join(l for l in open('_redirects').read().split('\n') if l.startswith('#')) if os.path.exists('_redirects') else ''
w = max(len(a) for a, _ in rows) + 2
body = '\n'.join(f'{a.ljust(w)}{b}  301!' for a, b in rows)
open('_redirects', 'w').write(head + '\n' + body + '\n\n/private/*  /index.html  404\n')
print(len(rows), 'rules written')
