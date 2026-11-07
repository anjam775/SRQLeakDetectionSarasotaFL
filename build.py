#!/usr/bin/env python3
"""SRQ Leak Pros static site generator -> dist/"""
import html, json, os, re, shutil, sys, importlib, glob
import markdown

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "content"))
from data import SITE, WIKI, SRC, SERVICES, LOCATIONS, POSTS, BLOG_CATS
from glossary import TERMS

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")
U = SITE["url"]
TEL = SITE["phone_tel"]
PH = SITE["phone_display"]
NAME = SITE["name"]
TODAY = SITE["today"]
import datetime as _dt
def human(d):
    x = _dt.date.fromisoformat(d); return f"{x:%B} {x.day}, {x.year}"

SVC = {s["slug"]: s for s in SERVICES}
LOC = {l["slug"]: l for l in LOCATIONS}
POST = {p["slug"]: p for p in POSTS}

# ---------------------------------------------------------------- loading pages
PAGES = []  # list of dicts
for mod in ["home", "services_a", "services_b", "locations", "posts_a", "posts_b", "posts_c", "posts_d", "posts_e", "support"]:
    m = importlib.import_module(mod)
    PAGES.extend(m.PAGES)
BY_URL = {p["url"]: p for p in PAGES}
for p in PAGES:
    if p["type"] == "post":
        POST[p["slug"]].update({"title": p["h1"], "card": p["card"], "url": p["url"], "date": p.get("date", SITE["launch"])})

# ---------------------------------------------------------------- helpers
def esc(s):
    return html.escape(s, quote=True)

def attr(s):
    return html.escape(s, quote=True)

ICONS = {
    "phone": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z"/></svg>',
    "line": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 14h6v-3h6v3h6v4H3z" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 3v5" stroke="currentColor" stroke-width="2"/><path d="M12 8c-1.5 2-2 3-2 4a2 2 0 0 0 4 0c0-1-.5-2-2-4z"/></svg>',
    "swap": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 8h13l-3-3m6 11H7l3 3" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "slab": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 10l9-6 9 6v2H3z"/><rect x="3" y="15" width="18" height="4" rx="1" fill="none" stroke="currentColor" stroke-width="2"/><path d="M8 17h8" stroke="currentColor" stroke-width="2" stroke-dasharray="2 2"/></svg>',
    "search": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10" cy="10" r="6" fill="none" stroke="currentColor" stroke-width="2"/><path d="M15 15l6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M10 6.5c-1 1.4-1.6 2.3-1.6 3.1a1.6 1.6 0 0 0 3.2 0c0-.8-.6-1.7-1.6-3.1z"/></svg>',
    "bolt": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13 2L4 14h6l-1 8 9-12h-6z"/></svg>',
    "pipes": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 7h8v10h10" fill="none" stroke="currentColor" stroke-width="3" stroke-linejoin="round"/><circle cx="11" cy="7" r="1.6"/><circle cx="11" cy="17" r="1.6"/></svg>',
    "sewer": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M2 12h20" stroke="currentColor" stroke-width="3"/><circle cx="12" cy="12" r="7" fill="none" stroke="currentColor" stroke-width="2"/><path d="M8 16l2-2m4 0l2 2" stroke="currentColor" stroke-width="2"/></svg>',
    "pool": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M2 17c2 0 2-1.5 4-1.5S8 17 10 17s2-1.5 4-1.5 2 1.5 4 1.5 2-1.5 4-1.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M8 14V5a2 2 0 0 1 4 0m2 9V5a2 2 0 0 1 4 0M8 9h6" fill="none" stroke="currentColor" stroke-width="2"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a7 7 0 0 0-7 7c0 5 7 13 7 13s7-8 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z"/></svg>',
    "check": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12l5 5 9-10" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "chev": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg>',
    "menu": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg>',
    "Facebook": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14 8h3V4h-3c-2.8 0-4 1.8-4 4.4V11H7v4h3v9h4v-9h3l1-4h-4V8.6c0-.4.2-.6.6-.6z"/></svg>',
    "Instagram": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="17.5" cy="6.5" r="1.3"/></svg>',
    "X": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 3h4.6l4.1 5.8L17.7 3H20l-6.2 7.2L21 21h-4.6l-4.5-6.3L6.3 21H4l6.9-8z"/></svg>',
    "YouTube": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M22 8.2a3 3 0 0 0-2.1-2.1C18 5.6 12 5.6 12 5.6s-6 0-7.9.5A3 3 0 0 0 2 8.2 31 31 0 0 0 1.6 12 31 31 0 0 0 2 15.8a3 3 0 0 0 2.1 2.1c1.9.5 7.9.5 7.9.5s6 0 7.9-.5a3 3 0 0 0 2.1-2.1 31 31 0 0 0 .4-3.8 31 31 0 0 0-.4-3.8zM10 15V9l5.2 3z"/></svg>',
    "LinkedIn": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9h3.6v11H4zM5.8 3.5a2 2 0 1 1 0 4 2 2 0 0 1 0-4zM10 9h3.4v1.6c.5-.9 1.7-1.9 3.6-1.9 3.8 0 4.5 2.4 4.5 5.6V20h-3.6v-5c0-1.3 0-2.9-1.8-2.9s-2 1.4-2 2.8V20H10z"/></svg>',
}

