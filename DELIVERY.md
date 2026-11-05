# SRQ Leak Pros — Delivery Report

Site: **https://leakdetectionsarasotafl.us** · Brand: **SRQ Leak Pros** · Phone: **(941) 541-0938** (`tel:+19415410938`) · Built November 04, 2026

Model: LeadSmart-compatible **referral voice**, service-area business (no address shown), no hours, no email, no licenses or reviews, no placeholders. Social icons link to platform homepages (owner request; replace with real profile URLs later).

## 1. Folder tree

```
site/                      ← deploy this folder (Cloudflare Pages output dir)
├── index.html             Home: Leak Detection in Sarasota, FL
├── 404.html               noindex
├── _headers  _redirects  robots.txt  sitemap.xml  site.webmanifest
├── favicon.ico  favicon.svg  apple-touch-icon.png
├── services/              hub + 8: water-service-line-repair, water-line-replacement, slab-leak-repair,
│                          underground-leak-detection, emergency-water-line-repair, repiping,
│                          sewer-line-repair, pool-leak-detection
├── locations/             hub + 8: venice, bradenton, lakewood-ranch, north-port, osprey, nokomis,
│                          siesta-key, longboat-key
├── blog/                  hub + 24 posts
├── glossary/              56 terms, DefinedTermSet schema
├── about/ contact/ disclaimer/ editorial-policy/ privacy-policy/ terms/ accessibility/
└── assets/
    ├── js/site.js         1.5 KB, deferred (menu, dropdowns, Esc, call_click dataLayer event)
    └── img/               logos (SVG horizontal/light/icon), icons 192/512/maskable, logo-512,
                           og-default.jpg, blog/<slug>.webp|.jpg|-600.webp
source/                    generator (Python): build.py, assets.py, audit.py, qa_browser.py, content/*.py
```

53 HTML pages (52 indexable). Rebuild: `python3 assets.py && python3 build.py && python3 audit.py`.

## 2. Image list

All images are generated branded graphics (no stock photos, no people).

| File | Placement | Alt text | Source |
| --- | --- | --- | --- |
| assets/img/logo-horizontal.svg / -light.svg | Brand use (light/dark backgrounds) | SRQ Leak Pros | Generated SVG |
| assets/img/logo-icon.svg, favicon.svg/.ico | Favicon, header mark (inline SVG) | — (decorative; logo link has aria-label) | Generated |
| apple-touch-icon.png, icon-192/512, icon-maskable-512 | Home-screen / manifest | — | Generated |
| assets/img/logo-512.png | Schema logo | — | Generated |
| assets/img/og-default.jpg (1200×630) | OG/Twitter image for all non-post pages | — (meta only) | Generated |
| assets/img/blog/<slug>.webp + .jpg (1200×630) | Post featured image (LCP, fetchpriority=high) + OG | "<Post H1> guide graphic" | Generated |
| assets/img/pages/<name>.webp + -600.webp (1200×675) | 19 in-content photos: 3 on the home page, 1 per service page, 1 per location page (lazy-loaded, srcset, captioned with photographer credit) | Descriptive alt per photo (content/figures.py) | Free Pexels photos (pexels.com/license), cropped to 16:9 and converted to WebP by photos.py |
| assets/img/blog/<slug>-600.webp (600×315) | Blog cards (lazy) | "<Post H1> guide graphic" | Generated |

To change a photo, edit its Pexels ID in photos.py and its alt, caption and credit in content/figures.py, then run `python3 photos.py` before `assets.py`/`build.py`.

Optional later: real job photos (WebP, ≤200 KB, with width/height) for service pages once you have them.

## 3. Self-audit report (Gate 4) — 27/27 pass

