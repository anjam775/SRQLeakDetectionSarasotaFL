#!/usr/bin/env python3
"""Headless Chrome QA: responsive overflow, console/CSP errors, interactive states, CLS/LCP, screenshots."""
import http.server, threading, os, json, functools, re
from playwright.sync_api import sync_playwright

DIST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "qa")
os.makedirs(OUT, exist_ok=True)
CSP = re.search(r"Content-Security-Policy: (.+)", open(f"{DIST}/_headers").read()).group(1)

class H(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Content-Security-Policy", CSP)
        super().end_headers()
    def log_message(self, *a): pass
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 8765), functools.partial(H, directory=DIST))
threading.Thread(target=srv.serve_forever, daemon=True).start()
B = "http://127.0.0.1:8765"

PAGES = ["/blog/main-water-line-repair-cost/", "/blog/does-home-warranty-cover-slab-leaks/", "/blog/why-is-my-water-pressure-low/", "/blog/pool-bucket-test/", "/glossary/", "/", "/services/", "/services/slab-leak-repair/", "/locations/", "/locations/siesta-key/", "/blog/",
         "/blog/why-is-my-water-bill-so-high/", "/glossary/", "/contact/", "/about/", "/privacy-policy/", "/404.html"]
res = {"overflow": [], "console": [], "css": [], "cls": {}, "lcp": {}, "states": []}