LOGO_MARK = ('<svg class="mark" viewBox="0 0 48 48" aria-hidden="true">'
             '<rect width="48" height="48" rx="11" fill="#0B2545"/>'
             '<path d="M22 9c-5.5 7.3-9 12.4-9 17a9 9 0 0 0 13.5 7.8" fill="none" stroke="#5EEAD4" stroke-width="4" stroke-linecap="round"/>'
             '<circle cx="28" cy="27" r="7" fill="none" stroke="#F59E0B" stroke-width="4"/>'
             '<path d="M33 32l6 6" stroke="#F59E0B" stroke-width="4.5" stroke-linecap="round"/></svg>')

def logo_html():
    return (f'<a class="logo" href="/" aria-label="{NAME} home">{LOGO_MARK}'
            '<span class="wm"><b>SRQ</b> Leak Pros</span></a>')

def call_btn(cls="btn btn-cta", label=None, loc="body"):
    label = label or f"Call {PH}"
    return f'<a class="{cls}" href="tel:{TEL}" data-call="{loc}">{ICONS["phone"]}<span>{esc(label)}</span></a>'

# ---------------------------------------------------------------- markdown
MD = markdown.Markdown(extensions=["tables", "md_in_html", "attr_list", "sane_lists"])

def md(text):
    text = text.strip("\n")
    def cta(m):
        return ('\n<div class="cta-box auto-cta"><p class="cta-t">' + esc(m.group(1).strip()) + '</p>'
                + call_btn(loc="cta-box") + '</div>\n')
    text = re.sub(r"^:::cta (.+)$", cta, text, flags=re.M)
    def block(m):
        return f'\n<div class="{m.group(1)}" markdown="1">\n\n{m.group(2).strip()}\n\n</div>\n'
    text = re.sub(r"^:::(\w+)\n(.*?)\n:::$", block, text, flags=re.M | re.S)
    MD.reset()
    out = MD.convert(text)
    # external links open in new tab
    out = re.sub(r'<a href="(https?://[^"]+)"', r'<a href="\1" target="_blank" rel="noopener"', out)
    # tables responsive wrapper
    out = out.replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")
    return out

def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def add_heading_ids(h):
    seen = set()
    def rep(m):
        lvl, inner = m.group(1), m.group(2)
        sid = slugify(re.sub("<[^>]+>", "", inner))[:60] or "s"
        base = sid; i = 2
        while sid in seen:
            sid = f"{base}-{i}"; i += 1
        seen.add(sid)
        return f'<h{lvl} id="{sid}">{inner}</h{lvl}>'
    return re.sub(r"<h([23])>(.*?)</h\1>", rep, h)

GL_SORTED = sorted(TERMS, key=lambda t: -len(t["term"]))

def glossary_link(h, max_links=4, skip=()):
    """Link first mention of up to 4 glossary terms, inside <p> only, never inside links."""
    used = 0
    linked = set()
    def process_p(pm):
        nonlocal used
        ptxt = pm.group(0)
        if used >= max_links:
            return ptxt
        for t in GL_SORTED:
            if used >= max_links:
                break
            if t["slug"] in linked or t["slug"] in skip:
                continue
            # split out existing anchors
            parts = re.split(r"(<a\b.*?</a>|<[^>]+>)", ptxt, flags=re.S)
            done = False
            for i, part in enumerate(parts):
                if done or part.startswith("<"):
                    continue
                mm = re.search(r"(?<![\w-])(" + re.escape(t["term"]) + r")(?![\w-])", part, flags=re.I)
                if mm:
                    parts[i] = part[:mm.start()] + f'<a class="gl" href="/glossary/#{t["slug"]}">{mm.group(1)}</a>' + part[mm.end():]
                    done = True
            if done:
                ptxt = "".join(parts)
                linked.add(t["slug"])
                used += 1
        return ptxt
    h = re.sub(r"<p>(?!<strong>(?:Quick answer|Short answer))(.*?)</p>", process_p, h, flags=re.S)
    return h, linked

