#!/usr/bin/env python3
"""Original flat illustrations for home, service and location pages.
Writes static/public/assets/img/pages/<name>.webp (1200x675) and <name>-600.webp.
All artwork is drawn from simple shapes here; no photos or third-party art."""
import os, io, random
import cairosvg
from PIL import Image
from html import escape as esc

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "static", "public", "assets", "img", "pages")
W, H = 1200, 675
NAVY, NAVY2, TEAL, TEALD, AQUA, MINT, AMBER = "#0B2545", "#13315C", "#0E7490", "#0B5E73", "#E8F6F7", "#5EEAD4", "#F59E0B"
WATER, PIPE_B, PIPE_R, SOIL, SOIL2, GRASS = "#38BDF8", "#2563EB", "#DC2626", "#D9B98A", "#C49A6C", "#6FBF73"
FONT = "DejaVu Sans, Arial, sans-serif"

# ------------------------------------------------------------------ primitives
def defs():
    return f'''<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#CFEFF3"/><stop offset="1" stop-color="#F7FCFD"/></linearGradient>
<linearGradient id="soil" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{SOIL}"/><stop offset="1" stop-color="{SOIL2}"/></linearGradient>
<linearGradient id="sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5BC0DE"/><stop offset="1" stop-color="#2A8FB8"/></linearGradient>
<linearGradient id="pool" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7DD3FC"/><stop offset="1" stop-color="#0EA5E9"/></linearGradient>
<linearGradient id="night" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#13315C"/><stop offset="1" stop-color="#1E4E79"/></linearGradient>
</defs>'''

def svg(body, bg="url(#sky)"):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{defs()}<rect width="{W}" height="{H}" fill="{bg}"/>{body}</svg>'

def sun(x=1060, y=95, r=46):
    return f'<circle cx="{x}" cy="{y}" r="{r+18}" fill="#FDE68A" opacity=".35"/><circle cx="{x}" cy="{y}" r="{r}" fill="#FCD34D"/>'

def cloud(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})" fill="#fff" opacity=".95"><ellipse cx="0" cy="0" rx="58" ry="22"/>'
            f'<ellipse cx="-34" cy="6" rx="34" ry="18"/><ellipse cx="38" cy="6" rx="40" ry="18"/><ellipse cx="6" cy="-14" rx="34" ry="22"/></g>')

def ground(y, x0=0, x1=W, seed=1, bottom=H):
    rnd = random.Random(seed)
    dots = "".join(f'<circle cx="{rnd.uniform(x0, x1):.0f}" cy="{rnd.uniform(y+26, bottom-6):.0f}" r="{rnd.uniform(1.5, 3.2):.1f}" fill="#B88A5A" opacity=".55"/>' for _ in range(int((x1-x0)/9)))
    return (f'<rect x="{x0}" y="{y}" width="{x1-x0}" height="{bottom-y}" fill="url(#soil)"/>{dots}'
            f'<rect x="{x0}" y="{y-10}" width="{x1-x0}" height="16" rx="3" fill="{GRASS}"/>'
            f'<rect x="{x0}" y="{y+4}" width="{x1-x0}" height="4" fill="#5AA35E" opacity=".6"/>')

def house(x, yg, w=300, h=170, wall="#FFFFFF", roof=NAVY, style="gable", door="#0E7490", win=True):
    out = f'<rect x="{x}" y="{yg-h}" width="{w}" height="{h}" fill="{wall}" stroke="#CBD5E1" stroke-width="3"/>'
    if style == "gable":
        out += f'<polygon points="{x-22},{yg-h+4} {x+w/2},{yg-h-92} {x+w+22},{yg-h+4}" fill="{roof}"/>'
    elif style == "hip":
        out += f'<polygon points="{x-20},{yg-h+4} {x+w*0.22},{yg-h-62} {x+w*0.78},{yg-h-62} {x+w+20},{yg-h+4}" fill="{roof}"/>'
    elif style == "tile":
        out += f'<polygon points="{x-20},{yg-h+4} {x+w*0.2},{yg-h-52} {x+w*0.8},{yg-h-52} {x+w+20},{yg-h+4}" fill="#C2410C"/>'
        out += "".join(f'<line x1="{x-10+i*22}" y1="{yg-h+2}" x2="{x+w*0.2+i*14}" y2="{yg-h-50}" stroke="#9A3412" stroke-width="2" opacity=".5"/>' for i in range(int(w/22)) if x+w*0.2+i*14 < x+w*0.8)
    elif style == "flat":
        out += f'<rect x="{x-12}" y="{yg-h-14}" width="{w+24}" height="18" fill="{roof}"/>'
    dw = 46
    out += f'<rect x="{x+w*0.44}" y="{yg-84}" width="{dw}" height="84" rx="4" fill="{door}"/><circle cx="{x+w*0.44+dw-10}" cy="{yg-42}" r="3.5" fill="#FDE68A"/>'
    if win:
        for wx in (x+w*0.12, x+w*0.7):
            out += f'<rect x="{wx}" y="{yg-h+40}" width="58" height="50" rx="4" fill="#BAE6FD" stroke="{NAVY2}" stroke-width="3"/><line x1="{wx+29}" y1="{yg-h+40}" x2="{wx+29}" y2="{yg-h+90}" stroke="{NAVY2}" stroke-width="2"/>'
    return out