| Check | Status | Result |
| --- | --- | --- |
| Internal links and assets resolve | PASS | 0 broken links |
| No orphan pages | PASS | 0 orphans |
| Max click depth 2 from home | PASS | max depth = 2 |
| ≥3 in-text inbound links (services, locations, posts) | PASS | all ≥3 (min 3) |
| No nested links (cards, glossary links) | PASS | 0 nested anchors |
| No generic anchor text | PASS | 0 generic anchors |
| Titles ≤60, metas ≤155, one H1, canonical/OG/lang, heading order | PASS | all pages pass |
| Unique titles, metas and H1s | PASS | all unique |
| Keyword in title, meta, H1, first 100 words, an H2, slug | PASS | 41 money/blog pages pass |
| No cannibalization (unique primary keyword per page) | PASS | Home owns 'leak detection Sarasota'; locations own 'leak detection + area'; services own sub-services; posts own informational queries |
| Word counts in range (home 1.2–1.8k, services 1.0–1.8k*, locations 0.8–1.2k, posts 1.0–2.3k) | PASS | all in range |
| Location pages ≥60% unique (5-word shingles) | PASS | min 83.1% / max 92.7% |
| No duplicate paragraphs of 14+ words site-wide | PASS | 0 duplicates |
| Reading level FK grade ≤9 (target 6–8) | PASS | avg 5.6, range 4.3–8.9 |
| Schema valid JSON, @ids resolve, FAQs visible, no ratings/address/geo/hours | PASS | 53 pages, 190 @ids |
| Banned wording scan (text, alt, meta) | PASS | 0 hits |
| 'Licensed' only next to plumber/contractor/law | PASS | rule respected |
| Single phone number and tel: value site-wide | PASS | (941) 541-0938 / tel:+19415410938 only |
| Referral disclosure on every page | PASS | present on all pages |
| No street address (service-area business) | PASS | no address in pages or schema |
| Images: alt text, width/height, lazy except LCP | PASS | all images pass |
| Performance budget (HTML <100KB, images <200KB, JS ≤10KB) | PASS | max HTML 64KB, JS 1461B, inline CSS 11800B, max image 63KB |
| No render-blocking scripts or CSS | PASS | JS deferred; CSS preloaded + inline critical |
| sitemap.xml lists every indexable page with lastmod | PASS | 52 URLs |
| robots, _headers, _redirects, manifest, icons, 404 present | PASS | all present |
| 404 is noindex | PASS |  |
| Every blog links its money page in first 150 words, 3+ guides, 2–5 locations | PASS | 24/24 posts pass |

**Browser QA (headless Chrome, live CSP headers):** no horizontal scroll at 360 / 768 / 1280 px on 17 page types (including 4 new posts); 0 console or CSP errors; CLS 0; local LCP ≤ 160 ms. Mobile menu opens, sub-menus expand, Esc closes; desktop dropdowns open on hover and focus; sticky call bar shows under 960 px and hides above; header phone visible on desktop; CTA hover amber→light amber with navy text; card hover teal border; logo stays visible on hover; visible 3 px focus outlines; footer links turn mint on hover.

| Fix log | Issue found | Fix applied |
| --- | --- | --- |
| Banned wording | "24 hours", "pick up/picks up" in 8 places | Reworded ("the next day", "detect", "amplifies") |
| Licensed rule | "be licensed?", "pool contractors are also licensed", "licensed author" | Reworded so "licensed" only sits next to plumber/contractor/law |
| Keyword map | Shut-off post title/H1 phrasing mismatch | Aligned H1, quick answer and H2 to "shut off water to your house" |
| Word counts | 7 location pages and 3 posts under minimum | Added unique local/how-to sections (all now in range) |
| Competitor length | Slab (1,301) and sewer (1,230) below top competitors (~1,425 / ~1,594) | Added gap sections; now 1,463 and 1,594 |
| Duplicate paragraphs | Shared legal "laws referenced" line on 3 pages | Unique law line per page |
| Nested links | Glossary auto-links inside service cards (broke 2 cards) | Glossary linking now runs before cards are inserted; audit check added |
| Contrast | Glossary link inside dark CTA box | CTA text excluded from glossary linking |
| CSP | Inline `onload` on CSS preload would be blocked by CSP | Full CSS (11.8 KB) inlined; CSP stays `script-src 'self'` |
| CLS | Async stylesheet caused layout shift (up to 2.4) | Inlined CSS; CLS now 0 on all tested pages |
| Unsourced claims | Pool "quarter inch a day", hot-vs-cold slab claim, PB stamp code, several local details (Wares Creek, swing bridge, South Venice) | Removed or reworded to what sources support |