# ---------------------------------------------------------------- layout parts
def nav_html():
    svc = "".join(f'<li><a href="/services/{s["slug"]}/">{esc(s["name"])}</a></li>' for s in SERVICES)
    loc = "".join(f'<li><a href="/locations/{l["slug"]}/">{esc(l["name"])}</a></li>' for l in LOCATIONS)
    return f'''<nav class="nav" id="nav" aria-label="Main">
<ul class="menu">
<li class="has-sub"><a href="/services/" class="top">Services</a><button class="sub-tg" aria-expanded="false" aria-label="Show services">{ICONS["chev"]}</button><ul class="sub">{svc}<li class="all"><a href="/services/">All services</a></li></ul></li>
<li class="has-sub"><a href="/locations/" class="top">Locations</a><button class="sub-tg" aria-expanded="false" aria-label="Show locations">{ICONS["chev"]}</button><ul class="sub">{loc}<li class="all"><a href="/locations/">All areas</a></li></ul></li>
<li><a href="/blog/" class="top">Blog</a></li>
<li><a href="/about/" class="top">About</a></li>
<li><a href="/contact/" class="top">Contact</a></li>
</ul></nav>'''

def header_html():
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="hdr"><div class="wrap hdr-in">
{logo_html()}
<button class="menu-tg" aria-controls="nav" aria-expanded="false">{ICONS["menu"]}<span>Menu</span></button>
{nav_html()}
<a class="btn btn-cta hdr-call" href="tel:{TEL}" data-call="header">{ICONS["phone"]}<span>{PH}</span></a>
</div></header>'''

DISCLOSURE = (f"Referral disclosure: {NAME} is a referral service and does not perform leak detection, plumbing, "
              "sewer, pool or repair work. Calls may be connected to independent, participating local service providers "
              "and may be recorded for quality and training. Providers are responsible for their own licenses, insurance, "
              f"pricing and work. {NAME} may be compensated when calls are connected.")

def footer_html():
    svc = "".join(f'<li><a href="/services/{s["slug"]}/">{esc(s["name"])}</a></li>' for s in SERVICES)
    loc = "".join(f'<li><a href="/locations/{l["slug"]}/">{esc(l["name"])}</a></li>' for l in LOCATIONS)
    soc = "".join(f'<a href="{u}" target="_blank" rel="noopener" aria-label="{n}">{ICONS[n]}</a>' for n, u in SITE["social"])
    return f'''<footer class="ftr"><div class="wrap ftr-grid">
