# SRQ Leak Pros — leakdetectionsarasotafl.us

Static lead-gen site for leak detection and water service line repair in Sarasota, FL. Referral voice (LeadSmart-compatible), service-area business, single phone (941) 541-0938.

## Layout

| Path | What it is |
| --- | --- |
| `dist/` | Built, deploy-ready site (Cloudflare Pages output directory) |
| `content/` | Page content and site data (`data.py`, `home.py`, `services_*.py`, `locations.py`, `posts_*.py`, `support.py`, `glossary.py`) |
| `static/` | CSS source, JS source, generated public assets (icons, logos, blog images, `_headers`, `_redirects`) |
| `assets.py` | Generates icons, logos, OG/blog images, minified CSS/JS, Cloudflare files |
| `build.py` | Renders every page, schema, sitemap and robots into `dist/` |
| `audit.py` | Gate 4 self-audit (links, metadata, keyword map, schema, compliance, performance) |
| `qa_browser.py` | Headless Chrome checks: responsive, console/CSP, interactive states, CLS/LCP |
| `DELIVERY.md` | Delivery report: audit results, image list, parked items, deploy steps, 90-day plan |

## Rebuild

```bash
pip install markdown pillow cairosvg
python3 assets.py && python3 build.py && python3 audit.py
```

Commit the updated `dist/` after every rebuild.

## Cloudflare Pages

- Framework preset: **None**
- Build command: *(leave empty)*
- Build output directory: **`dist`**
- Custom domain: `leakdetectionsarasotafl.us` (+ `www` redirect to apex)

## Status at launch

- 53 pages: home, 8 services, 8 locations, 24 blog posts, glossary (63 terms), hubs, about, contact, disclaimer, editorial policy, privacy, terms, accessibility, 404
- Self-audit 27/27 pass; Lighthouse 100/100/100/100 on home, a service, a location and a post
