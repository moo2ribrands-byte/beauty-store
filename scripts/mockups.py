"""Product mockups: illustrated packs drawn to match each product's real US packaging.

  python3 scripts/mockups.py          -> writes img/p/<sku>.svg for every product in designs.py
  python3 scripts/mockups.py preview  -> also writes scripts/_preview.html, a sheet of all of them

They're illustrations, not photos: brand names are set as plain text and no logo artwork is copied.
A photo uploaded in Manage shop always replaces the mockup on the site.
Then run python3 scripts/build.py so the page knows which products have a mockup.
"""
import os, sys, json, glob
from designs import D

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "img", "p")


def build(preview=False):
    os.makedirs(OUT, exist_ok=True)
    for f in glob.glob(os.path.join(OUT, "*.svg")):
        os.remove(f)
    for sku, fn in D.items():
        open(os.path.join(OUT, sku.lower() + ".svg"), "w").write(fn().svg())
    if preview:
        seed = {p["sku"]: p for p in json.load(open(os.path.join(HERE, "seed.json")))}
        cells = "".join(
            f'<figure style="background:{seed[k]["c"][4] if k in seed else "#eee"}"><img src="../img/p/{k.lower()}.svg">'
            f'<figcaption>{k}</figcaption></figure>' for k in D)
        open(os.path.join(HERE, "_preview.html"), "w").write(
            '<style>body{margin:0;display:grid;grid-template-columns:repeat(8,1fr);gap:6px;font:10px Arial;background:#fff}'
            'figure{margin:0;padding:12px 12px 4px;aspect-ratio:5/6;display:flex;flex-direction:column}'
            'img{flex:1;min-height:0;object-fit:contain}</style>' + cells)
    return list(D)


if __name__ == "__main__":
    print(len(build("preview" in sys.argv)), "mockups")