<div class="ftr-brand">{logo_html()}
<p>{NAME} connects homeowners in Sarasota, Sarasota County and nearby Manatee County with independent local providers for leak detection, water line, sewer and pool leak work.</p>
<p class="ftr-area"><strong>Service area:</strong> Sarasota and nearby communities. Service-area business; no walk-in office.</p>
<p><a class="ftr-phone" href="tel:{TEL}" data-call="footer">{ICONS["phone"]}{PH}</a></p>
<div class="soc">{soc}</div></div>
<div><h2 class="fh">Services</h2><ul>{svc}</ul></div>
<div><h2 class="fh">Areas</h2><ul><li><a href="/">Sarasota</a></li>{loc}</ul></div>
<div><h2 class="fh">Company</h2><ul><li><a href="/about/">About</a></li><li><a href="/contact/">Contact</a></li><li><a href="/blog/">Blog</a></li><li><a href="/glossary/">Glossary</a></li><li><a href="/disclaimer/">Disclaimer</a></li><li><a href="/editorial-policy/">Editorial policy</a></li><li><a href="/privacy-policy/">Privacy policy</a></li><li><a href="/terms/">Terms</a></li><li><a href="/accessibility/">Accessibility</a></li></ul></div>
</div>
<div class="wrap ftr-legal"><p class="disc">{esc(DISCLOSURE)} <a href="/disclaimer/">Read the full disclaimer</a>.</p>
<p>&copy; <span data-y>2026</span> {NAME}. General information only, not professional advice.</p></div>
</footer>
<div class="sticky-call"><a href="tel:{TEL}" data-call="sticky">{ICONS["phone"]}<span>Call {PH}</span></a></div>'''

def crumbs_html(trail):
    items = []
    for i, (name, url) in enumerate(trail):
        if i == len(trail) - 1:
            items.append(f'<li aria-current="page">{esc(name)}</li>')
        else:
            items.append(f'<li><a href="{url}">{esc(name)}</a></li>')
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{"".join(items)}</ol></nav>'

def call_band(text=None):
    text = text or f"Leak, wet spot or a water bill that keeps climbing? Call to reach a local leak pro in the Sarasota area."
    return f'''<section class="band auto"><div class="wrap band-in"><p class="band-t">{esc(text)}</p>{call_btn(loc="band")}</div></section>'''

def svc_cards(slugs, h_tag="h3"):
    out = []
    for s in slugs:
        sv = SVC[s]
        out.append(f'<a class="card" href="/services/{s}/"><span class="ic">{ICONS[sv["icon"]]}</span><{h_tag} class="ct">{esc(sv["name"])}</{h_tag}><p>{esc(sv["card"])}</p></a>')
    return '<div class="cards">' + "".join(out) + "</div>"

def loc_cards(slugs, h_tag="h3"):
    out = []
    for s in slugs:
        l = LOC[s]
        out.append(f'<a class="card" href="/locations/{s}/"><span class="ic">{ICONS["pin"]}</span><{h_tag} class="ct">{esc(l["name"])}</{h_tag}><p>{esc(l["card"])}</p></a>')
    return '<div class="cards">' + "".join(out) + "</div>"

def post_cards(slugs, h_tag="h3"):
    out = []
    for s in slugs:
        p = POST[s]
        out.append(f'<a class="card pc" href="/blog/{s}/"><img src="/assets/img/blog/{s}-600.webp" width="600" height="315" alt="{attr(p["title"])} guide graphic" loading="lazy" decoding="async"><span class="cat">{esc(p["cat"])}</span><{h_tag} class="ct">{esc(p["title"])}</{h_tag}><p>{esc(p["card"])}</p></a>')
    return '<div class="cards">' + "".join(out) + "</div>"

def pills(items):
    return '<ul class="pills">' + "".join(f'<li><a href="{u}">{esc(n)}</a></li>' for n, u in items) + "</ul>"

def sources_html(keys, extra_note=True):
    li = "".join(f'<li><a href="{SRC[k][1]}" target="_blank" rel="noopener">{esc(SRC[k][0])}</a></li>' for k in keys)
    note = (f'<p class="rev">Last reviewed {SITE["today_human"]}. This page is general information, not professional advice. '
            'See the <a href="/editorial-policy/">editorial policy</a> for how pages are researched and updated.</p>') if extra_note else ""
    return f'<section class="sources"><h2 id="sources">Sources</h2><ol>{li}</ol>{note}</section>'

def faq_html(faqs, title="Frequently asked questions"):
    items = "".join(f'<div class="qa"><h3>{esc(q)}</h3><p>{a}</p></div>' for q, a in faqs)
    return f'<section class="faq"><h2 id="faq">{esc(title)}</h2>{items}</section>'

# ---------------------------------------------------------------- schema
def ent(key):
    n, u = WIKI[key]
    return {"@type": "Thing", "name": n, "sameAs": u}

def org_nodes():
    return [
        {"@type": "Organization", "@id": U + "/#org", "name": NAME, "url": U + "/",
         "logo": {"@type": "ImageObject", "url": U + "/assets/img/logo-512.png", "width": 512, "height": 512},
         "telephone": TEL, "publishingPrinciples": U + "/editorial-policy/",
         "sameAs": []},
        {"@type": "WebSite", "@id": U + "/#website", "url": U + "/", "name": NAME, "inLanguage": "en-US",
         "publisher": {"@id": U + "/#org"}},
    ]

def business_node():
    return {"@type": "ProfessionalService", "@id": U + "/#business", "name": NAME, "url": U + "/",
            "description": f"{NAME} is a referral service that connects homeowners in Sarasota and nearby areas with independent local providers for leak detection, water service line, slab leak, sewer line and pool leak work.",
            "telephone": TEL, "image": U + "/assets/img/og-default.jpg", "logo": U + "/assets/img/logo-512.png",
            "parentOrganization": {"@id": U + "/#org"},
            "areaServed": area_served(),
            "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Leak and water line services",
                                "itemListElement": [{"@type": "Offer", "itemOffered": {"@id": f"{U}/services/{s['slug']}/#service"}} for s in SERVICES]}}

def area_served():
    a = [{"@type": "City", "name": "Sarasota", "sameAs": WIKI["sarasota"][1]},
         {"@type": "AdministrativeArea", "name": "Sarasota County", "sameAs": WIKI["sarasota_county"][1]},
         {"@type": "AdministrativeArea", "name": "Manatee County", "sameAs": WIKI["manatee_county"][1]}]
    for l in LOCATIONS:
        a.append({"@type": "City" if l["type"] in ("City", "Town") else "Place", "name": l["full"], "sameAs": WIKI[l["wiki"]][1]})
    return a

def breadcrumb_node(url, trail):
    return {"@type": "BreadcrumbList", "@id": U + url + "#breadcrumb",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": U + u} for i, (n, u) in enumerate(trail)]}

def faq_node(url, faqs):
    return {"@type": "FAQPage", "@id": U + url + "#faq", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}} for q, a in faqs]}

def webpage_node(p, ptype="WebPage"):
    n = {"@type": ptype, "@id": U + p["url"] + "#webpage", "url": U + p["url"], "name": p["title"],
         "description": p["meta"], "inLanguage": "en-US", "isPartOf": {"@id": U + "/#website"},
         "dateModified": TODAY}
    if p.get("about"):
        n["about"] = [{"@id": U + "/#business"}] + [ent(k) for k in p["about"]]
    if p.get("mentions"):
        n["mentions"] = [ent(k) for k in p["mentions"]]
    if p.get("sources"):
        n["citation"] = [SRC[k][1] for k in p["sources"]]
    if p.get("trail"):
        n["breadcrumb"] = {"@id": U + p["url"] + "#breadcrumb"}
    return n

def service_node(p, sv, area=None):
    n = {"@type": "Service", "@id": U + p["url"] + "#service", "name": p["h1"], "serviceType": sv["serviceType"],
         "description": p["meta"], "url": U + p["url"], "provider": {"@id": U + "/#business"},
         "availableChannel": {"@type": "ServiceChannel", "servicePhone": {"@type": "ContactPoint", "telephone": TEL, "contactType": "customer service"}}}
    n["areaServed"] = area if area else area_served()
    return n

# ---------------------------------------------------------------- page assembly
CSS_CRIT = open(os.path.join(ROOT, "static", "critical.min.css")).read() + open(os.path.join(ROOT, "static", "site.min.css")).read()

def head_html(p, robots="index,follow"):
    img = p.get("og_image", "/assets/img/og-default.jpg")
    og_type = "article" if p["type"] == "post" else "website"
    extra = ""
    if p["type"] == "post":
        extra = f'<meta property="article:published_time" content="{p.get("date", SITE["launch"])}"><meta property="article:modified_time" content="{TODAY}">'
    canon = U + p["url"] if p["url"] != "/404.html" else U + "/404.html"
    preload = p.get("preload", "")
    return f'''<!doctype html><html lang="en-US"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(p["title"])}</title>