with sync_playwright() as p:
    br = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    for w, hgt in [(360, 780), (768, 1024), (1280, 900)]:
        ctx = br.new_context(viewport={"width": w, "height": hgt})
        # Google Analytics is unreachable from the sandbox: serve an empty gtag.js and accept beacons
        ctx.route("https://www.googletagmanager.com/**", lambda r: r.fulfill(status=200, body="", headers={"content-type": "application/javascript"}))
        ctx.route(re.compile(r"https://.*(google-analytics|analytics\.google)\.com/.*"), lambda r: r.fulfill(status=204, body=""))
        ctx.route(re.compile(r"https://(static\.)?cloudflareinsights\.com/.*"), lambda r: r.fulfill(status=204, body=""))
        for u in PAGES:
            pg = ctx.new_page()
            pg.on("console", lambda m, w=w: res["console"].append(f"{w}px {m.type}: {m.text}") if m.type in ("error", "warning") else None)
            pg.on("pageerror", lambda e, w=w: res["console"].append(f"{w}px pageerror {e}"))
            pg.add_init_script("""window.__cls=0;new PerformanceObserver(l=>{for(const e of l.getEntries()){if(!e.hadRecentInput)window.__cls+=e.value}}).observe({type:'layout-shift',buffered:true});
window.__lcp=0;new PerformanceObserver(l=>{const e=l.getEntries();window.__lcp=e[e.length-1].startTime}).observe({type:'largest-contentful-paint',buffered:true});""")
            pg.goto(B + u, wait_until="networkidle")
            pg.wait_for_timeout(300)
            ov = pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
            if ov > 0: res["overflow"].append(f"{u} @{w}px +{ov}px")
            # CSS from site.css applied? footer background is defined only in site.css
            bg = pg.evaluate("getComputedStyle(document.querySelector('.ftr')).backgroundColor")
            if bg not in ("rgb(11, 37, 69)",): res["css"].append(f"{u} @{w}px footer bg {bg}")
            res["cls"][f"{u}@{w}"] = round(pg.evaluate("window.__cls"), 4)
            res["lcp"][f"{u}@{w}"] = round(pg.evaluate("window.__lcp"))
            pg.close()
        pg = ctx.new_page()
        pg.goto(B + "/", wait_until="networkidle")
        pg.screenshot(path=f"{OUT}/home-{w}.png", full_page=False)
        pg.screenshot(path=f"{OUT}/home-{w}-full.png", full_page=True)
        if w == 360:
            # mobile menu + sticky bar
            vis = pg.evaluate("getComputedStyle(document.querySelector('.sticky-call')).display")
            res["states"].append(f"360 sticky bar display={vis}")
            pg.click(".menu-tg"); pg.wait_for_timeout(150)
            res["states"].append("360 menu open=" + str(pg.evaluate("document.getElementById('nav').classList.contains('open')")))
            pg.click(".has-sub .sub-tg"); pg.wait_for_timeout(150)
            res["states"].append("360 services submenu visible=" + str(pg.is_visible(".has-sub .sub a")))
            pg.screenshot(path=f"{OUT}/menu-360.png")
            pg.keyboard.press("Escape"); pg.wait_for_timeout(100)
            res["states"].append("360 Esc closes menu=" + str(not pg.evaluate("document.getElementById('nav').classList.contains('open')")))
            pg.goto(B + "/services/slab-leak-repair/", wait_until="networkidle")
            pg.screenshot(path=f"{OUT}/service-360-full.png", full_page=True)
            pg.goto(B + "/blog/why-is-my-water-bill-so-high/", wait_until="networkidle")
            pg.screenshot(path=f"{OUT}/post-360.png", full_page=False)
        if w == 1280:
            vis = pg.evaluate("getComputedStyle(document.querySelector('.sticky-call')).display")
            res["states"].append(f"1280 sticky bar display={vis} (expect none)")
            res["states"].append("1280 header call visible=" + str(pg.is_visible(".hdr-call")))
            pg.hover(".has-sub >> nth=0"); pg.wait_for_timeout(200)
            res["states"].append("1280 hover dropdown visible=" + str(pg.is_visible(".has-sub >> nth=0 >> .sub")))
            pg.screenshot(path=f"{OUT}/dropdown-1280.png")
            # hover CTA + card colors
            pg.mouse.move(5, 5)
            before = pg.evaluate("getComputedStyle(document.querySelector('.hero .btn-cta')).backgroundColor")
            pg.hover(".hero .btn-cta"); pg.wait_for_timeout(250)
            after = pg.evaluate("getComputedStyle(document.querySelector('.hero .btn-cta')).backgroundColor")
            col = pg.evaluate("getComputedStyle(document.querySelector('.hero .btn-cta')).color")
            res["states"].append(f"1280 CTA hover bg {before} -> {after}, text {col}")
            pg.hover(".cards .card >> nth=0"); pg.wait_for_timeout(250)
            bc = pg.evaluate("getComputedStyle(document.querySelector('.cards .card')).borderColor")
            res["states"].append(f"1280 card hover border {bc}")
            # logo hover keeps visible
            pg.hover(".hdr .logo"); pg.wait_for_timeout(150)
            res["states"].append("1280 logo visible on hover=" + str(pg.is_visible(".hdr .logo .wm")))
            # keyboard focus outline on first nav link
            pg.keyboard.press("Tab"); pg.keyboard.press("Tab")
            ol = pg.evaluate("(()=>{const a=document.activeElement;const s=getComputedStyle(a);return a.className+' outline:'+s.outlineStyle+' '+s.outlineWidth})()")
            res["states"].append("1280 focus " + ol)
            # footer link hover contrast
            pg.hover(".ftr ul a >> nth=0"); pg.wait_for_timeout(150)
            res["states"].append("1280 footer link hover color " + pg.evaluate("getComputedStyle(document.querySelector('.ftr ul a')).color"))
            pg.goto(B + "/blog/", wait_until="networkidle"); pg.screenshot(path=f"{OUT}/blog-1280.png")
            pg.goto(B + "/locations/venice/", wait_until="networkidle"); pg.screenshot(path=f"{OUT}/location-1280-full.png", full_page=True)
        ctx.close()
    br.close()
srv.shutdown()
json.dump(res, open(f"{OUT}/qa.json", "w"), indent=1)
print("overflow:", res["overflow"] or "none")
print("console/CSP:", res["console"] or "none")
print("css applied issues:", res["css"] or "none")
print("max CLS:", max(res["cls"].values()), " max LCP(ms, local):", max(res["lcp"].values()))
for s in res["states"]: print(" ", s)
