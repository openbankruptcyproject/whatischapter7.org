"""Submit sitemaps via Google Search Console API + Bing IndexNow."""
import google.auth
from googleapiclient.discovery import build
import requests

SCOPES = ['https://www.googleapis.com/auth/webmasters']

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

def main():
    # --- GOOGLE: Submit sitemaps via GSC API ---
    print("=" * 70)
    print("GOOGLE SEARCH CONSOLE - Sitemap Submission")
    print("=" * 70)

    credentials, project = google.auth.default(scopes=SCOPES)
    service = build('searchconsole', 'v1', credentials=credentials)

    google_ok = 0
    google_fail = 0
    google_skip = 0

    for domain in DOMAINS:
        site_url = f"sc-domain:{domain}"
        sitemap_url = f"https://{domain}/sitemap.xml"
        try:
            # Submit sitemap
            service.sitemaps().submit(siteUrl=site_url, feedpath=sitemap_url).execute()
            print(f"  SUBMITTED  {domain:42s} sitemap.xml")
            google_ok += 1
        except Exception as e:
            err = str(e)
            if "403" in err or "forbidden" in err.lower():
                # Try with https:// prefix instead
                try:
                    site_url2 = f"https://{domain}/"
                    service.sitemaps().submit(siteUrl=site_url2, feedpath=sitemap_url).execute()
                    print(f"  SUBMITTED  {domain:42s} sitemap.xml (https prefix)")
                    google_ok += 1
                    continue
                except Exception:
                    print(f"  SKIP       {domain:42s} not verified in GSC")
                    google_skip += 1
            else:
                print(f"  FAIL       {domain:42s} {err[:80]}")
                google_fail += 1

    print(f"\nGoogle: {google_ok} submitted, {google_skip} skipped (not verified), {google_fail} failed")

    # --- BING: Ping via IndexNow (no key needed for sitemap ping) ---
    print(f"\n{'=' * 70}")
    print("BING - Sitemap Ping via www.bing.com/indexnow")
    print("=" * 70)

    bing_ok = 0
    bing_fail = 0

    for domain in DOMAINS:
        sitemap_url = f"https://{domain}/sitemap.xml"
        try:
            # Bing still accepts sitemap submissions via this URL
            r = requests.get(
                "https://www.bing.com/webmaster/api.svc/json/SubmitSitemap",
                params={"siteUrl": f"https://{domain}", "feedUrl": sitemap_url},
                timeout=15
            )
            if r.status_code == 200:
                print(f"  OK         {domain:42s}")
                bing_ok += 1
            else:
                # Try IndexNow as fallback
                r2 = requests.get(
                    "https://www.bing.com/indexnow",
                    params={"url": sitemap_url, "key": domain.replace(".", "")},
                    timeout=15
                )
                if r2.status_code in (200, 202):
                    print(f"  OK         {domain:42s} (IndexNow)")
                    bing_ok += 1
                else:
                    print(f"  HTTP {r.status_code:3d}   {domain:42s}")
                    bing_fail += 1
        except Exception as e:
            print(f"  ERROR      {domain:42s} {e}")
            bing_fail += 1

    print(f"\nBing: {bing_ok} OK, {bing_fail} failed")

if __name__ == "__main__":
    main()