<meta name="description" content="{attr(p["meta"])}">
<link rel="canonical" href="{canon}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="{SITE["theme"]}">
<meta property="og:type" content="{og_type}"><meta property="og:site_name" content="{NAME}"><meta property="og:title" content="{attr(p["title"])}"><meta property="og:description" content="{attr(p["meta"])}"><meta property="og:url" content="{canon}"><meta property="og:image" content="{U}{img}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:locale" content="en_US">{extra}
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{attr(p["title"])}"><meta name="twitter:description" content="{attr(p["meta"])}"><meta name="twitter:image" content="{U}{img}">
<link rel="icon" href="/favicon.ico" sizes="32x32"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/apple-touch-icon.png"><link rel="manifest" href="/site.webmanifest">
{preload}<link rel="preconnect" href="https://www.googletagmanager.com" crossorigin><script async src="https://www.googletagmanager.com/gtag/js?id={SITE["ga4"]}"></script>
<style>{CSS_CRIT}</style>
<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": p["_schema"]}, ensure_ascii=False, separators=(",", ":"))}</script>
</head>'''

def page_html(p, main_html, robots="index,follow"):
    return (head_html(p, robots) + f'<body class="t-{p["type"]}">' + header_html() +
            f'<main id="main">{main_html}</main>' + footer_html() +
            '<script src="/assets/js/site.js" defer></script></body></html>')

def hero(p, chips=None, inner_lead=True, kicker=None):
    chips_html = ""
    if chips:
        chips_html = '<ul class="chips">' + "".join(f'<li>{ICONS["check"]}{esc(c)}</li>' for c in chips) + "</ul>"
    k = f'<p class="kicker">{esc(kicker)}</p>' if kicker else ""
    crumbs = crumbs_html(p["trail"]) if p.get("trail") else ""
    return f'''<section class="hero"><div class="wrap">{crumbs}{k}<h1>{esc(p["h1"])}</h1>