def palm(x, yg, h=190, lean=18):
    tx, ty = x + lean, yg - h
    trunk = f'<path d="M{x-7},{yg} Q{x+lean*0.4},{yg-h*0.5} {tx-4},{ty} L{tx+5},{ty} Q{x+lean*0.4+12},{yg-h*0.5} {x+9},{yg} Z" fill="#A16207"/>'
    rings = "".join(f'<line x1="{x+lean*(i/8)-8}" y1="{yg-h*(i/8)}" x2="{x+lean*(i/8)+9}" y2="{yg-h*(i/8)-3}" stroke="#854D0E" stroke-width="2"/>' for i in range(1, 8))
    fr = ""
    for ang, ln in ((-160, 95), (-120, 85), (-60, 90), (-20, 95), (-90, 70), (200, 70), (-200, 0)):
        if ln == 0: continue
        fr += f'<path d="M{tx},{ty} q{ln*0.5},{-34} {ln},{8} q{-ln*0.45},{-10} {-ln},{-8}" fill="#16A34A" transform="rotate({ang+90} {tx} {ty})"/>'
    return trunk + rings + fr + f'<circle cx="{tx}" cy="{ty+4}" r="8" fill="#713F12"/>'

def shrub(x, yg, r=26, c="#22A04B"):
    return f'<circle cx="{x-r*0.6}" cy="{yg-r*0.6}" r="{r*0.75}" fill="{c}"/><circle cx="{x+r*0.6}" cy="{yg-r*0.6}" r="{r*0.75}" fill="{c}"/><circle cx="{x}" cy="{yg-r}" r="{r}" fill="{c}"/>'

