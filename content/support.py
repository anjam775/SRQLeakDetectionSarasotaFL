import html as _h
from data import POSTS, BLOG_CATS, SITE
from glossary import TERMS

NAME = SITE["name"]
DATE = SITE["today_human"]

def _blog_sections():
    out = []
    for c in BLOG_CATS:
        slugs = [p["slug"] for p in POSTS if p["cat"] == c]
        out.append(f"## {c}\n\n{{{{POSTS:{','.join(slugs)}}}}}\n")
    return "\n".join(out)

def _glossary_html():
    letters = sorted({t["term"][0].upper() for t in TERMS})
    az = '<ul class="gl-az" aria-label="Jump to letter">' + "".join(f'<li><a href="#letter-{l.lower()}">{l}</a></li>' for l in letters) + "</ul>"
    parts = [az]
    for l in letters:
        terms = sorted([t for t in TERMS if t["term"][0].upper() == l], key=lambda t: t["term"].lower())
        parts.append(f'<h2 id="letter-{l.lower()}">{l}</h2><dl class="gl-list">')
        for t in terms:
            name = t["term"][0].upper() + t["term"][1:]
            parts.append(f'<dt id="{t["slug"]}">{_h.escape(name)}</dt><dd>{_h.escape(t["def"])} <a href="{t["target"]}">Learn more about {_h.escape(t["term"])}</a>.</dd>')
        parts.append("</dl>")
    return "".join(parts)

_LAW = {
 "934": "[§ 934.03, Florida Statutes](https://www.flsenate.gov/Laws/Statutes/2025/934.03), on recording calls with all-party consent",
 "171": "[§ 501.171, Florida Statutes](https://www.flsenate.gov/Laws/Statutes/2025/501.171), the Florida Information Protection Act",
 "059": "[§ 501.059, Florida Statutes](https://www.flsenate.gov/laws/statutes/2024/501.059), on telephone solicitation",
 "fdbr": "the Florida Digital Bill of Rights, [§ 501.701 and following](https://www.flsenate.gov/Session/Bill/2023/262/Amendment/181372/PDF)",
}
def legal_src(intro, keys):
    items = [_LAW[k] for k in keys]
    joined = items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]
    return "\n\n" + intro + " " + joined + "."