<p class="lead">{p["lead"]}</p><div class="hero-cta">{call_btn(loc="hero")}</div>{chips_html}</div></section>'''

CHIPS = ["Sarasota & Manatee counties", "Service lines, slabs, sewers & pools", "Homes, condos & businesses", "Independent local providers"]


from figures import FIGS
def add_figures(url, body):
    for heading, name, alt, cap, (who, link) in FIGS.get(url, []):
        m = re.search(r'<h2[^>]*>' + re.escape(esc(heading)) + r'</h2>', body)
        if not m:
            raise SystemExit(f"figure heading not found on {url}: {heading}")
        # Float the photo beside text when enough text follows it; otherwise use a compact side-by-side card.
        nxt = body.find("<h2", m.end()); nxt = len(body) if nxt < 0 else nxt
        def text_run(start):
            stops = [body.find(t, start) for t in ('<div class="tw"', '<div class="cta-box"', '<table', '<div class="cards"', '<h2')]
            end = min([s for s in stops if s >= 0] + [len(body)])
            return len(re.sub(r"<[^>]+>", "", body[start:end]))
        p_end = body.find("</p>", m.end())
        cands = ([p_end + 4] if 0 <= p_end < nxt else []) + [m.end()]
        at = next((c for c in cands if text_run(c) >= 900), None)
        layout = "fig"
        if at is None:
            layout = "fig fig-row"
            at = cands[0]
        src = f"/assets/img/pages/{name}"
        fig = (f'<figure class="{layout}"><img src="{src}.webp" srcset="{src}-600.webp 600w, {src}.webp 1200w" '
               f'sizes="(max-width: 899px) 92vw, 420px" width="1200" height="675" loading="lazy" decoding="async" '
               f'alt="{esc(alt)}"><figcaption>{esc(cap)} <span class="credit">Photo: <a href="{link}" target="_blank" rel="noopener">{esc(who)}</a> / Pexels</span></figcaption></figure>')
        body = body[:at] + fig + body[at:]
    return body

def render(p):
    t = p["type"]
    raw = p.get("body", "").replace("{PH}", PH)
    body = add_heading_ids(md(raw))
    skip = set(p.get("gl_skip", []))
    if t not in ("legal", "glossary", "hub", "contact", "404"):
        body, _ = glossary_link(body, skip=skip)
    body = body.replace("<p>{{SERVICES}}</p>", svc_cards([s["slug"] for s in SERVICES]))
    body = body.replace("<p>{{LOCATIONS}}</p>", loc_cards([l["slug"] for l in LOCATIONS]))
    body = re.sub(r"<p>\{\{POSTS:([^}]+)\}\}</p>", lambda m: post_cards(m.group(1).split(",")), body)
    body = add_figures(p["url"], body)
    schema = org_nodes()
    tail = ""
    if t == "home":
        schema += [business_node(), webpage_node(p)]
        if p.get("faqs"):
            schema.append(faq_node(p["url"], p["faqs"]))
        src = sources_html(p["sources"]) if p.get("sources") else ""
        main = hero(p, CHIPS, kicker="Leak detection & water line help") + f'<div class="wrap content">{body}{faq_html(p["faqs"], "Leak detection questions")}{src}</div>' + call_band()
    elif t == "service":
        sv = SVC[p["slug"]]
        schema += [webpage_node(p), service_node(p, sv), breadcrumb_node(p["url"], p["trail"]), faq_node(p["url"], p["faqs"])]
        rel = p["related"]
        guides = p["guides"]
        near = [(f'{sv["short"]} in {l["name"]}', f'/locations/{l["slug"]}/') for l in LOCATIONS]
        near = [(f'{sv["short"]} in Sarasota', "/")] + near
        tail = (faq_html(p["faqs"], f'{sv["name"]} questions') + sources_html(p["sources"]) +
                f'<section class="auto"><h2>Related leak and water line services</h2>{svc_cards(rel)}</section>'
                f'<section class="auto"><h2>{esc(sv["name"])} near you</h2>{pills(near)}</section>'
                f'<section class="auto"><h2>Helpful guides</h2>{post_cards(guides)}</section>')
        main = hero(p, CHIPS[:3] + ["Independent local providers"]) + f'<div class="wrap content">{body}{tail}</div>' + call_band(p.get("band"))
    elif t == "location":
        l = LOC[p["slug"]]
        area = [{"@type": "City" if l["type"] in ("City", "Town") else "Place", "name": l["full"], "sameAs": WIKI[l["wiki"]][1],
                 "containedInPlace": {"@type": "AdministrativeArea", "name": l["county"] if "and" not in l["county"] else "Sarasota County",
                                      "sameAs": WIKI["manatee_county" if l["county"] == "Manatee County" else "sarasota_county"][1]}}]
        schema += [webpage_node(p), service_node(p, {"serviceType": "Leak detection and water line repair referral"}, area),
                   breadcrumb_node(p["url"], p["trail"]), faq_node(p["url"], p["faqs"])]
        near = [("Leak detection in Sarasota", "/")] + [(f'Leak detection in {LOC[s]["name"]}', f"/locations/{s}/") for s in l["nearby"]] + [("All service areas", "/locations/")]
        tail = (faq_html(p["faqs"], f'Leak detection in {l["name"]}: questions') +
                (sources_html(p["sources"]) if p.get("sources") else "") +
                f'<section class="auto"><h2>Leak detection and water line services in {esc(l["name"])}</h2>{svc_cards([s["slug"] for s in SERVICES])}</section>'
                f'<section class="auto"><h2>Nearby areas covered</h2>{pills(near)}</section>')
        main = hero(p, [l["county"], f'ZIP {l["zips"]}', "Homes, condos & businesses", "Independent local providers"]) + f'<div class="wrap content">{body}{tail}</div>' + call_band(p.get("band"))
    elif t == "post":
        post = POST[p["slug"]]
        img = f"/assets/img/blog/{p['slug']}"
        p["og_image"] = img + ".jpg"
        p["preload"] = f'<link rel="preload" as="image" href="{img}.webp" fetchpriority="high">\n'
        schema += [webpage_node(p), breadcrumb_node(p["url"], p["trail"]), faq_node(p["url"], p["faqs"]),
                   {"@type": "BlogPosting", "@id": U + p["url"] + "#post", "headline": p["h1"], "description": p["meta"],
                    "image": {"@type": "ImageObject", "url": U + img + ".jpg", "width": 1200, "height": 630},
                    "datePublished": p.get("date", SITE["launch"]), "dateModified": TODAY, "inLanguage": "en-US",
                    "author": {"@type": "Organization", "name": SITE["editorial"], "url": U + "/editorial-policy/"},
                    "publisher": {"@id": U + "/#org"}, "mainEntityOfPage": {"@id": U + p["url"] + "#webpage"},
                    "wordCount": 0, "articleSection": post["cat"],
                    "citation": [SRC[k][1] for k in p["sources"]]}]
        mins = "{mins}"
        head = f'''<header class="post-hd wrap narrow">{crumbs_html(p["trail"])}<p class="kicker">{esc(post["cat"])}</p><h1>{esc(p["h1"])}</h1>
