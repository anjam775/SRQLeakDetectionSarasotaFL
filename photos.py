#!/usr/bin/env python3
"""Pexels photos for home, service and location pages.
Downloads each photo from images.pexels.com (free Pexels license), crops to 16:9 and
writes static/public/assets/img/pages/<name>.webp (1200x675) and <name>-600.webp.
Credits live in content/figures.py and are shown in each caption."""
import os, io, urllib.request
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "static", "public", "assets", "img", "pages")
CACHE = os.path.join(ROOT, "photos-src")

# name: (pexels id, vertical focus 0=top 0.5=center 1=bottom)
PHOTOS = {
    "home-leak": (18274115, 0.5),
    "home-meter": (11658940, 0.5),
    "home-sarasota": (31836358, 0.6),
    "svc-water-service-line-repair": (29274530, 0.5),
    "svc-water-line-replacement": (13791255, 0.45),
    "svc-slab-leak-repair": (17395035, 0.55),
    "svc-underground-leak-detection": (4406597, 0.5),
    "svc-emergency-water-line-repair": (7616004, 0.5),
    "svc-repiping": (28169591, 0.5),
    "svc-sewer-line-repair": (37627673, 0.6),
    "svc-pool-leak-detection": (261238, 0.55),
    "loc-bradenton": (5278888, 0.55),
    "loc-lakewood-ranch": (32270936, 0.5),
    "loc-longboat-key": (31790256, 0.5),
    "loc-nokomis": (28437165, 0.55),
    "loc-north-port": (15334546, 0.5),
    "loc-osprey": (37485059, 0.5),
    "loc-siesta-key": (16403226, 0.5),
    "loc-venice": (15764620, 0.5),
}

def fetch(pid):
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, f"{pid}.jpg")
    if not os.path.exists(path):
        url = f"https://images.pexels.com/photos/{pid}/pexels-photo-{pid}.jpeg?auto=compress&cs=tinysrgb&w=1600"
        with urllib.request.urlopen(url, timeout=60) as r:
            open(path, "wb").write(r.read())
    return Image.open(path).convert("RGB")

def crop169(im, fy):
    w, h = im.size
    if w / h > 16 / 9:
        nw = int(h * 16 / 9); x = (w - nw) // 2
        return im.crop((x, 0, x + nw, h))
    nh = int(w * 9 / 16); y = int((h - nh) * fy)
    return im.crop((0, y, w, y + nh))

def main():
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        os.remove(os.path.join(OUT, f))
    for name, (pid, fy) in PHOTOS.items():
        im = crop169(fetch(pid), fy)
        big = im.resize((1200, 675), Image.LANCZOS)
        for q in (78, 72, 66, 60, 55, 50, 45, 40):  # keep each file under 180 KB
            buf = io.BytesIO(); big.save(buf, "WEBP", quality=q, method=6)
            if buf.tell() < 180_000: break
        open(os.path.join(OUT, f"{name}.webp"), "wb").write(buf.getvalue())
        im.resize((600, 338), Image.LANCZOS).save(os.path.join(OUT, f"{name}-600.webp"), "WEBP", quality=76, method=6)
    print(f"{len(PHOTOS)} photos -> {OUT}")

if __name__ == "__main__":
    main()