PAGES = [
# ------------------------------------------------------------------ services hub
{"type": "hub", "slug": "services", "url": "/services/",
"title": "Leak Detection & Water Line Services | Sarasota, FL",
"meta": "Leak detection and water line services in Sarasota, FL: service lines, slabs, sewers, pools, repipes and emergencies. Call (941) 541-0938.",
"h1": "Leak Detection and Water Line Services in Sarasota",
"crumb": "Services", "trail": [("Home", "/"), ("Services", "/services/")],
"lead": "Eight services, one phone number. SRQ Leak Pros connects Sarasota-area homeowners with independent local leak detection and water line companies.",
"about": ["leak_detection", "sarasota"], "mentions": ["plumbing", "sanitary_sewer"],
"body": """
Pick the service that matches what you're seeing. Each page explains the signs, how the work is done, what changes the price and what to ask before you hire. If you're not sure which one fits, start with [leak detection in Sarasota](/) or call **{PH}** and describe the problem.

## Leak detection and water line repair services

{{SERVICES}}

## How to choose the right service

| What you notice | Start here |
| --- | --- |
| Meter moves, yard looks dry | [Underground leak detection](/services/underground-leak-detection/) |
| Soggy strip from the meter to the house | [Water service line repair](/services/water-service-line-repair/) |
| Old line that keeps breaking | [Water line replacement](/services/water-line-replacement/) |
| Warm floor or damp baseboard | [Slab leak repair](/services/slab-leak-repair/) |
| Burst pipe or gushing yard line | [Emergency water line repair](/services/emergency-water-line-repair/) |
| Polybutylene or pinholed copper | [Repiping](/services/repiping/) |
| Slow drains or sewage smell | [Sewer line repair](/services/sewer-line-repair/) |
| Pool level keeps dropping | [Pool leak detection](/services/pool-leak-detection/) |

## Comparing leak detection companies in Sarasota

SRQ Leak Pros is a referral service, not a plumbing company. When your call connects, ask the provider for a Florida license number, proof of insurance and a written estimate. Florida law places water and sewer line work within the plumbing contractor's scope. You can check a license on the state DBPR license search.
""",
},
# ------------------------------------------------------------------ locations hub
{"type": "hub", "slug": "locations", "url": "/locations/",
"title": "Leak Detection Service Areas Near Sarasota, FL",
"meta": "Leak detection and water line repair service areas near Sarasota, FL: Venice, Bradenton, Lakewood Ranch, North Port, Osprey, Nokomis and the keys.",
"h1": "Leak Detection Service Areas Near Sarasota",
"crumb": "Locations", "trail": [("Home", "/"), ("Locations", "/locations/")],
"lead": "SRQ Leak Pros connects homeowners in Sarasota and nearby communities in Sarasota and Manatee counties with independent local leak detection pros.",
"about": ["leak_detection", "sarasota_county"], "mentions": ["manatee_county", "sarasota"],
"body": """
Leaks don't behave the same everywhere. Barrier-island homes face salt air and empty months. Older river-city neighborhoods have aging pipe. Newer planned communities have long plastic lines and big irrigation systems. Each area page explains what to watch for where you live. The City of Sarasota itself is covered on the [Sarasota leak detection](/) home page.

## Leak detection and water line repair by area

{{LOCATIONS}}

## How service areas work

Calls are connected with independent, participating providers that serve your part of the region. Coverage near the edges of the area can vary by provider. If you're unsure whether your street is covered, call **{PH}** and ask.
""",
},
# ------------------------------------------------------------------ blog hub
{"type": "hub", "slug": "blog", "url": "/blog/", "blog": True,
"title": "Leak Detection & Water Line Guides | SRQ Leak Pros Blog",
"meta": "Plain-English guides on service line leaks, slab leaks, high water bills, insurance, costs and pipes for Sarasota-area homeowners.",
"h1": "Leak Detection and Water Line Guides",
"crumb": "Blog", "trail": [("Home", "/"), ("Blog", "/blog/")],
"lead": "Clear, sourced answers to the leak and water line questions Sarasota homeowners ask most.",
"about": ["leak_detection"], "mentions": ["water_supply", "sarasota"],
"body": """
Each guide answers one question in plain English, cites its sources and points to the right next step. Ready to get a leak found? Start with [leak detection in Sarasota](/). Need a term explained? See the [leak and water line glossary](/glossary/).

""" + _blog_sections(),
},
# ------------------------------------------------------------------ glossary
{"type": "glossary", "slug": "glossary", "url": "/glossary/",
"title": "Leak Detection & Water Line Glossary | SRQ Leak Pros",
"meta": "Plain-English glossary of leak detection, water service line, slab leak, sewer and pool plumbing terms, from acoustic leak detection to water table.",
"h1": "Leak Detection and Water Line Glossary",
"crumb": "Glossary", "trail": [("Home", "/"), ("Glossary", "/glossary/")],
"lead": "Plain-English definitions of the words you'll hear from a leak detection pro, with links to the guide that explains each one.",
"about": ["leak_detection"], "mentions": ["plumbing", "water_supply"],
"body": """
Jump to a letter, or scroll the list. Each term links to the page that covers it in more depth. For help finding a leak, start with [leak detection in Sarasota](/) or browse the [blog](/blog/).
""",
"html": _glossary_html(),
},
# ------------------------------------------------------------------ about
{"type": "about", "slug": "about", "url": "/about/",
"title": "About SRQ Leak Pros | Sarasota Leak Detection Referrals",
"meta": "SRQ Leak Pros is a referral service connecting Sarasota-area homeowners with independent local leak detection and water line providers.",
"h1": "About SRQ Leak Pros",
"crumb": "About", "trail": [("Home", "/"), ("About", "/about/")],
"lead": "SRQ Leak Pros helps Sarasota-area homeowners reach independent local pros for leaks, water service lines, sewers and pools, with one phone call.",
"about": ["leak_detection", "sarasota"], "mentions": ["sarasota_county"],
"body": """
## What SRQ Leak Pros does

SRQ Leak Pros is a referral service. When you call **{PH}**, your call can be connected with an independent, participating local provider who handles leak detection and water line work in your area. The provider quotes the job, does the work and bills you directly.

SRQ Leak Pros does not perform plumbing, leak detection, sewer, pool or repair work, and does not employ the providers. "SRQ" is the local shorthand for Sarasota.

## Why this site exists

Hidden leaks are confusing. Owners often don't know whether a wet yard is the utility's problem or theirs, which kind of pro to call, or what questions to ask. This site explains those things in plain English, with sources, and makes it easy to reach a local provider when you're ready.

## How the content is made

Every guide is written by SRQ Leak Pros Editorial and checked against primary sources such as Sarasota County, the City of Sarasota, the U.S. EPA and Florida Statutes. Search data for planning comes from Semrush. Nothing on the site claims credentials, reviews, awards or prices that haven't been verified. Read the [editorial policy](/editorial-policy/) for details.

## How to choose a provider

When your call connects, ask:

:::checks
- What is your Florida license number?
- Are you insured for this work?
- How will you find the leak, and what will that cost?
- What repair options do I have?
- Will you give me a written estimate before you start?
- Will you pull the permit and call 811 if digging is needed?
:::

## Where calls are connected

Calls from Sarasota and nearby communities in Sarasota and Manatee counties can be connected. See all [service areas](/locations/) and [services](/services/).

## Disclosure

Calls may be connected to independent providers and may be recorded for quality and training. SRQ Leak Pros may be compensated when calls are connected. Read the full [disclaimer](/disclaimer/).
""",
},
# ------------------------------------------------------------------ contact
{"type": "contact", "slug": "contact", "url": "/contact/",
"title": "Contact SRQ Leak Pros | Call (941) 541-0938",
"meta": "Contact SRQ Leak Pros by phone at (941) 541-0938 to reach an independent local leak detection or water line provider in the Sarasota area.",
"h1": "Contact SRQ Leak Pros",
"crumb": "Contact", "trail": [("Home", "/"), ("Contact", "/contact/")],
"lead": "The fastest way to reach a local leak pro is by phone. Call and describe what you're seeing.",
"about": ["leak_detection"], "mentions": ["sarasota"],
"body": """
## Call to reach a local provider

<p><a class="big-call" href="tel:+19415410938" data-call="contact">(941) 541-0938</a></p>

Your call can be connected with an independent, participating provider that serves your area. Calls may be recorded for quality and training.

## What to have ready

:::checks
- Your street address or ZIP code
- What you've noticed: meter moving, wet yard, warm floor, high bill, pool dropping
- Whether you've closed the main shut-off valve
- Your water utility, if you know it
- Any photos of the leak or damage
:::

## Before you call: a quick check

Turn off all water and look at your meter. If the small flow indicator is moving, water is leaking somewhere. Then close the house main and look again. This tells the provider whether the leak is likely in the yard or the house. The full steps are in [how to find a water leak underground](/blog/how-to-find-water-leak-underground/).

## Water leaking in the street?

If water is coming up in the street, from a hydrant or inside the meter box, report it to your water utility first. Those leaks are usually the utility's to fix. Read [who is responsible for the water line](/blog/who-is-responsible-for-water-line-from-street-to-house/).

## Service area

SRQ Leak Pros is a service-area business with no walk-in office. Calls from Sarasota and nearby communities in Sarasota and Manatee counties can be connected. See the [service areas](/locations/).
""",
},
# ------------------------------------------------------------------ disclaimer
{"type": "legal", "slug": "disclaimer", "url": "/disclaimer/",
"title": "Disclaimer and Referral Disclosure | SRQ Leak Pros",
"meta": "SRQ Leak Pros is a referral service. Read how calls are connected with independent providers, call recording, compensation and limits of the content.",
"h1": "Disclaimer and Referral Disclosure",
"crumb": "Disclaimer", "trail": [("Home", "/"), ("Disclaimer", "/disclaimer/")],
"lead": "Document: Referral disclosure and content disclaimer for leakdetectionsarasotafl.us, effective " + DATE + ".",
"about": [], "mentions": [],
"body": """
## Referral service

SRQ Leak Pros is a referral service. It does not perform leak detection, plumbing, water line, sewer, pool or any repair work. It does not employ, supervise or control the providers it connects you with.

## How calls work

When you call the number on this site, your call may be connected with an independent, participating local service provider. Calls may be routed through a call-tracking system and **may be recorded for quality and training**. By calling, you consent to this. Florida law, § 934.03, generally requires the consent of all parties to record a call.

## Compensation

SRQ Leak Pros may be compensated when calls are connected. This does not change the price you pay the provider, which you agree with the provider directly.

## Providers are independent

Providers are responsible for their own licenses, insurance, permits, pricing, scheduling, workmanship and warranties. SRQ Leak Pros does not guarantee any provider's work, availability, timing or price. Before hiring, ask for a license number and check it on the Florida DBPR license search, ask about insurance, and get a written estimate.

## Information only

The content on this site is general information. It is not legal, insurance, engineering or professional advice. Laws, utility rules and prices change. Check your own policy, your utility's rules and current law, and talk with a qualified professional about your situation.

## Third-party sources

Pages cite outside sources such as government sites and named cost guides. SRQ Leak Pros does not control those sites and is not responsible for their content.

## Contact

Questions about this disclosure can be raised by calling {PH}.
""" + legal_src("The recording rule above comes from", ["934"]),
},
# ------------------------------------------------------------------ editorial policy
{"type": "legal", "slug": "editorial-policy", "url": "/editorial-policy/",
"title": "Editorial Policy | SRQ Leak Pros",
"meta": "How SRQ Leak Pros researches, writes, fact-checks and updates its leak detection and water line guides, and what it never publishes.",
"h1": "Editorial Policy",
"crumb": "Editorial Policy", "trail": [("Home", "/"), ("Editorial Policy", "/editorial-policy/")],
"lead": "Document: Editorial standards for SRQ Leak Pros content, effective " + DATE + ".",
"about": [], "mentions": [],
"body": """
## Who writes the content

Pages and guides are written by SRQ Leak Pros Editorial. Bylines read "SRQ Leak Pros Editorial." No page claims an author with a license or a credentialed reviewer unless one has actually reviewed it, and that person will be named.

## How content is researched

- **Topics** come from validated search demand (Semrush, U.S. database) and from questions homeowners actually ask.
- **Facts** come from primary sources wherever possible: Sarasota County and City of Sarasota pages, Florida Statutes, the U.S. EPA and eCFR, and Sunshine 811.
- **Single figures** from a company, such as a national cost average, are credited to that company by name in the text.
- **Sources are opened and read** before they're cited. A search snippet is not a source.

## How content is fact-checked

Each page is checked against its listed sources before publishing. Laws and figures are checked to be current on the publish date. Pages show a "Last reviewed" or "Updated" date.

## What is never published

:::checks
- Invented prices, statistics or cost ranges
- Fake reviews, testimonials or ratings
- Claims about licenses, awards or company history that haven't been verified
- Promises about response times or availability
- Medical, legal or insurance advice presented as advice
:::

## Referral disclosure

SRQ Leak Pros is a referral service and may be compensated when calls are connected. This doesn't affect the content of guides. See the [disclaimer](/disclaimer/).

## Review cycle

Guides are reviewed at least once a year, and sooner when a law, utility rule or cited figure changes.

## Reporting an error

If you spot an error, call {PH} and describe it. Confirmed errors are corrected and the page's updated date is changed.
""",
},
# ------------------------------------------------------------------ privacy
{"type": "legal", "slug": "privacy-policy", "url": "/privacy-policy/",
"title": "Privacy Policy | SRQ Leak Pros",
"meta": "Privacy policy for SRQ Leak Pros: what data the site and phone calls collect, call recording, cookies, security, Florida law and your choices.",
"h1": "Privacy Policy",
"crumb": "Privacy Policy", "trail": [("Home", "/"), ("Privacy Policy", "/privacy-policy/")],
"lead": "Document: Privacy policy for leakdetectionsarasotafl.us, operated by SRQ Leak Pros, effective " + DATE + ".",
"about": [], "mentions": [],
"body": """
## Who this policy covers

This policy explains how SRQ Leak Pros ("SRQ Leak Pros") handles information when you visit leakdetectionsarasotafl.us or call the phone number on the site.

## Information collected

**When you browse.** The site's host, Cloudflare, may log standard technical data such as IP address, browser type, pages visited and time of visit, for security and performance. The site uses no forms and no account sign-up.

**When you call.** Calls may be routed through a call-tracking system that records the calling number, call time, duration, the page you called from and, where enabled, an audio recording of the call. Calls may be connected to an independent service provider, who will receive the details you share on the call.

**Click events.** The site records an anonymous "call click" event in the page when a phone link is tapped. No analytics script is installed at launch. If analytics are added later, this policy will be updated first.

## Call recording

Calls may be recorded for quality and training. Florida law, § 934.03, generally requires all parties to consent to recording. By staying on the call after being told it may be recorded, you consent to recording.

## How information is used

- To connect your call with a local provider
- To measure call quality and site performance
- To keep the site secure
- To meet legal obligations

## Sharing

Information you give on a call may be shared with the independent provider your call is connected with, so they can help you. Call records may be shared with call-routing partners and service providers who operate the phone system. SRQ Leak Pros does not sell personal information.

## Telephone and text messages

SRQ Leak Pros does not make telephone solicitations or send marketing texts to people who visit the site. Florida's telephone solicitation law, § 501.059, requires prior express written consent for certain automated sales calls and texts.

## Cookies

The site does not set advertising or tracking cookies at launch. Cloudflare may set strictly necessary security cookies.

## Data security and breach notice

Reasonable measures are used to protect information. If a breach of personal information occurs, notice will be given as required by Florida's Information Protection Act, § 501.171, which generally requires notice to affected individuals no later than 30 days after the breach is determined.

## Florida Digital Bill of Rights

The Florida Digital Bill of Rights mainly applies to businesses with more than $1 billion in global gross annual revenue that meet further tests. SRQ Leak Pros does not meet that threshold, but it does not sell sensitive personal data.

## Children

The site is not directed to children under 13 and does not knowingly collect their information.

## Your choices

You may ask what call information is held about you, or ask for it to be deleted, by calling {PH}. Some records may need to be kept for legal or security reasons.

## Changes

This policy may be updated. The effective date at the top will change when it is.
""" + legal_src("Laws named in this policy:", ["934", "171", "059", "fdbr"]),
},
# ------------------------------------------------------------------ terms
{"type": "legal", "slug": "terms", "url": "/terms/",
"title": "Terms of Use | SRQ Leak Pros",
"meta": "Terms of use for leakdetectionsarasotafl.us: referral service terms, independent providers, no warranties, limits of liability and Florida law.",
"h1": "Terms of Use",
"crumb": "Terms", "trail": [("Home", "/"), ("Terms", "/terms/")],
"lead": "Document: Terms of use for leakdetectionsarasotafl.us, operated by SRQ Leak Pros, effective " + DATE + ".",
"about": [], "mentions": [],
"body": """
## Acceptance

By using this website or calling the number on it, you agree to these terms. If you don't agree, please don't use the site.

## The service

SRQ Leak Pros is a free-to-use referral service that may connect your call with an independent, participating local service provider. SRQ Leak Pros does not perform any leak detection, plumbing, sewer, pool or repair work.

## Independent providers

Providers are independent businesses. They are solely responsible for their licenses, insurance, permits, estimates, pricing, scheduling, work and warranties. Any agreement for work is between you and the provider. SRQ Leak Pros is not a party to it.

## No guarantee

SRQ Leak Pros does not guarantee that a provider will be available, that a call will be connected, or that any provider's work will meet your expectations. Check any provider's license on the Florida DBPR license search before hiring.

## Content is general information

Site content is for general information only and is not legal, insurance, engineering or professional advice. Don't rely on it in place of advice from a qualified professional.

## Calls and recording

Calls may be recorded for quality and training. Florida law, § 934.03, generally requires all-party consent to record; by staying on the call, you consent.

## Acceptable use

Don't misuse the site, attempt to disrupt it, copy it in bulk, or use the phone number to place fraudulent, abusive or automated calls.

## Intellectual property

The site's text, design, logo and graphics belong to SRQ Leak Pros unless otherwise noted. Cited third-party sources belong to their owners.

## Disclaimer of warranties

The site is provided "as is," without warranties of any kind, to the extent allowed by law.

## Limitation of liability

To the extent allowed by law, SRQ Leak Pros is not liable for any indirect, incidental or consequential damages, or for any damages arising from a provider's work or failure to perform.

## Governing law

These terms are governed by the laws of the State of Florida.

## Changes

These terms may be updated. The effective date at the top will change when they are.

## Contact

Questions about these terms can be raised by calling {PH}.
""" + legal_src("For the call-recording terms, see", ["934"]) + " These terms are read under Florida law.",
},
# ------------------------------------------------------------------ accessibility
{"type": "legal", "slug": "accessibility", "url": "/accessibility/",
"title": "Accessibility Statement | SRQ Leak Pros",
"meta": "Accessibility statement for SRQ Leak Pros: WCAG 2.1 AA target, features of the site, known limits and how to report a barrier by phone.",
"h1": "Accessibility Statement",
"crumb": "Accessibility", "trail": [("Home", "/"), ("Accessibility", "/accessibility/")],
"lead": "Document: Accessibility statement for leakdetectionsarasotafl.us, effective " + DATE + ".",
"about": [], "mentions": [],
"body": """
## Commitment

SRQ Leak Pros wants everyone to be able to use this site. The site aims to meet the Web Content Accessibility Guidelines (WCAG) 2.1, Level AA.

## Features

:::checks
- A "Skip to content" link at the top of each page
- One main heading per page and a logical heading order
- Text and button colors chosen for strong contrast
- Visible focus outlines for keyboard users
- Menus that work with a keyboard and the Escape key
- Descriptive link text and alt text on images
- Pages that resize and reflow on phones and tablets
- Respect for reduced-motion settings
- No auto-playing audio or video
:::

## Known limits

Some linked outside sources, such as government documents, may not meet the same standard. SRQ Leak Pros doesn't control those sites.

## Report a barrier

If you have trouble using any part of this site, call {PH} and describe the page and the problem. Reports are reviewed and fixed where possible.
""",
},
# ------------------------------------------------------------------ 404
{"type": "404", "slug": "404", "url": "/404.html",
"title": "Page Not Found | SRQ Leak Pros",
"meta": "The page you were looking for was not found. Find leak detection help, services, areas and guides from SRQ Leak Pros.",
"h1": "Page Not Found",
"crumb": "Not found",
"lead": "That page doesn't exist or has moved. Here are the most helpful places to go next.",
"about": [], "mentions": [],
"body": """
- [Leak detection in Sarasota](/)
- [All leak and water line services](/services/)
- [Service areas](/locations/)
- [Leak and water line guides](/blog/)
- [Glossary](/glossary/)
- [Contact](/contact/)

Need help now? Call **{PH}** to reach a local leak pro.
""",
},
]