## 4. Placeholder list

No `[PLACEHOLDER]` text is on the site (per your instruction). These items are **parked** until real data exists:

- Real social profile URLs (icons currently link to platform homepages)
- License number(s) — none shown; pages tell readers to verify licenses on DBPR
- Reviews / ratings (no Review or AggregateRating schema)
- Email address and hours (not shown; 24/7 and "10+ years" removed for LeadSmart compliance)
- Owner name / bio and a credentialed reviewer for EEAT
- Job photos and case studies
- Form: none (LeadSmart takes calls only). If you want form leads for other buyers (e.g. Inquirly via Resend), add later and update CSP `connect-src`/`form-action`.
- Google Business Profile (create as a service-area business, no address shown)

## 5. Deploy and launch steps

1. **GitHub:** create a private repo (e.g. `anjam775/LeakDetectionSarasotaFL`), commit the `site/` contents (or the `source/` project with `dist/` as output).
2. **Cloudflare Pages:** Create project → Connect to Git (or Direct Upload the `site` folder / ZIP). Framework preset: None. Build command: none (or `python3 assets.py && python3 build.py` if building from source). Output directory: `/` for the site folder (or `dist`).
3. **Custom domain:** Pages project → Custom domains → add `leakdetectionsarasotafl.us` and `www.leakdetectionsarasotafl.us`. If DNS is at Spaceship, either move nameservers to Cloudflare or add the CNAME records Cloudflare shows. Add a redirect rule www → apex (301).
4. **Check headers:** open DevTools → Network on the live site and confirm `_headers` (CSP, HSTS, immutable `/assets/*`).
5. **Google Search Console:** add a Domain property, verify by DNS TXT, submit `https://leakdetectionsarasotafl.us/sitemap.xml`, request indexing for home, services hub and locations hub.
6. **Bing Webmaster Tools:** import from GSC, submit the sitemap.
7. **Call tracking:** confirm (941) 541-0938 routes through Ringba/LeadSmart as planned and that the recording announcement plays (the site says calls may be recorded).
8. **GBP and citations:** create a service-area GBP, name **SRQ Leak Pros**, phone **(941) 541-0938**, website the apex URL, address hidden, service areas = Sarasota, Venice, Bradenton, Lakewood Ranch, North Port, Osprey, Nokomis, Siesta Key, Longboat Key. Use the identical name/phone/URL on every citation (Bing Places, Apple Business Connect, Yelp, BBB, Nextdoor). No address on any citation.
9. **Social:** create profiles, then replace the default URLs in `content/data.py → SITE["social"]` and rebuild.
10. **Monitoring:** run Semrush Position Tracking for the keyword map; review at day 30 and day 60.

## 6. Content wave 2 (published November 5, 2026)

The 12 posts from the 90-day plan are now live, bringing the blog to 24 posts. Each follows the Blog Post Criteria doc: short-answer box, money-page link in the first 150 words, question H2s, numbered steps, checklists, comparison tables, a Florida rule section, a Sarasota section, mid and final CTAs, a prevention list, a Local note with 3–4 location links, a Related reading paragraph, 4–5 FAQs (FAQPage schema) and 3–6 opened primary sources.

