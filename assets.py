#!/usr/bin/env python3
"""Generate static/public: CSS/JS, logos, icons, manifest, OG + blog images, Cloudflare files."""
import os, re, sys, io, importlib, textwrap
import cairosvg
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.join(ROOT, "static", "public")
sys.path.insert(0, os.path.join(ROOT, "content"))
from data import SITE

def w(path, data, mode="w"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, mode) as f:
        f.write(data)

def mincss(s):
    s = re.sub(r"/\*.*?\*/", "", s, flags=re.S)
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"\s*([{};:,>])\s*", r"\1", s)
    return s.replace(";}", "}").strip()

def minjs(s):
    return "\n".join(l.strip() for l in s.splitlines() if l.strip())

# --- CSS / JS
w(f"{ROOT}/static/site.min.css", mincss(open(f"{ROOT}/static/site.css").read()))
w(f"{ROOT}/static/critical.min.css", mincss(open(f"{ROOT}/static/critical.css").read()))
w(f"{PUB}/assets/js/site.js", minjs(open(f"{ROOT}/static/site.js").read()))

# --- Logos
MARK = ('<rect width="48" height="48" rx="11" fill="#0B2545"/>'
        '<path d="M22 9c-5.5 7.3-9 12.4-9 17a9 9 0 0 0 13.5 7.8" fill="none" stroke="#5EEAD4" stroke-width="4" stroke-linecap="round"/>'
        '<circle cx="28" cy="27" r="7" fill="none" stroke="#F59E0B" stroke-width="4"/>'
        '<path d="M33 32l6 6" stroke="#F59E0B" stroke-width="4.5" stroke-linecap="round"/>')
icon_svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48">{MARK}</svg>'
horiz_svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 260 56" role="img" aria-label="SRQ Leak Pros">'
             f'<g transform="translate(4 4)">{MARK}</g>'
             '<text x="64" y="38" font-family="Inter,Segoe UI,Arial,sans-serif" font-size="26" fill="#0B2545">'
             '<tspan font-weight="800">SRQ</tspan><tspan font-weight="600" dx="6">Leak Pros</tspan></text></svg>')
horiz_dark = horiz_svg.replace('fill="#0B2545">', 'fill="#FFFFFF">', 1)
w(f"{PUB}/favicon.svg", icon_svg)
w(f"{PUB}/assets/img/logo-icon.svg", icon_svg)
w(f"{PUB}/assets/img/logo-horizontal.svg", horiz_svg)
w(f"{PUB}/assets/img/logo-horizontal-light.svg", horiz_dark)

def png(svg, size):
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode(), output_width=size, output_height=size))).convert("RGBA")

for size, name in [(180, "apple-touch-icon.png"), (192, "assets/img/icon-192.png"), (512, "assets/img/icon-512.png"), (512, "assets/img/logo-512.png")]:
    img = png(icon_svg, size)
    if name == "apple-touch-icon.png":
        bg = Image.new("RGBA", img.size, "#0B2545"); bg.alpha_composite(img); img = bg.convert("RGB")
    os.makedirs(os.path.dirname(f"{PUB}/{name}"), exist_ok=True)
    img.save(f"{PUB}/{name}", optimize=True)
