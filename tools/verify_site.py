#!/usr/bin/env python3
"""Pre-deploy checks for the built site:  python3 tools/verify_site.py _site

Exits non-zero if any check fails. No third-party dependencies.
"""
import json, os, re, sys

if len(sys.argv) > 1:
    if not os.path.isdir(sys.argv[1]):
        print(f"FAIL — no such directory: {sys.argv[1]}")
        sys.exit(1)
    os.chdir(sys.argv[1])

BASE = "https://miamipeculiar.com/"
CATALOG = "https://studio-lab-nodarse.github.io/studio-lab-catalog/"   # the live catalog, a different site
ORDER_EMAIL = "jesusnodarse1823@gmail.com"
WHATSAPP = "17864834268"
PAGES = {"index.html": ("en", ""), "es/index.html": ("es", "es/")}     # file -> (lang, URL path)
PAGE_SIZE_BUDGET = 150 * 1024
IMAGE_SIZE_BUDGET = 400 * 1024
FIELDS = ["store", "name", "phone", "zip", "email", "custom", "_honey"]
PANELS = ["form", "outside", "net", "already", "done", "doneout"]
PLACEHOLDERS = ["undefined", "NaN", "{{", "[object", "$ ", "Sunny Days Gifts"]

errors = []
def err(m): errors.append(m)
def read(p):
    with open(p, encoding="utf-8", errors="replace") as f:
        return f.read()

for p, (lang, path) in PAGES.items():
    if not os.path.isfile(p):
        err(f"[missing-page] {p}")
        continue
    s = read(p)
    up = "../" if "/" in p else ""
    body = re.sub(r"<(script|style)\b.*?</\1>", "", s, flags=re.S)

    # size, images
    if os.path.getsize(p) > PAGE_SIZE_BUDGET:
        err(f"[size] {p} exceeds {PAGE_SIZE_BUDGET // 1024}KB")
    if re.search(r"data:image/(?:jpeg|jpg|png|webp|gif);base64,", s):
        err(f"[base64] {p} has an inline raster image; put it in assets/img/")

    # SEO + language
    for need in [f'<html lang="{lang}"', f'<link rel="canonical" href="{BASE}{path}">', 'hreflang="en"', 'hreflang="es"',
                 'hreflang="x-default"', 'property="og:title"', 'name="description"']:
        if need not in s:
            err(f"[seo] {p} missing {need}")
    for tag in ["<title>", "<h1"]:
        if s.count(tag) != 1:
            err(f"[seo] {p} has {s.count(tag)} {tag} (want 1)")
    for i, block in enumerate(re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)):
        try:
            json.loads(block)
        except Exception as e:
            err(f"[jsonld] {p} block {i}: {e}")

    # every local file resolves; every #anchor exists; no dead anchors
    for m in set(re.findall(r'(?:src|srcset|href)="((?:\.\./)?assets/[^"]+)"', s)) | set(re.findall(r'url\("((?:\.\./)?assets/[^"]+)"\)', s)):
        if not os.path.isfile(os.path.normpath(os.path.join(os.path.dirname(p), m))):
            err(f"[asset] {p} -> {m} (missing)")
    ids = set(re.findall(r'\sid="([^"]+)"', s))
    for a in set(re.findall(r'href="#([^"]*)"', s)):
        if a not in ids:
            err(f"[anchor] {p} -> #{a}")
    for u in set(re.findall(re.escape(BASE) + r"[^\"'\s<>)]*", s)):
        f = u[len(BASE):].split("#")[0].split("?")[0]
        f = os.path.join(f, "index.html") if f == "" or f.endswith("/") else f
        if not os.path.isfile(f):
            err(f"[url] {p} -> {u} (no file {f})")
    for href in [CATALOG, CATALOG + "apps/storefront/"]:
        if f'href="{href}"' not in s:
            err(f"[link] {p} does not link {href}")

    # contact channels
    if f"mailto:{ORDER_EMAIL}" not in s:
        err(f"[contact] {p} has no mailto:{ORDER_EMAIL}")
    for n in set(re.findall(r"wa\.me/(\d+)", s)):
        if n != WHATSAPP:
            err(f"[contact] {p} -> wa.me/{n} (want {WHATSAPP})")

    # form wiring
    for f in FIELDS:
        if f'name="{f}"' not in s:
            err(f"[form] {p} is missing the {f} field")
    for f in PANELS:
        if f'data-panel="{f}"' not in s:
            err(f"[form] {p} is missing the {f} state")
    if not re.search(r'data-zip-min="\d{5}" data-zip-max="\d{5}"', s):
        err(f"[form] {p} has no Florida ZIP range")
    for js in ["submit.js", "trial.js"]:
        if f'<script src="{up}assets/{js}"></script>' not in s:
            err(f"[form] {p} does not load assets/{js}")
    if "formsubmit.co" in s:
        err(f"[form] {p} carries a FormSubmit endpoint; it lives only in assets/submit.js")

    # nothing empty or fake leaked into the page; external scripts pinned
    for bad in PLACEHOLDERS:
        if bad in body:
            err(f"[placeholder] {p} contains {bad!r}")
    for tag in re.findall(r'<script\b[^>]*\bsrc="https?://[^"]+"[^>]*>', s):
        if "integrity=" not in tag:
            err(f"[sri] {p} loads an external script without integrity: {tag[:90]}…")

if os.path.isfile("assets/submit.js"):
    js = read("assets/submit.js")
    if f"formsubmit.co/ajax/{ORDER_EMAIL}" not in js or "window.mpSubmit" not in js:
        err("[form] assets/submit.js must expose mpSubmit and post to ORDER_EMAIL")
else:
    err("[form] missing assets/submit.js")
if os.path.isfile("assets/trial.js") and "formsubmit.co" in read("assets/trial.js"):
    err("[form] assets/trial.js must not carry a FormSubmit endpoint")

for f in os.listdir("assets/img"):
    if os.path.getsize(f"assets/img/{f}") > IMAGE_SIZE_BUDGET:
        err(f"[size] assets/img/{f} exceeds {IMAGE_SIZE_BUDGET // 1024}KB")
for a in ["robots.txt", "sitemap.xml", "404.html", ".nojekyll", "assets/favicon.png", "assets/apple-touch-icon.png", "assets/og/default.jpg"]:
    if not os.path.isfile(a):
        err(f"[ops] missing {a}")
sm = read("sitemap.xml") if os.path.isfile("sitemap.xml") else ""
for _, path in PAGES.values():
    if f"<loc>{BASE}{path}</loc>" not in sm:
        err(f"[sitemap] missing {BASE}{path}")

if errors:
    print(f"FAIL — {len(errors)} issue(s):")
    for e in errors:
        print("  " + e)
    sys.exit(1)
print(f"OK — {len(PAGES)} pages checked, all invariants hold.")
