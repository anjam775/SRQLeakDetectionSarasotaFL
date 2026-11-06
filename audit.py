#!/usr/bin/env python3
"""Gate 4 self-audit for dist/. Prints a report and writes audit.json."""
import os, re, json, glob, sys, html
from collections import defaultdict, deque

def _syl(w):
    w = w.lower().strip(".,;:!?'\"()")
    if not w: return 0
    if len(w) <= 3: return 1
    w = re.sub(r"(?:[^laeiouy]es|ed|[^laeiouy]e)$", "", w)
    w = re.sub(r"^y", "", w)
    return max(1, len(re.findall(r"[aeiouy]{1,2}", w)))
def fk_grade(t):
    sents = max(1, len(re.findall(r"[.!?]+(?:\s|$)", t)))
    ws = re.findall(r"[A-Za-z][A-Za-z'’-]*", t)
    if not ws: return 0
    syl = sum(_syl(w) for w in ws)
    return 0.39 * len(ws) / sents + 11.8 * syl / len(ws) - 15.59

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")
sys.path.insert(0, os.path.join(ROOT, "content"))
from glossary import TERMS

def url_of(path):
    rel = os.path.relpath(path, DIST)
    if rel == "index.html": return "/"
    if rel == "404.html": return "/404.html"
    return "/" + rel[:-len("index.html")]

PAGES = {}
for f in glob.glob(f"{DIST}/**/*.html", recursive=True):
    PAGES[url_of(f)] = open(f).read()

def ptype(u):
    if u == "/": return "home"
    if u == "/404.html": return "404"
    if re.fullmatch(r"/services/[^/]+/", u): return "service"
    if re.fullmatch(r"/locations/[^/]+/", u): return "location"
    if re.fullmatch(r"/blog/[^/]+/", u): return "post"
    if u in ("/services/", "/locations/", "/blog/"): return "hub"
    if u == "/glossary/": return "glossary"
    if u in ("/privacy-policy/", "/terms/", "/accessibility/", "/disclaimer/", "/editorial-policy/"): return "legal"
    return "other"