def pipe(pts, color=PIPE_B, w=16, outline=True):
    d = " ".join(f"{'M' if i == 0 else 'L'}{x},{y}" for i, (x, y) in enumerate(pts))
    o = f'<path d="{d}" fill="none" stroke="#0F172A" stroke-opacity=".25" stroke-width="{w+6}" stroke-linejoin="round" stroke-linecap="round"/>' if outline else ""
    return o + f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"/><path d="{d}" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="{max(2, w//4)}" stroke-linejoin="round" stroke-linecap="round" transform="translate(0 -{w//4})"/>'

def leak(x, y, s=1.0):
    drops = "".join(f'<path d="M{x+dx},{y+dy-12*s} q{7*s},{10*s} 0,{16*s} q{-7*s},{-6*s} 0,{-16*s}Z" fill="{WATER}"/>' for dx, dy in ((-26*s, -8*s), (24*s, -14*s), (2*s, -30*s), (-8*s, 22*s), (30*s, 16*s)))
    rings = "".join(f'<ellipse cx="{x}" cy="{y}" rx="{r*s}" ry="{r*0.55*s}" fill="none" stroke="{WATER}" stroke-width="3" opacity="{op}"/>' for r, op in ((26, .9), (44, .6), (64, .35)))
    return f'<ellipse cx="{x}" cy="{y}" rx="{70*s}" ry="{40*s}" fill="{WATER}" opacity=".18"/>' + rings + drops

def waves(x, y, up=True, n=3, color=AMBER):
    sgn = -1 if up else 1
    return "".join(f'<path d="M{x-18-i*16},{y+sgn*(10+i*16)} Q{x},{y+sgn*(28+i*22)} {x+18+i*16},{y+sgn*(10+i*16)}" fill="none" stroke="{color}" stroke-width="4" stroke-linecap="round" opacity="{1-i*0.25}"/>' for i in range(n))

def meterbox(x, yg):
    return (f'<rect x="{x-38}" y="{yg-6}" width="76" height="62" rx="6" fill="#64748B"/><rect x="{x-42}" y="{yg-14}" width="84" height="14" rx="4" fill="#334155"/>'
            f'<circle cx="{x}" cy="{yg+26}" r="16" fill="#E2E8F0" stroke="{NAVY}" stroke-width="3"/><path d="M{x},{yg+26} l9,-7" stroke="{PIPE_R}" stroke-width="3"/>')

def valve(x, y, c=PIPE_R):
    return f'<rect x="{x-14}" y="{y-14}" width="28" height="28" rx="5" fill="#94A3B8" stroke="{NAVY}" stroke-width="3"/><rect x="{x-24}" y="{y-34}" width="48" height="12" rx="6" fill="{c}"/><rect x="{x-3}" y="{y-24}" width="6" height="12" fill="{NAVY}"/>'

def label(x, y, text, anchor="middle", fill="#fff", color=NAVY, size=24, bold=True):
    wpx = len(text) * size * 0.6 + 28
    rx = x - wpx / 2 if anchor == "middle" else (x if anchor == "start" else x - wpx)
    return (f'<rect x="{rx:.0f}" y="{y-size-6}" width="{wpx:.0f}" height="{size+20}" rx="{(size+20)/2:.0f}" fill="{fill}" stroke="{NAVY}" stroke-opacity=".15" stroke-width="2"/>'
            f'<text x="{rx+wpx/2:.0f}" y="{y+4}" text-anchor="middle" font-family="{FONT}" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}">{esc(text)}</text>')

def arrow(x1, y1, x2, y2, c=NAVY, w=4):
    import math
    a = math.atan2(y2 - y1, x2 - x1); L = 16
    p1 = (x2 - L*math.cos(a-0.45), y2 - L*math.sin(a-0.45)); p2 = (x2 - L*math.cos(a+0.45), y2 - L*math.sin(a+0.45))
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/><polygon points="{x2},{y2} {p1[0]:.0f},{p1[1]:.0f} {p2[0]:.0f},{p2[1]:.0f}" fill="{c}"/>'

def tower(x, yg, w=110, h=300, c="#F1F5F9"):
    out = f'<rect x="{x}" y="{yg-h}" width="{w}" height="{h}" fill="{c}" stroke="#CBD5E1" stroke-width="3"/>'
    for r in range(int((h-30)/34)):
        out += f'<rect x="{x+10}" y="{yg-h+16+r*34}" width="{w-20}" height="10" rx="3" fill="#93C5FD" opacity=".9"/>'
    return out

def sea(y, x0=0, x1=W):
    return f'<rect x="{x0}" y="{y}" width="{x1-x0}" height="40" fill="url(#sea)"/>' + "".join(f'<path d="M{x},{y+14} q14,-8 28,0" stroke="#fff" stroke-width="3" fill="none" opacity=".6"/>' for x in range(x0+20, x1, 90))

def device(x, yg):
    """Ground microphone / listening device on the surface."""
    return (f'<rect x="{x-6}" y="{yg-120}" width="12" height="106" rx="5" fill="{NAVY2}"/>'
            f'<ellipse cx="{x}" cy="{yg-8}" rx="34" ry="10" fill="{NAVY}"/><rect x="{x-30}" y="{yg-24}" width="60" height="16" rx="6" fill="{TEAL}"/>'
            f'<rect x="{x-32}" y="{yg-170}" width="64" height="52" rx="8" fill="{NAVY}"/><rect x="{x-24}" y="{yg-162}" width="48" height="26" rx="4" fill="{MINT}"/>'
            f'<path d="M{x-18},{yg-148} l8,-6 l7,10 l8,-14 l7,8" fill="none" stroke="{NAVY}" stroke-width="3"/>')

def badge(text):
    """Small corner tag with the brand mark."""
    return (f'<rect x="28" y="{H-62}" width="{len(text)*11+72}" height="40" rx="20" fill="{NAVY}" opacity=".9"/>'
            f'<circle cx="52" cy="{H-42}" r="10" fill="none" stroke="{MINT}" stroke-width="4"/><path d="M58,{H-36} l8,8" stroke="{AMBER}" stroke-width="4" stroke-linecap="round"/>'
            f'<text x="76" y="{H-35}" font-family="{FONT}" font-size="19" font-weight="700" fill="#fff">{esc(text)}</text>')

# ------------------------------------------------------------------ scenes
S = {}

def scene(name):
    def deco(f):
        S[name] = f
        return f
    return deco

@scene("home-service-line")
def _():
    yg = 330
    b = sun() + cloud(250, 90) + cloud(720, 70, .8) + ground(yg)
    b += house(720, yg, 330, 190) + palm(1110, yg, 220) + shrub(690, yg) + shrub(1065, yg, 22)
    b += meterbox(150, yg) + label(150, yg-50, "Water meter")
    b += pipe([(150, yg+50), (150, yg+150), (700, yg+150), (790, yg+150), (790, yg-6)])
    b += valve(790, yg-30) + label(640, yg-90, "Main shut-off", size=20)
    b += leak(450, yg+150) + label(450, yg+240, "Hidden leak", fill="#FEF3C7")
    b += device(450, yg) + waves(450, yg+110, up=True)
    b += label(640, yg+108, "Service line (your side)", fill=AQUA, size=20)
    return svg(b + badge("Meter to house: the line you own"))

@scene("home-steps")
def _():
    b = f'<rect width="{W}" height="{H}" fill="{AQUA}"/>'
    steps = [("1", "Meter test", "Shut off all water", "meter"), ("2", "Isolate", "Close the main valve", "valve"),
             ("3", "Pinpoint", "Listen or trace the line", "ear"), ("4", "Repair", "Small dig, test, restore", "wrench")]
    for i, (n, t, s, ic) in enumerate(steps):
        x = 60 + i * 282
        b += f'<rect x="{x}" y="185" width="250" height="380" rx="22" fill="#fff" stroke="#CBD5E1" stroke-width="2"/>'
        b += f'<circle cx="{x+125}" cy="185" r="34" fill="{NAVY}"/><text x="{x+125}" y="197" text-anchor="middle" font-family="{FONT}" font-size="32" font-weight="700" fill="#fff">{n}</text>'
        cx, cy = x + 125, 330
        if ic == "meter":
            b += f'<circle cx="{cx}" cy="{cy}" r="58" fill="#E2E8F0" stroke="{NAVY}" stroke-width="6"/><path d="M{cx},{cy} l34,-26" stroke="{PIPE_R}" stroke-width="7" stroke-linecap="round"/><circle cx="{cx}" cy="{cy}" r="8" fill="{NAVY}"/><polygon points="{cx-14},{cy+30} {cx+14},{cy+30} {cx},{cy+8}" fill="{TEAL}"/>'
        elif ic == "valve":
            b += pipe([(cx-90, cy+20), (cx+90, cy+20)], w=22) + valve(cx, cy+20) + f'<path d="M{cx+40},{cy-50} a40,40 0 1,1 -80,0" fill="none" stroke="{AMBER}" stroke-width="6"/><polygon points="{cx-50},{cy-58} {cx-30},{cy-58} {cx-40},{cy-40}" fill="{AMBER}"/>'
        elif ic == "ear":
            b += f'<rect x="{cx-100}" y="{cy+66}" width="200" height="14" rx="4" fill="{GRASS}"/>' + device(cx, cy+70) + pipe([(cx-100, cy+104), (cx+100, cy+104)], w=12, outline=False)
        else:
            b += pipe([(cx-90, cy+30), (cx+90, cy+30)], w=22) + f'<rect x="{cx-24}" y="{cy+12}" width="48" height="36" rx="6" fill="{AMBER}"/>' + f'<path d="M{cx-60},{cy-60} l70,70" stroke="{NAVY}" stroke-width="16" stroke-linecap="round"/><circle cx="{cx-64}" cy="{cy-64}" r="22" fill="none" stroke="{NAVY}" stroke-width="12"/>'
        b += f'<text x="{x+125}" y="470" text-anchor="middle" font-family="{FONT}" font-size="30" font-weight="700" fill="{NAVY}">{t}</text>'
        b += f'<text x="{x+125}" y="508" text-anchor="middle" font-family="{FONT}" font-size="19" fill="#4B5563">{s}</text>'
        if i < 3:
            b += arrow(x + 254, 375, x + 278, 375, c=TEAL, w=5)
    b += f'<text x="600" y="100" text-anchor="middle" font-family="{FONT}" font-size="36" font-weight="700" fill="{NAVY}">How a hidden leak is found</text>'
    return svg(b, bg=AQUA)

@scene("svc-water-service-line-repair")
def _():
    yg = 300
    b = sun(1080, 80, 38) + cloud(380, 80) + ground(yg)
    b += house(860, yg, 260, 160, style="hip") + shrub(840, yg)
    b += meterbox(110, yg) + label(110, yg-52, "Meter", size=20)
    # excavation pit
    b += f'<polygon points="430,{yg-4} 690,{yg-4} 650,{yg+190} 470,{yg+190}" fill="#8B6B4A"/><polygon points="440,{yg-4} 680,{yg-4} 642,{yg+182} 478,{yg+182}" fill="#A37E58"/>'
    b += f'<path d="M380,{yg-6} q30,-50 60,-10 q25,-40 55,-4 Z" fill="#B88A5A"/><path d="M690,{yg-6} q30,-46 60,-8 q24,-36 50,-2 Z" fill="#B88A5A"/>'
    b += pipe([(110, yg+48), (110, yg+150), (930, yg+150), (930, yg-4)])
    b += f'<rect x="530" y="{yg+128}" width="64" height="44" rx="8" fill="{AMBER}" stroke="{NAVY}" stroke-width="3"/>'
    b += label(560, yg+236, "Repair coupling", fill="#FEF3C7", size=20) + label(560, yg-70, "Small access pit", size=20)
    b += label(300, yg+112, "Service line", fill=AQUA, size=20)
    return svg(b + badge("Spot repair on a service line"))

@scene("svc-water-line-replacement")
def _():
    yg = 300
    b = cloud(240, 90) + cloud(900, 70, .8) + ground(yg)
    b += house(900, yg, 250, 160) + palm(820, yg, 180, -14)
    # driveway slab on the surface
    b += f'<rect x="380" y="{yg-14}" width="360" height="24" rx="3" fill="#CBD5E1" stroke="#94A3B8" stroke-width="3"/>'
    b += f'<g fill="#475569"><rect x="470" y="{yg-60}" width="170" height="46" rx="14"/><circle cx="505" cy="{yg-14}" r="16"/><circle cx="605" cy="{yg-14}" r="16"/></g>'
    for px in (230, 860):
        b += f'<rect x="{px-50}" y="{yg-2}" width="100" height="150" fill="#A37E58"/>'
    b += f'<path d="M230,{yg+130} Q545,{yg+230} 860,{yg+130}" fill="none" stroke="{TEAL}" stroke-width="18" stroke-dasharray="2 0"/>'
    b += f'<path d="M230,{yg+130} Q545,{yg+230} 860,{yg+130}" fill="none" stroke="#fff" stroke-width="3" stroke-dasharray="14 12" opacity=".8"/>'
    b += pipe([(90, yg+130), (230, yg+130)], color="#64748B") + meterbox(90, yg)
    b += label(230, yg-40, "Entry pit", size=20) + label(860, yg-40, "Exit pit", size=20)
    b += label(545, yg+272, "New line bored under the driveway", fill=AQUA, size=20)
    return svg(b + badge("Trenchless water line replacement"))

@scene("svc-slab-leak-repair")
def _():
    yg = 380
    b = f'<rect x="0" y="0" width="{W}" height="{yg}" fill="#F8FAFC"/>'
    b += f'<rect x="120" y="80" width="960" height="{yg-80}" fill="#fff" stroke="#CBD5E1" stroke-width="4"/>'
    b += f'<rect x="170" y="{yg-150}" width="200" height="150" fill="#E2E8F0"/><rect x="190" y="{yg-120}" width="160" height="20" fill="#94A3B8"/>'  # counter
    b += f'<rect x="760" y="{yg-110}" width="230" height="110" rx="18" fill="#BFDBFE"/>'  # sofa-ish
    b += f'<ellipse cx="560" cy="{yg-4}" rx="120" ry="16" fill="{AMBER}" opacity=".45"/>' + label(560, yg-70, "Warm or damp spot", fill="#FEF3C7", size=20)
    b += f'<rect x="80" y="{yg}" width="1040" height="44" fill="#CBD5E1" stroke="#94A3B8" stroke-width="3"/>'
    b += "".join(f'<line x1="{x}" y1="{yg+8}" x2="{x+30}" y2="{yg+36}" stroke="#94A3B8" stroke-width="2"/>' for x in range(100, 1100, 60))
    b += ground(yg+44, 0, W, seed=4).replace(f'fill="{GRASS}"', 'fill="#C49A6C"')
    b += pipe([(80, yg+110), (1120, yg+110)], color="#B45309", w=14)
    b += pipe([(260, yg+110), (260, yg+40)], color="#B45309", w=12, outline=False)
    b += leak(560, yg+110, .9)
    b += label(980, yg+180, "Copper line under the slab", fill=AQUA, size=20) + label(170, 50, "Concrete slab home", size=20)
    return svg(b + badge("Slab leak under a concrete floor"), bg="#F8FAFC")

@scene("svc-underground-leak-detection")
def _():
    yg = 300
    b = sun(120, 90, 36) + cloud(520, 80, .9) + ground(yg, seed=7)
    b += house(900, yg, 250, 160, style="hip") + palm(830, yg, 180)
    b += pipe([(0, yg+150), (980, yg+150), (980, yg-4)])
    b += leak(420, yg+150)
    b += device(420, yg) + waves(420, yg+118)
    b += f'<path d="M640,{yg+150} l0,-0" />'
    # tracer gas bubbles rising
    b += "".join(f'<circle cx="{660+dx}" cy="{yg+130-dy}" r="{r}" fill="{MINT}" opacity=".8"/>' for dx, dy, r in ((0, 20, 8), (14, 52, 6), (-8, 84, 7), (6, 112, 5)))
    b += label(420, yg-200, "Ground microphone", size=20) + label(690, yg+228, "Tracer gas rising", fill=AQUA, size=20)
    b += label(250, yg+228, "Leak pinpointed", fill="#FEF3C7", size=20)
    return svg(b + badge("Pinpointing a buried leak"))

@scene("svc-emergency-water-line-repair")
def _():
    yg = 360
    b = f'<rect width="{W}" height="{yg}" fill="url(#night)"/>' + "".join(f'<circle cx="{x}" cy="{y}" r="2" fill="#fff" opacity=".7"/>' for x, y in ((90, 60), (300, 120), (520, 50), (760, 90), (980, 40), (1130, 130)))
    b += ground(yg, seed=9) + house(760, yg, 300, 180, wall="#E2E8F0")
    b += f'<rect x="800" y="{yg-140}" width="58" height="50" rx="4" fill="#FDE68A"/>'
    b += pipe([(0, yg+140), (700, yg+140), (900, yg+140), (900, yg-6)])
    b += valve(900, yg-34, c=AMBER) + label(1040, yg+70, "Close the main", fill="#FEF3C7", size=22) + arrow(960, yg+60, 918, yg-14, c=AMBER, w=4)
    # geyser
    b += f'<path d="M360,{yg+130} C330,{yg-20} 300,{yg-160} 250,{yg-200} M360,{yg+130} C370,{yg-60} 380,{yg-190} 360,{yg-250} M360,{yg+130} C400,{yg-20} 450,{yg-150} 490,{yg-190}" stroke="{WATER}" stroke-width="16" fill="none" stroke-linecap="round" opacity=".9"/>'
    b += leak(360, yg+4, 1.2) + label(360, yg+230, "Burst line", fill="#FEE2E2", size=22)
    return svg(b + badge("Water line emergency: shut it off first"), bg=NAVY)

@scene("svc-repiping")
def _():
    b = f'<rect width="{W}" height="{H}" fill="#F8FAFC"/>'
    b += f'<rect x="80" y="70" width="1040" height="520" fill="#FDF6EC" stroke="#E2D3BC" stroke-width="4"/>'
    for x in range(120, 1120, 120):
        b += f'<rect x="{x}" y="70" width="22" height="520" fill="#E7C9A0"/>'
    b += f'<rect x="80" y="110" width="1040" height="22" fill="#E7C9A0"/>'
    hot = [(200, 600), (200, 170), (1040, 170)]; cold = [(250, 600), (250, 210), (1040, 210)]
    b += pipe(hot, color=PIPE_R, w=14) + pipe(cold, color=PIPE_B, w=14)
    for fx, name in ((420, "Sink"), (680, "Shower"), (930, "Toilet")):
        b += pipe([(fx, 170), (fx, 400)], color=PIPE_R, w=12, outline=False) + pipe([(fx+40, 210), (fx+40, 400)], color=PIPE_B, w=12, outline=False)
        b += f'<rect x="{fx-20}" y="400" width="80" height="26" rx="6" fill="#94A3B8"/>' + label(fx+20, 480, name, size=20)
    b += label(380, 140, "New PEX lines", fill=AQUA, size=20)
    return svg(b + badge("Whole-house repipe inside the walls"), bg="#F8FAFC")

@scene("svc-sewer-line-repair")
def _():
    yg = 300
    b = cloud(300, 80) + ground(yg, seed=11) + house(80, yg, 260, 160) + shrub(380, yg)
    b += f'<rect x="420" y="{yg-40}" width="22" height="44" rx="4" fill="#E2E8F0" stroke="#94A3B8" stroke-width="3"/>' + label(431, yg-64, "Cleanout", size=18)
    b += pipe([(300, yg+60), (431, yg+90), (1200, yg+230)], color="#6B7280", w=26)
    b += pipe([(431, yg+90), (431, yg)], color="#6B7280", w=16, outline=False)
    # roots
    b += f'<g stroke="#7C2D12" stroke-width="5" fill="none" stroke-linecap="round"><path d="M820,{yg} q-20,60 -10,150"/><path d="M820,{yg} q30,70 20,160"/><path d="M800,{yg+80} q-30,20 -60,30"/></g>'
    b += shrub(820, yg, 40, "#15803D")
    # camera
    b += f'<rect x="600" y="{yg+136}" width="44" height="20" rx="8" fill="{NAVY}" transform="rotate(10 622 {yg+146})"/><path d="M650,{yg+152} l60,-20 l0,44 Z" fill="#FDE68A" opacity=".7"/>'
    b += f'<path d="M431,{yg+90} Q520,{yg+140} 600,{yg+146}" stroke="{AMBER}" stroke-width="4" fill="none"/>'
    b += label(640, yg+250, "Camera inspection", fill=AQUA, size=20) + label(900, yg+300, "Root intrusion", fill="#FEF3C7", size=20)
    b += label(1060, yg+180, "To city main", size=18)
    return svg(b + badge("Sewer lateral camera inspection"))

@scene("svc-pool-leak-detection")
def _():
    yg = 300
    b = sun() + cloud(260, 80) + f'<rect x="0" y="{yg-10}" width="{W}" height="{H}" fill="#E7E5E4"/>'
    b += f'<path d="M150,{yg} L850,{yg} L850,{yg+230} Q500,{yg+300} 150,{yg+230} Z" fill="#E2E8F0" stroke="#94A3B8" stroke-width="5"/>'
    b += f'<path d="M165,{yg+22} L835,{yg+22} L835,{yg+222} Q500,{yg+286} 165,{yg+222} Z" fill="url(#pool)"/>'
    b += "".join(f'<path d="M{x},{yg+40} q16,-8 32,0" stroke="#fff" stroke-width="3" fill="none" opacity=".7"/>' for x in range(200, 820, 110))
    # step with bucket
    b += f'<rect x="165" y="{yg+70}" width="120" height="30" fill="#CBD5E1"/>'
    b += f'<path d="M190,{yg+8} L260,{yg+8} L252,{yg+70} L198,{yg+70} Z" fill="{AMBER}" stroke="{NAVY}" stroke-width="3"/><line x1="196" y1="{yg+34}" x2="256" y2="{yg+34}" stroke="{NAVY}" stroke-width="3"/>'
    b += label(225, yg-40, "Bucket test", size=20)
    # skimmer and equipment
    b += f'<rect x="700" y="{yg+6}" width="60" height="24" rx="4" fill="#475569"/>' + label(730, yg-40, "Skimmer", size=20)
    b += f'<rect x="950" y="{yg-90}" width="90" height="90" rx="12" fill="#64748B"/><rect x="1060" y="{yg-70}" width="70" height="70" rx="10" fill="#475569"/>' + label(1040, yg-120, "Pump & filter", size=20)
    b += pipe([(990, yg), (990, yg+260), (860, yg+260), (760, yg+200)], color="#F8FAFC", w=12)
    b += leak(900, yg+260, .7) + label(990, yg+330, "Return line leak", fill="#FEF3C7", size=20)
    return svg(b + badge("Pool leak: shell, fittings or plumbing"))

# ------------------------------------------------------------------ locations
@scene("loc-bradenton")
def _():
    yg = 330
    b = sun(150, 90, 38) + cloud(700, 70) + f'<rect x="0" y="{yg-60}" width="{W}" height="50" fill="url(#sea)"/>'
    b += ground(yg, seed=12) + house(300, yg, 300, 160, wall="#FEF3C7", style="gable", roof="#7C2D12")
    b += f'<rect x="280" y="{yg-40}" width="340" height="12" fill="#E5E7EB"/>' + shrub(650, yg, 30) + palm(720, yg, 200)
    b += pipe([(60, yg+120), (480, yg+120), (480, yg-4)], color="#9CA3AF") + meterbox(60, yg)
    b += label(270, yg+190, "Older galvanized or copper line", fill=AQUA, size=20)
    b += label(940, yg-150, "Riverfront lots", size=20)
    return svg(b + badge("Older homes near the river"))

@scene("loc-lakewood-ranch")
def _():
    yg = 330
    b = sun() + cloud(300, 80) + ground(yg, seed=13)
    for i, x in enumerate((60, 430, 800)):
        b += house(x, yg, 300, 170, wall=("#FFFFFF", "#F1F5F9", "#FFF7ED")[i], style="hip", roof=("#334155", NAVY, "#475569")[i])
    b += "".join(f'<rect x="{x}" y="{yg-6}" width="30" height="12" fill="#D6B88E" stroke="#B88A5A"/>' for x in range(430, 740, 32))
    b += pipe([(0, yg+120), (1200, yg+120)], color="#2563EB", w=12)
    b += "".join(pipe([(x, yg+120), (x, yg+40)], color="#7C3AED", w=8, outline=False) + f'<rect x="{x-6}" y="{yg+30}" width="12" height="14" fill="#1F2937"/>' for x in (250, 640, 1020))
    b += label(380, yg+200, "PEX and plastic service lines", fill=AQUA, size=20) + label(880, yg+200, "Irrigation zones", fill="#EDE9FE", size=20)
    b += label(590, yg-210, "Paver drives over the line", size=20)
    return svg(b + badge("Newer homes, quieter leaks"))

@scene("loc-longboat-key")
def _():
    yg = 360
    b = sun(1080, 90, 40) + cloud(200, 80) + sea(yg-30, 0, W)
    b += f'<rect x="0" y="{yg-30}" width="{W}" height="22" fill="#FDE68A"/>'
    b += tower(150, yg-8, 120, 280) + tower(300, yg-8, 140, 340, "#FFF7ED") + tower(470, yg-8, 110, 250)
    b += palm(640, yg-8, 200) + palm(700, yg-8, 160, -16)
    b += ground(yg, seed=14).replace(f'fill="{GRASS}"', 'fill="#FDE68A"')
    b += f'<rect x="0" y="{yg+150}" width="{W}" height="{H-yg-150}" fill="#7DB9D6" opacity=".55"/>' + label(1000, yg+200, "High water table", fill=AQUA, size=20)
    b += pipe([(80, yg+60), (980, yg+60)], color=PIPE_B, w=12) + pipe([(80, yg+90), (980, yg+90)], color="#F59E0B", w=10, outline=False) + pipe([(80, yg+118), (980, yg+118)], color="#16A34A", w=10, outline=False)
    b += label(520, yg+176, "Utilities packed close together", size=20)
    return svg(b + badge("A narrow barrier island"))

@scene("loc-nokomis")
def _():
    yg = 320
    b = sun(140, 90) + cloud(640, 70) + ground(yg, seed=15)
    b += house(560, yg, 300, 160, wall="#ECFEFF", style="gable", roof=TEALD) + palm(940, yg, 210) + shrub(520, yg)
    b += f'<rect x="200" y="{yg+60}" width="240" height="110" rx="20" fill="#9CA3AF" stroke="#475569" stroke-width="4"/>' + label(320, yg+210, "Septic tank", fill="#F1F5F9", size=20)
    b += pipe([(600, yg+40), (440, yg+100)], color="#6B7280", w=14)
    b += pipe([(1200, yg+150), (760, yg+150), (760, yg-4)], color=PIPE_B, w=14) + meterbox(1130, yg)
    b += label(980, yg+230, "Water line from the street", fill=AQUA, size=20)
    return svg(b + badge("Septic and water lines on one lot"))

@scene("loc-north-port")
def _():
    yg = 330
    b = cloud(220, 80) + cloud(820, 60, .8) + ground(yg, seed=16)
    b += f'<rect x="1000" y="{yg-12}" width="200" height="{H}" fill="url(#sea)"/>' + label(1100, yg-40, "Canal", size=20)
    b += house(700, yg, 260, 160, style="hip") + palm(980, yg, 180, -20) + shrub(670, yg)
    b += meterbox(60, yg) + pipe([(60, yg+48), (60, yg+140), (820, yg+140), (820, yg-4)])
    b += arrow(110, yg+200, 780, yg+200, c=TEAL, w=4) + arrow(780, yg+200, 110, yg+200, c=TEAL, w=4)
    b += label(440, yg+250, "Long run from meter to house", fill=AQUA, size=20)
    b += leak(330, yg+140, .7)
    return svg(b + badge("Deep lots, long service lines"))

@scene("loc-osprey")
def _():
    yg = 330
    b = sun() + sea(yg-50, 0, 520) + ground(yg, seed=17)
    b += f'<ellipse cx="300" cy="{yg-6}" rx="200" ry="14" fill="#86EFAC"/><rect x="380" y="{yg-90}" width="4" height="84" fill="#475569"/><polygon points="384,{yg-90} 420,{yg-80} 384,{yg-70}" fill="{PIPE_R}"/>'
    b += label(300, yg-120, "Golf communities", size=20)
    b += house(640, yg, 320, 170, wall="#FFFFFF", style="tile") + palm(1010, yg, 210)
    b += f'<rect x="980" y="{yg+20}" width="200" height="70" rx="10" fill="url(#pool)" stroke="#94A3B8" stroke-width="4"/>' + label(1080, yg+130, "Pool lines", size=18)
    b += pipe([(1080, yg+90), (1080, yg+200), (720, yg+200)], color="#F8FAFC", w=10)
    b += f'<g fill="#fff" opacity=".85">' + "".join(f'<circle cx="{x}" cy="{y}" r="3"/>' for x, y in ((560, 200), (600, 170), (520, 150), (640, 210))) + '</g>'
    b += label(560, yg+130, "Salt air on metal fittings", fill=AQUA, size=20)
    return svg(b + badge("Bayfront lots, pools and HOAs"))

@scene("loc-siesta-key")
def _():
    yg = 350
    b = sun(1060, 90) + cloud(300, 80) + sea(yg-40, 0, W) + f'<rect x="0" y="{yg-40}" width="{W}" height="30" fill="#FEF9C3"/>'
    b += house(140, yg-10, 240, 140, wall="#FDF2F8", style="hip", roof=TEAL) + tower(500, yg-10, 150, 260) + tower(680, yg-10, 120, 210, "#FFF7ED")
    b += palm(420, yg-10, 180) + palm(880, yg-10, 200, -16)
    b += ground(yg, seed=18).replace(f'fill="{GRASS}"', 'fill="#FEF9C3"')
    b += f'<rect x="0" y="{yg+110}" width="{W}" height="{H-yg-110}" fill="#7DB9D6" opacity=".6"/>'
    b += f'<rect x="300" y="{yg-4}" width="160" height="140" fill="#A37E58"/><rect x="300" y="{yg+110}" width="160" height="30" fill="#60A5FA" opacity=".8"/>'
    b += pipe([(80, yg+80), (900, yg+80)], color=PIPE_B, w=12)
    b += label(380, yg+190, "Holes fill with water fast", fill="#FEF3C7", size=20) + label(980, yg+190, "Sandy soil", fill=AQUA, size=20)
    return svg(b + badge("Beach cottages and condos"))

@scene("loc-venice")
def _():
    yg = 330
    b = sun(130, 90) + cloud(560, 70) + ground(yg, seed=19)
    # Mediterranean-style house with arches
    x, w, h = 380, 440, 180
    b += f'<rect x="{x}" y="{yg-h}" width="{w}" height="{h}" fill="#FDE7C7" stroke="#E2C9A2" stroke-width="3"/>'
    b += f'<polygon points="{x-20},{yg-h+4} {x+w*0.15},{yg-h-50} {x+w*0.85},{yg-h-50} {x+w+20},{yg-h+4}" fill="#C2410C"/>'
    for i in range(4):
        ax = x + 40 + i * 100
        b += f'<path d="M{ax},{yg} L{ax},{yg-90} A30,30 0 0,1 {ax+60},{yg-90} L{ax+60},{yg} Z" fill="#0E7490" opacity=".85"/>'
    b += palm(300, yg, 220) + palm(900, yg, 200, -14) + shrub(860, yg)
    b += pipe([(1200, yg+140), (600, yg+140), (600, yg-4)], color="#9CA3AF") + meterbox(1120, yg)
    b += f'<rect x="740" y="{yg+124}" width="54" height="34" rx="6" fill="{AMBER}" stroke="{NAVY}" stroke-width="3"/>'
    b += label(860, yg+220, "Older pipe, past repairs", fill=AQUA, size=20)
    return svg(b + badge("Older and historic homes"))

def render_all():
    os.makedirs(OUT, exist_ok=True)
    src = os.path.join(ROOT, "illustrations")
    os.makedirs(src, exist_ok=True)
    for name, f in S.items():
        s = f()
        open(os.path.join(src, f"{name}.svg"), "w").write(s)
        png = cairosvg.svg2png(bytestring=s.encode(), output_width=W, output_height=H)
        im = Image.open(io.BytesIO(png)).convert("RGB")
        im.save(os.path.join(OUT, f"{name}.webp"), "WEBP", quality=82, method=6)
        im.resize((600, 338), Image.LANCZOS).save(os.path.join(OUT, f"{name}-600.webp"), "WEBP", quality=80, method=6)
    print(f"{len(S)} illustrations -> {OUT}")

if __name__ == "__main__":
    render_all()