| # | Post | Keyword (Semrush vol/KD) | Supports | Strongest competitor (est.) | Our words |
| --- | --- | --- | --- | --- | --- |
| 13 | /blog/how-deep-are-water-lines-buried/ | how deep are water lines buried (880/3) | Water line replacement | HomeServe ~800 | 1,545 |
| 14 | /blog/how-to-locate-underground-water-lines/ | how to locate underground water lines (480/6) | Underground leak detection | Precision Outdoor Tech ~1,400 | 1,540 |
| 15 | /blog/repipe-cost/ | repipe cost (480/9); whole house repipe (1,000/6) | Repiping | Angi ~1,100 | 1,180 |
| 16 | /blog/water-meter-leak/ | water meter leak (320/5) | Water service line repair | Checkatrade ~1,100 | 1,245 |
| 17 | /blog/water-leak-under-driveway/ | water leak under driveway (390/9) | Underground leak detection | HomeGo ~800 | 1,280 |
| 18 | /blog/does-home-warranty-cover-slab-leaks/ | does home warranty cover slab leaks (320/9) | Slab leak repair | ConsumerAffairs ~1,500 | 1,582 |
| 19 | /blog/irrigation-leak/ | irrigation leak (320/11) | Underground leak detection | Angi ~1,250 | 1,344 |
| 20 | /blog/main-water-line-repair-cost/ | water line repair cost (140/21) | Water service line repair | Angi/HomeAdvisor ~1,500 (excl. FAQ) | 1,505 |
| 21 | /blog/why-is-my-water-pressure-low/ | water pressure low (880/27) | Water service line repair | Bob Vila ~3,000 (above the 2,300 cap) | 1,753 |
| 22 | /blog/galvanized-pipe-replacement/ | galvanized pipe replacement (320/25) | Repiping | Home Living Handbook ~800 | 1,199 |
| 23 | /blog/cpvc-pipe-problems/ | cpvc pipe problems (170/8) | Repiping | Repipe Specialists ~1,150 | 1,325 |
| 24 | /blog/pool-bucket-test/ | pool bucket test (pool leak questions) | Pool leak detection | Angi ~1,100 | 1,261 |

Bob Vila's low-pressure guide runs about 3,000 words, above the site's 2,300-word ceiling, so that post covers its 10 causes and fixes in tighter form instead of matching length.

**Semantic coverage:** each post was checked against a 19–24 term topic list (equipment, materials, codes, agencies and local terms). All 12 cover at least 19 terms; jargon such as sonde, trace wire, PRV, zone valve, solvent cement and home warranty association is defined on first use.

**Internal links added:** each service page now lists its new guides first under Helpful guides; 11 older posts gained Related reading links to the new posts; every new post has at least 3 in-text inbound links. The glossary gained 7 terms (bucket test, ground-penetrating radar, home warranty, solvent cement, sonde, trace wire, zone valve), and 5 existing terms now point to the new guides.

**New sources opened:** Florida Building Code plumbing supplement § 305.6; Florida Statutes §§ 556.108 and 634.301; EPA WaterSense Sprinkler Spruce-Up; City of Sarasota Phase III restrictions update (Sept. 23, 2026); PNNL Building America service water pressure guide; City of Scottsdale pool bucket test; WKMG ClickOrlando CPVC report (2015). Company figures from Angi and ConsumerAffairs are credited by name in the text.

**Next:** refresh all 24 posts with Semrush position data at day 60, and watch the Phase III restriction end date (currently March 31, 2027) in the irrigation post.

## 7. Data-source note

Keyword volumes, KD, SERPs, competitor traffic and pages: **Semrush** (US database, Nov 2026). Competitor word counts, headings and schema: measured in the built-in browser on Spartan, Sleuth, Wimpy's, Bullseye, Aqua and HydroScout pages (American Leak Detection blocked access). Local facts: Wikipedia pages checked 2026-11-04; Sarasota County, City of Sarasota, EPA, eCFR, Sunshine 811 and Florida Statutes pages opened directly. Cost figures: Angi only, credited by name.