<p class="byline">By <a href="/editorial-policy/">{SITE["editorial"]}</a> · Published <time datetime="{p.get("date", SITE["launch"])}">{human(p.get("date", SITE["launch"]))}</time> · Updated <time datetime="{TODAY}">{SITE["today_human"]}</time> · {mins} min read</p>
<img class="feat" src="{img}.webp" width="1200" height="630" alt="{attr(p["h1"])} guide graphic" fetchpriority="high" decoding="async"></header>'''
        author = (f'<aside class="author"><h2>About this article</h2><p>Written by {SITE["editorial"]} and checked against the sources listed above. '
                  f'Last updated {SITE["today_human"]}. General information, not legal, insurance or professional advice. '
                  'Read the <a href="/editorial-policy/">editorial policy</a> and the <a href="/disclaimer/">disclaimer</a>.</p></aside>')
        tail = (faq_html(p["faqs"]) + sources_html(p["sources"], extra_note=False) + author +
                f'<section class="auto"><h2>Related guides</h2>{post_cards(post["related"])}</section>')
        main = head + f'<article class="wrap narrow content post">{body}{tail}</article>' + call_band(p.get("band"))
    elif t == "hub":
        schema += [webpage_node(p, "CollectionPage"), breadcrumb_node(p["url"], p["trail"])]
        if p.get("blog"):
            schema.append({"@type": "Blog", "@id": U + "/blog/#blog", "name": f"{NAME} Blog", "url": U + "/blog/",
                           "publisher": {"@id": U + "/#org"},
                           "blogPost": [{"@id": f'{U}/blog/{x["slug"]}/#post'} for x in POSTS]})
        main = hero(p) + f'<div class="wrap content">{body}{p.get("html", "")}</div>' + call_band()
    elif t == "glossary":
        schema += [webpage_node(p), breadcrumb_node(p["url"], p["trail"]),
                   {"@type": "DefinedTermSet", "@id": U + "/glossary/#terms", "name": f"{NAME} leak and water line glossary",
                    "hasDefinedTerm": [{"@type": "DefinedTerm", "@id": f'{U}/glossary/#{x["slug"]}', "name": x["term"].capitalize() if x["term"].islower() else x["term"],
                                        "description": x["def"], "inDefinedTermSet": {"@id": U + "/glossary/#terms"},
                                        "url": f'{U}/glossary/#{x["slug"]}'} for x in TERMS]}]
        main = hero(p) + f'<div class="wrap content">{body}{p["html"]}</div>' + call_band()
    else:  # legal, contact, about, 404
        schema += [webpage_node(p)]
        if p.get("trail"):
            schema.append(breadcrumb_node(p["url"], p["trail"]))
        if p.get("faqs"):
            schema.append(faq_node(p["url"], p["faqs"]))
        faq = faq_html(p["faqs"]) if p.get("faqs") else ""
        main = hero(p) + f'<div class="wrap content narrow">{body}{faq}</div>' + (call_band() if t != "404" else "")
    p["_schema"] = schema
    return main

def finalize(p, main):
    robots = "noindex,follow" if p["type"] == "404" else "index,follow"
    doc = page_html(p, main, robots)
    # word count for posts + minutes
    if p["type"] == "post":
        art = re.search(r'<article.*?</article>', doc, re.S).group(0)
        art = re.sub(r'<section class="auto">.*?</section>', "", art, flags=re.S)
        words = len(re.sub(r"<[^>]+>", " ", art).split())
        doc = doc.replace('"wordCount":0', f'"wordCount":{words}').replace("{mins}", str(max(1, round(words / 230))))
    return doc

def minify(h):
    h = re.sub(r">\s+<", "><", h)
    h = re.sub(r"\n\s*", "\n", h)
    return h

def write(path, content, mode="w"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, mode) as f:
        f.write(content)

def build():
    if os.path.exists(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST)
    # static assets
    shutil.copytree(os.path.join(ROOT, "static", "public"), DIST, dirs_exist_ok=True)
    for p in PAGES:
        main = render(p)
        doc = minify(finalize(p, main))
        out = os.path.join(DIST, "404.html") if p["url"] == "/404.html" else os.path.join(DIST, p["url"].strip("/"), "index.html")
        write(out, doc)
    # sitemap
    pri = {"home": "1.0", "service": "0.9", "hub": "0.8", "location": "0.8", "post": "0.7", "glossary": "0.6"}
    urls = []
    for p in PAGES:
        if p["type"] == "404":
            continue
        urls.append(f'<url><loc>{U}{p["url"]}</loc><lastmod>{TODAY}</lastmod><priority>{pri.get(p["type"], "0.5")}</priority></url>')
    write(os.path.join(DIST, "sitemap.xml"), '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n")
    write(os.path.join(DIST, "robots.txt"), f"User-agent: *\nAllow: /\n\nSitemap: {U}/sitemap.xml\n")
    print(f"Built {len(PAGES)} pages -> {DIST}")

if __name__ == "__main__":
    build()