# maskable icon with safe padding
mk = Image.new("RGBA", (512, 512), "#0B2545"); mk.alpha_composite(png(icon_svg, 360), (76, 76)); mk.save(f"{PUB}/assets/img/icon-maskable-512.png", optimize=True)
png(icon_svg, 64).save(f"{PUB}/favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])

w(f"{PUB}/site.webmanifest", ('{"name":"SRQ Leak Pros","short_name":"SRQ Leak Pros","start_url":"/","display":"standalone",'
  '"background_color":"#ffffff","theme_color":"#0B2545","icons":[{"src":"/assets/img/icon-192.png","sizes":"192x192","type":"image/png"},'
  '{"src":"/assets/img/icon-512.png","sizes":"512x512","type":"image/png"},'
  '{"src":"/assets/img/icon-maskable-512.png","sizes":"512x512","type":"image/png","purpose":"maskable"}]}'))

# --- Cloudflare files
w(f"{PUB}/_headers", """/*
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=()
  Strict-Transport-Security: max-age=31536000; includeSubDomains
  Content-Security-Policy: default-src 'self'; script-src 'self' https://www.googletagmanager.com; style-src 'self' 'unsafe-inline'; img-src 'self' data: https://*.google-analytics.com https://*.googletagmanager.com; font-src 'self'; connect-src 'self' https://*.google-analytics.com https://*.analytics.google.com https://*.googletagmanager.com; frame-ancestors 'none'; base-uri 'self'; form-action 'self'; upgrade-insecure-requests
  Cache-Control: public, max-age=0, must-revalidate

/assets/*
  Cache-Control: public, max-age=31536000, immutable

/favicon.ico
  Cache-Control: public, max-age=604800
/favicon.svg
  Cache-Control: public, max-age=604800
/apple-touch-icon.png
  Cache-Control: public, max-age=604800
/site.webmanifest
  Cache-Control: public, max-age=86400
/sitemap.xml
  Cache-Control: public, max-age=3600
""")
w(f"{PUB}/_redirects", """# Cloudflare Pages serves folder/index.html at /folder/ and adds the trailing slash itself.
# Legacy / alternate paths
/home                       /                       301
/service/*                  /services/:splat        301
/location/*                 /locations/:splat       301
/areas/*                    /locations/:splat       301
/posts/*                    /blog/:splat            301
/privacy                    /privacy-policy/        301
/terms-of-service           /terms/                 301
/services/slab-leak-detection/       /services/slab-leak-repair/            301
/services/water-line-repair/         /services/water-service-line-repair/   301
/services/main-water-line-replacement/ /services/water-line-replacement/    301
""")

# --- Images (OG default + blog featured)
FB = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"
FS = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"

def base_canvas():
    im = Image.new("RGB", (1200, 630), "#0B2545")
    d = ImageDraw.Draw(im)
    for x in range(1200):  # diagonal-ish gradient
        c = int(0x25 + (0x4e - 0x25) * x / 1200)
        d.line([(x, 0), (x, 630)], fill=(11, c, 69 + int(42 * x / 1200)))
    # water ripple accents
    for r, a in [(260, 40), (200, 55), (140, 70)]:
        d.ellipse([1200 - 180 - r, 630 - 120 - r, 1200 - 180 + r, 630 - 120 + r], outline=(94, 234, 212), width=3)
    logo = png(icon_svg, 84)
    im.paste(logo, (64, 470), logo)
    d.text((166, 492), "SRQ Leak Pros", font=ImageFont.truetype(FB, 38), fill="#FFFFFF")
    return im, d

def wrap_text(d, text, font, width):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if d.textlength(t, font=font) <= width:
            cur = t
        else:
            lines.append(cur); cur = wd
    lines.append(cur)
    return lines

def make_img(title, label, out):
    im, d = base_canvas()
    d.rounded_rectangle([64, 60, 64 + int(d.textlength(label.upper(), font=ImageFont.truetype(FS, 24))) + 36, 106], radius=22, fill="#F59E0B")
    d.text((82, 68), label.upper(), font=ImageFont.truetype(FS, 24), fill="#0B2545")
    size = 64
    while True:
        f = ImageFont.truetype(FB, size)
        lines = wrap_text(d, title, f, 1000)
        if len(lines) <= 4 or size <= 44:
            break
        size -= 4
    y = 140
    for ln in lines:
        d.text((64, y), ln, font=f, fill="#FFFFFF"); y += int(size * 1.18)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    im.save(out + ".jpg", "JPEG", quality=82, optimize=True, progressive=True)
    im.save(out + ".webp", "WEBP", quality=80, method=6)
    im.resize((600, 315), Image.LANCZOS).save(out + "-600.webp", "WEBP", quality=78, method=6)

make_img("Leak Detection & Water Line Help in Sarasota, FL", "Sarasota & nearby areas", f"{PUB}/assets/img/og-default"); [os.remove(f"{PUB}/assets/img/og-default{x}") for x in (".webp", "-600.webp")]

if __name__ == "__main__":
    mods = [importlib.import_module(m) for m in ("posts_a", "posts_b", "posts_c", "posts_d", "posts_e")]
    for m in mods:
        for p in m.PAGES:
            if p["type"] == "post":
                from data import POSTS
                cat = next(x["cat"] for x in POSTS if x["slug"] == p["slug"])
                make_img(p["h1"], cat, f"{PUB}/assets/img/blog/{p['slug']}")
    print("assets done")