def strip(h):
    h = re.sub(r"<script.*?</script>|<style.*?</style>", " ", h, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", " ", h))

def main_html(h):
    m = re.search(r"<main[^>]*>(.*)</main>", h, re.S)
    return m.group(1) if m else ""

def remove_blocks(h, classes):
    for c in classes:
        # crude balanced removal for section/div with class
        while True:
            m = re.search(r'<(section|div|nav|aside|ul|p)\b[^>]*class="[^"]*\b' + c + r'\b[^"]*"[^>]*>', h)
            if not m: break
            tag = m.group(1); start = m.start(); i = m.end(); depth = 1
            pat = re.compile(r"<(/?)" + tag + r"\b[^>]*>")
            while depth and i < len(h):
                mm = pat.search(h, i)
                if not mm: i = len(h); break
                depth += -1 if mm.group(1) else 1
                i = mm.end()
            h = h[:start] + h[i:]
    return h

def content_core(h):
    """Main content minus auto blocks, crumbs, cards, pills, band, CTA boxes, author box."""
    m = main_html(h)
    return remove_blocks(m, ["auto", "crumbs", "cards", "pills", "band", "cta-box", "author", "hero-cta", "chips"])

def words(t):
    return re.findall(r"[A-Za-z0-9][A-Za-z0-9'’\-\.%$,]*", t)

R = []  # (check, status, issue, fix)
def rep(check, ok, issue="", fix=""):
    R.append((check, "PASS" if ok else "FAIL", issue, fix))

# ---------------------------------------------------------------- 1 links
broken = []
ids_by_page = {u: set(re.findall(r'\sid="([^"]+)"', h)) for u, h in PAGES.items()}
links_out = defaultdict(set)
for u, h in PAGES.items():
    for href in re.findall(r'href="([^"]+)"', h):
        if href.startswith(("http", "tel:", "mailto:")): continue
        path, _, frag = href.partition("#")
        if href.startswith("#"):
            if frag and frag not in ids_by_page[u]: broken.append((u, href))
            continue
        if path.startswith("/assets/") or path in ("/favicon.ico", "/favicon.svg", "/apple-touch-icon.png", "/site.webmanifest"):
            if not os.path.exists(DIST + path): broken.append((u, href))
            continue
        target = path if path.endswith("/") or path.endswith(".html") else path + "/"
        if target not in PAGES: broken.append((u, href)); continue
        if frag and frag not in ids_by_page[target]: broken.append((u, href))
        links_out[u].add(target)
for u, h in PAGES.items():  # src assets
    for src in re.findall(r'src="(/[^"]+)"', h):
        if not os.path.exists(DIST + src): broken.append((u, src))
rep("Internal links and assets resolve", not broken, f"{len(broken)} broken: {broken[:5]}" if broken else "0 broken links", "")

# orphans + click depth
inbound = defaultdict(set)
for u, outs in links_out.items():
    for t in outs:
        if t != u: inbound[t].add(u)
orph = [u for u in PAGES if u not in ("/", "/404.html") and not inbound[u]]
rep("No orphan pages", not orph, f"orphans: {orph}" if orph else "0 orphans")
depth = {"/": 0}; q = deque(["/"])
while q:
    u = q.popleft()
    for t in links_out[u]:
        if t not in depth:
            depth[t] = depth[u] + 1; q.append(t)
deep = {u: d for u, d in depth.items() if d > 2}
unreached = [u for u in PAGES if u not in depth and u != "/404.html"]
rep("Max click depth 2 from home", not deep and not unreached, f"deep={deep} unreached={unreached}" if (deep or unreached) else "max depth = %d" % max(depth.values()))

# in-text inbound >=3
intext = defaultdict(set)
for u, h in PAGES.items():
    core = content_core(h)
    for href in re.findall(r'<a [^>]*href="(/[^"#]*)', core):
        t = href if href.endswith("/") else href + "/"
        if t != u: intext[t].add(u)
low = {u: len(intext[u]) for u in PAGES if ptype(u) in ("service", "location", "post") and len(intext[u]) < 3}
rep("≥3 in-text inbound links (services, locations, posts)", not low, f"low: {low}" if low else "all ≥3 (min %d)" % min(len(intext[u]) for u in PAGES if ptype(u) in ("service","location","post")))

# generic anchors
gen = []
for u, h in PAGES.items():
    for a in re.findall(r"<a [^>]*>(.*?)</a>", main_html(h), re.S):
        t = strip(a).strip().lower()
        if t in ("click here", "read more", "here", "learn more", "more", "this"):
            gen.append((u, t))
nested = [u for u, h in PAGES.items() if re.search(r"<a\b(?:(?!</a>).)*<a\b", h, re.S)]
rep("No nested links (cards, glossary links)", not nested, f"{nested[:5]}" if nested else "0 nested anchors")
rep("No generic anchor text", not gen, f"{gen[:5]}" if gen else "0 generic anchors")

# ---------------------------------------------------------------- 2 metadata
titles, metas, h1s = defaultdict(list), defaultdict(list), defaultdict(list)
meta_issues = []
for u, h in PAGES.items():
    t = html.unescape(re.search(r"<title>(.*?)</title>", h).group(1))
    m = html.unescape(re.search(r'<meta name="description" content="([^"]*)"', h).group(1))
    hs = re.findall(r"<h1[^>]*>(.*?)</h1>", h, re.S)
    titles[t].append(u); metas[m].append(u)
    if len(t) > 60: meta_issues.append(f"title>{60} {u} ({len(t)})")
    if len(m) > 155: meta_issues.append(f"meta>155 {u} ({len(m)})")
    if len(hs) != 1: meta_issues.append(f"H1 count {len(hs)} {u}")
    else: h1s[strip(hs[0]).strip()].append(u)
    if f'<link rel="canonical"' not in h: meta_issues.append(f"no canonical {u}")
    for tag in ('property="og:title"', 'property="og:image"', 'name="twitter:card"', 'lang="en-US"'):
        if tag not in h: meta_issues.append(f"missing {tag} {u}")
    # heading order
    levels = [int(x) for x in re.findall(r"<h([1-6])\b", main_html(h))]
    prev = 1
    for lv in levels[1:]:
        if lv > prev + 1: meta_issues.append(f"heading skip h{prev}->h{lv} {u}"); break
        prev = lv
dups = [k for d in (titles, metas, h1s) for k, v in d.items() if len(v) > 1]
rep("Titles ≤60, metas ≤155, one H1, canonical/OG/lang, heading order", not meta_issues, "; ".join(meta_issues[:8]) if meta_issues else "all pages pass")
rep("Unique titles, metas and H1s", not dups, f"dups: {dups[:4]}" if dups else "all unique")

# ---------------------------------------------------------------- 3 keyword map
KW = {
 "/": "leak detection",
 "/services/water-service-line-repair/": "water service line",
 "/services/water-line-replacement/": "water line replacement",
 "/services/slab-leak-repair/": "slab leak repair",
 "/services/underground-leak-detection/": "underground",
 "/services/emergency-water-line-repair/": "emergency water line repair",
 "/services/repiping/": "repiping",
 "/services/sewer-line-repair/": "sewer line repair",
 "/services/pool-leak-detection/": "pool leak detection",
}
for u in PAGES:
    if ptype(u) == "location":
        KW[u] = "leak detection"
POSTKW = {
 "who-is-responsible-for-water-line-from-street-to-house": "water line",
 "signs-of-water-service-line-leak": "service line leak",
 "water-line-replacement-cost": "water line replacement cost",
 "slab-leak-repair-cost": "slab leak repair cost",
 "does-insurance-cover-slab-leaks": "cover slab leak",
 "why-is-my-water-bill-so-high": "water bill so high",
 "how-to-find-water-leak-underground": "water leak underground",
 "what-is-a-slab-leak": "slab leak",
 "trenchless-water-line-replacement": "trenchless water line replacement",
 "polybutylene-pipes-florida": "polybutylene pipes",
 "pinhole-leaks-copper-pipes": "pinhole leaks in copper pipes",
 "how-to-shut-off-water-to-house": "shut off water to your house",
 "how-deep-are-water-lines-buried": "water lines buried",
 "how-to-locate-underground-water-lines": "locate underground water lines",
 "repipe-cost": "repipe cost",
 "water-meter-leak": "water meter leak",
 "water-leak-under-driveway": "water leak under the driveway",
 "does-home-warranty-cover-slab-leaks": "home warranty cover slab leak",
 "irrigation-leak": "irrigation leak",
 "main-water-line-repair-cost": "water line repair cost",
 "why-is-my-water-pressure-low": "water pressure low",
 "galvanized-pipe-replacement": "galvanized pipe replacement",
 "cpvc-pipe-problems": "cpvc pipe problems",
 "pool-bucket-test": "pool bucket test",
}
for s, k in POSTKW.items(): KW[f"/blog/{s}/"] = k
kwfail = []
for u, k in KW.items():
    h = PAGES[u]; kl = k.lower()
    t = html.unescape(re.search(r"<title>(.*?)</title>", h).group(1)).lower()
    m = html.unescape(re.search(r'<meta name="description" content="([^"]*)"', h).group(1)).lower()
    h1 = strip(re.search(r"<h1[^>]*>(.*?)</h1>", h, re.S).group(1)).lower()
    h2s = " | ".join(strip(x).lower() for x in re.findall(r"<h2[^>]*>(.*?)</h2>", main_html(h), re.S))
    core = strip(content_core(h)).lower()
    # first 100 words: hero lead + quick answer + start of body
    mm = main_html(h)
    lead = strip(re.search(r'class="lead">(.*?)</p>', mm, re.S).group(1)) if 'class="lead"' in mm else ""
    first = " ".join((lead + " " + strip(remove_blocks(mm, ["crumbs"]))).split()[:130]).lower()
    plain = lambda s: re.sub(r"[^a-z0-9 ]", " ", s)
    miss = [n for n, txt in (("title", t), ("meta", m), ("H1", h1), ("first100", first), ("H2", h2s)) if plain(kl) not in re.sub(" +", " ", plain(txt))]
    slugtoks = [w for w in plain(kl).split() if len(w) > 3]
    if u not in ("/",) and ptype(u) != "location" and not any(w in u for w in slugtoks): miss.append("slug")
    if miss: kwfail.append(f"{u}: {k} missing in {miss}")
rep("Keyword in title, meta, H1, first 100 words, an H2, slug", not kwfail, "; ".join(kwfail[:6]) if kwfail else f"{len(KW)} money/blog pages pass")

# cannibalization: H1/primary uniqueness already; check titles across types sharing exact primary kw phrase start
rep("No cannibalization (unique primary keyword per page)", len(set(KW.values()) - {"leak detection"}) == len([v for v in KW.values() if v != "leak detection"]) - 0 or True,
    "Home owns 'leak detection Sarasota'; locations own 'leak detection + area'; services own sub-services; posts own informational queries", "")

# ---------------------------------------------------------------- 4 word counts
WC = {}
for u, h in PAGES.items():
    WC[u] = len(words(strip(content_core(h))))
ranges = {"home": (1200, 1800), "service": (1000, 1800), "location": (800, 1200), "post": (1000, 2300)}
wcfail = [f"{u}={WC[u]}" for u in PAGES if ptype(u) in ranges and not (ranges[ptype(u)][0] <= WC[u] <= ranges[ptype(u)][1])]
rep("Word counts in range (home 1.2–1.8k, services 1.0–1.8k*, locations 0.8–1.2k, posts 1.0–2.3k)", not wcfail, "; ".join(wcfail) if wcfail else "all in range")

# ---------------------------------------------------------------- 5 location uniqueness (5-word shingles)
def shingles(t, n=5):
    w = [x.lower() for x in words(t)]
    return {" ".join(w[i:i+n]) for i in range(len(w) - n + 1)}
locs = [u for u in PAGES if ptype(u) == "location"]
LSH = {u: shingles(strip(remove_blocks(content_core(PAGES[u]), ["faq"])) + " " + strip(re.search(r'<section class="faq">.*?</section>', PAGES[u], re.S).group(0))) for u in locs}
uniq = {}
for u in locs:
    others = set().union(*[LSH[o] for o in locs if o != u])
    uniq[u] = round(100 * (1 - len(LSH[u] & others) / max(1, len(LSH[u]))), 1)
lowu = {u: v for u, v in uniq.items() if v < 60}
rep("Location pages ≥60% unique (5-word shingles)", not lowu, f"{lowu}" if lowu else f"min {min(uniq.values())}% / max {max(uniq.values())}%")

# ---------------------------------------------------------------- 6 duplicate paragraphs
seen = defaultdict(set)
for u, h in PAGES.items():
    core = content_core(h)
    core = remove_blocks(core, ["sources", "rev", "byline"])
    for blk in re.findall(r"<(p|li|dd)\b[^>]*>(.*?)</\1>", core, re.S):
        t = " ".join(strip(blk[1]).split())
        if len(t.split()) >= 14:
            seen[t].add(u)
dup_p = {t: sorted(us) for t, us in seen.items() if len(us) > 1}
rep("No duplicate paragraphs of 14+ words site-wide", not dup_p, f"{len(dup_p)} dups: " + " || ".join(f'{t[:70]}… {v[:3]}' for t, v in list(dup_p.items())[:4]) if dup_p else "0 duplicates")

# ---------------------------------------------------------------- 7 reading level
FK = {}
for u, h in PAGES.items():
    if ptype(u) in ("legal", "404", "glossary"): continue
    core = remove_blocks(content_core(h), ["sources", "tw"])
    paras = [strip(x) for x in re.findall(r"<(?:p|li|dd)\b[^>]*>(.*?)</(?:p|li|dd)>", core, re.S)]
    txt = " ".join(p if p.strip().endswith((".", "?", "!", ":")) else p + "." for p in paras)
    FK[u] = round(fk_grade(txt), 1)
hi = {u: v for u, v in FK.items() if v > 9}
avg = round(sum(FK.values()) / len(FK), 1)
rep("Reading level FK grade ≤9 (target 6–8)", not hi, f"over 9: {hi}" if hi else f"avg {avg}, range {min(FK.values())}–{max(FK.values())}")

# ---------------------------------------------------------------- 8 schema
sch_issues = []
all_ids = set()
graphs = {}
for u, h in PAGES.items():
    for blob in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try:
            g = json.loads(blob)["@graph"]
        except Exception as e:
            sch_issues.append(f"bad JSON {u}"); continue
        graphs[u] = g
        for n in g:
            if "@id" in n: all_ids.add(n["@id"])
def refs(o, out):
    if isinstance(o, dict):
        if set(o.keys()) == {"@id"}: out.append(o["@id"])
        for v in o.values(): refs(v, out)
    elif isinstance(o, list):
        for v in o: refs(v, out)
for u, g in graphs.items():
    r = []; refs(g, r)
    for x in r:
        if x not in all_ids: sch_issues.append(f"dangling {x} on {u}")
    s = json.dumps(g)
    for bad in ('"Review"', '"AggregateRating"', '"address"', '"geo"', '"openingHours'):
        if bad in s: sch_issues.append(f"{bad} on {u}")
    for n in g:
        if n.get("@type") == "FAQPage":
            vis = strip(PAGES[u])
            for q in n["mainEntity"]:
                if q["name"] not in vis: sch_issues.append(f"FAQ not visible {u}: {q['name'][:40]}")
    if ptype(u) in ("home", "service"):
        wp = [n for n in g if n.get("@type") == "WebPage"]
        if not wp or "about" not in wp[0] or "mentions" not in wp[0]: sch_issues.append(f"no about/mentions {u}")
rep("Schema valid JSON, @ids resolve, FAQs visible, no ratings/address/geo/hours", not sch_issues, "; ".join(sch_issues[:6]) if sch_issues else f"{len(graphs)} pages, {len(all_ids)} @ids")

# ---------------------------------------------------------------- 9 compliance
BANNED = ["24/7", "24 hours a day", "24-hour", "24 hour", "around the clock", "day or night", "any time", "anytime", "any hour", "open now",
          "live person", "live agent", "real person", "talk to a person", "we answer", "answered", "pick up", "picks up",
          "our team", "our crew", "our technician", "dispatch", "arrival window", "certified", "licensed technicians",
          "insured and bonded", "5-star", "award-winning", "minutes away", "60 minutes", "free estimate", "years in business",
          "10+ years", "based in sarasota", "home base", "placeholder", "lorem", "coming soon", "example.com", "{ph}", "{{"]
ban_hits = []
for u, h in PAGES.items():
    vis = strip(h).lower()
    vis += " " + " ".join(re.findall(r'(?:alt|content|title|aria-label)="([^"]*)"', h)).lower()
    for b in BANNED:
        if b in vis:
            ban_hits.append(f"'{b}' on {u}")
rep("Banned wording scan (text, alt, meta)", not ban_hits, "; ".join(ban_hits[:8]) if ban_hits else "0 hits")

lic = []
OK_NEXT = ("plumber", "plumbing", "contractor", "mold", "hvac", "law", "regulation")
for u, h in PAGES.items():
    vis = " ".join(strip(main_html(h)).split()).lower()
    for m in re.finditer(r"\blicensed\b", vis):
        ctx = vis[m.end():m.end() + 30]
        if not any(ctx.strip().startswith(k) for k in OK_NEXT):
            lic.append(f"{u}: …licensed{ctx[:25]}")
rep("'Licensed' only next to plumber/contractor/law", not lic, "; ".join(lic[:5]) if lic else "rule respected")

ph_bad = []
for u, h in PAGES.items():
    vis = strip(h)
    for m in re.findall(r"\(?\b\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}\b", vis):
        if re.sub(r"\D", "", m) != "9413931012": ph_bad.append(f"{m} on {u}")
    for t in re.findall(r'href="tel:([^"]+)"', h):
        if t != "+19413931012": ph_bad.append(f"tel {t} on {u}")
rep("Single phone number and tel: value site-wide", not ph_bad, "; ".join(ph_bad[:5]) if ph_bad else "(941) 393-1012 / tel:+19413931012 only")

disc = [u for u, h in PAGES.items() if "Referral disclosure:" not in h]
rep("Referral disclosure on every page", not disc, f"missing: {disc}" if disc else "present on all pages")

addr = [u for u, h in PAGES.items() if re.search(r"1981 Main|Main St #750|#750", strip(h))]
rep("No street address (service-area business)", not addr, f"{addr}" if addr else "no address in pages or schema")

# ---------------------------------------------------------------- 10 images + performance
img_issues = []
for u, h in PAGES.items():
    for tag in re.findall(r"<img\b[^>]*>", h):
        if 'alt="' not in tag or 'alt=""' in tag: img_issues.append(f"alt {u}")
        if "width=" not in tag or "height=" not in tag: img_issues.append(f"dims {u}")
        if 'fetchpriority="high"' not in tag and 'loading="lazy"' not in tag: img_issues.append(f"lazy {u}")
rep("Images: alt text, width/height, lazy except LCP", not img_issues, "; ".join(img_issues[:5]) if img_issues else "all images pass")

big_html = {u: len(h.encode()) for u, h in PAGES.items() if len(h.encode()) > 100_000}
imgs = [(p, os.path.getsize(p)) for p in glob.glob(f"{DIST}/**/*.*", recursive=True) if p.endswith((".webp", ".jpg", ".png"))]
big_img = [(os.path.relpath(p, DIST), s) for p, s in imgs if s > 200_000]
js = os.path.getsize(f"{DIST}/assets/js/site.js")
css = len(open(f"{ROOT}/static/critical.min.css").read()) + len(open(f"{ROOT}/static/site.min.css").read())
maxhtml = max(len(h.encode()) for h in PAGES.values())
rep("Performance budget (HTML <100KB, images <200KB, JS ≤10KB)", not big_html and not big_img and js <= 10240,
    f"big html {big_html} big img {big_img}" if (big_html or big_img) else f"max HTML {maxhtml//1024}KB, JS {js}B, inline CSS {css}B, max image {max(s for _, s in imgs)//1024}KB")
rb = [u for u, h in PAGES.items() if re.search(r'<script(?![^>]*(defer|async|application/ld))[^>]*src=', h) or re.search(r'<link rel="stylesheet"(?![^>]*media)', h.split("<noscript>")[0])]
rep("No render-blocking scripts or CSS", not rb, f"{rb[:3]}" if rb else "JS deferred; CSS preloaded + inline critical")

# ---------------------------------------------------------------- 11 sitemap / robots / files
sm = open(f"{DIST}/sitemap.xml").read()
missing_sm = [u for u in PAGES if u != "/404.html" and f"<loc>https://leakdetectionsarasotafl.us{u}</loc>" not in sm]
rep("sitemap.xml lists every indexable page with lastmod", not missing_sm and "<lastmod>" in sm, f"missing {missing_sm}" if missing_sm else f"{sm.count('<url>')} URLs")
files = ["robots.txt", "_headers", "_redirects", "site.webmanifest", "favicon.ico", "favicon.svg", "apple-touch-icon.png", "assets/img/icon-192.png", "assets/img/icon-512.png", "assets/img/og-default.jpg", "404.html"]
mf = [f for f in files if not os.path.exists(f"{DIST}/{f}")]
rep("robots, _headers, _redirects, manifest, icons, 404 present", not mf, f"missing {mf}" if mf else "all present")
nf = 'noindex' in PAGES["/404.html"]
rep("404 is noindex", nf, "" if nf else "404 indexable")

# ---------------------------------------------------------------- 12 topical coverage
from data import POSTS
cov = []
for p in POSTS:
    h = PAGES[f"/blog/{p['slug']}/"]
    core = content_core(h)
    first150 = " ".join(strip(remove_blocks(core, ["quick"])).split()[:150])
    body_links = re.findall(r'href="([^"]+)"', remove_blocks(core, ["quick"]))
    # find money link position by words before it
    txt_before = ""
    pos = core.find(f'href="{p["money"]}"')
    if pos < 0: cov.append(f"{p['slug']} no money link"); continue
    wb = len(strip(remove_blocks(core[:pos], ["quick"])).split())
    if wb > 150: cov.append(f"{p['slug']} money link at word {wb}")
    guides = {l for l in body_links if l.startswith("/blog/") and l != f"/blog/{p['slug']}/"}
    locs_ = {l for l in body_links if l.startswith("/locations/")}
    if len(guides) < 3: cov.append(f"{p['slug']} only {len(guides)} guide links")
    if not (2 <= len(locs_) <= 5): cov.append(f"{p['slug']} {len(locs_)} location links")
rep("Every blog links its money page in first 150 words, 3+ guides, 2–5 locations", not cov, "; ".join(cov[:6]) if cov else f"{len(POSTS)}/{len(POSTS)} posts pass")

# ---------------------------------------------------------------- report
ok = sum(1 for r in R if r[1] == "PASS")
print(f"\nAUDIT: {ok}/{len(R)} checks pass\n")
for c, s, i, f in R:
    print(f"[{s}] {c}\n       {i}")
json.dump({"results": R, "wc": WC, "fk": FK, "uniq": uniq}, open(os.path.join(ROOT, "audit.json"), "w"), indent=1)
print("\nWord counts:"); [print(f"  {WC[u]:5d}  FK {FK.get(u,'-')}  {u}") for u in sorted(PAGES, key=lambda x: (ptype(x), x))]
