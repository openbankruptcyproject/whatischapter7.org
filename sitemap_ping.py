"""Ping Google and Bing with all BTN sitemaps."""
import requests

DOMAINS = [
    "109g.org", "341meeting.org", "523a.org", "727a8.com", "727a8.org",
    "automaticstay.org", "bankruptcyhardship.org", "bankruptcymill.com",
    "bankruptcymill.org", "chapter13plan.org", "codebtorstay.org",
    "dischargebar.org", "dischargeinjunction.com", "dischargeinjunction.org",
    "dismissedbankruptcy.org", "keepmycarinbankruptcy.com",
    "keepmyhouseinbankruptcy.com", "lienstripping.org", "meanstest.org",
    "nondischargeable.org", "prosedebtors.org", "reaffirmationagreement.org",
    "rebuildcreditafterbankruptcy.com", "relieffromstay.org", "section1328.org",
    "serialfiler.org", "voluntarypetition.org", "whatischapter7.com",
    "whatischapter7.org", "1328f.com", "1328f.org",
]

google_ok = 0
google_fail = 0
bing_ok = 0
bing_fail = 0

for domain in DOMAINS:
    sitemap_url = f"https://{domain}/sitemap.xml"

    # Google ping
    try:
        g_url = f"https://www.google.com/ping?sitemap={sitemap_url}"
        r = requests.get(g_url, timeout=15)
        status = "OK" if r.status_code == 200 else f"HTTP {r.status_code}"
        if r.status_code == 200:
            google_ok += 1
        else:
            google_fail += 1
        print(f"Google  {domain:42s} {status}")
    except Exception as e:
        google_fail += 1
        print(f"Google  {domain:42s} ERROR: {e}")

    # Bing ping
    try:
        b_url = f"https://www.bing.com/ping?sitemap={sitemap_url}"
        r = requests.get(b_url, timeout=15)
        status = "OK" if r.status_code == 200 else f"HTTP {r.status_code}"
        if r.status_code == 200:
            bing_ok += 1
        else:
            bing_fail += 1
        print(f"Bing    {domain:42s} {status}")
    except Exception as e:
        bing_fail += 1
        print(f"Bing    {domain:42s} ERROR: {e}")

    print()

print("=" * 60)
print(f"Google: {google_ok} OK, {google_fail} failed out of {len(DOMAINS)}")
print(f"Bing:   {bing_ok} OK, {bing_fail} failed out of {len(DOMAINS)}")
