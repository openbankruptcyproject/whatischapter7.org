"""Request indexing via Google Search Console API urlInspection."""
import google.auth
from googleapiclient.discovery import build
import json

SCOPES = ['https://www.googleapis.com/auth/webmasters']

# URLs to inspect, grouped by property
URLS = {
    "sc-domain:1328f.com": [
        "https://1328f.com/109g-filing-bar.html",
        "https://1328f.com/explainer.html",
        "https://1328f.com/727a8-discharge-bar.html",
        "https://1328f.com/caselaw.html",
        "https://1328f.com/",
        "https://1328f.com/section-362-automatic-stay.html",
        "https://1328f.com/chapter-11.html",
        "https://1328f.com/can-you-file-bankruptcy-twice.html",
        "https://1328f.com/check.html",
        "https://1328f.com/dashboard.html",
        "https://1328f.com/chapter-13-failure-rate.html",
    ],
    "sc-domain:1328f.org": [
        "https://1328f.org/",
        "https://1328f.org/about/",
        "https://1328f.org/research/",
        "https://1328f.org/reports/",
    ],
}

def main():
    credentials, project = google.auth.default(scopes=SCOPES)
    service = build('searchconsole', 'v1', credentials=credentials)

    for site_url, urls in URLS.items():
        print(f"\n{'='*60}")
        print(f"Property: {site_url}")
        print(f"{'='*60}")
        for url in urls:
            try:
                body = {
                    "inspectionUrl": url,
                    "siteUrl": site_url,
                }
                result = service.urlInspection().index().inspect(body=body).execute()

                verdict = result.get('inspectionResult', {}).get('indexStatusResult', {}).get('verdict', 'UNKNOWN')
                coverage = result.get('inspectionResult', {}).get('indexStatusResult', {}).get('coverageState', 'UNKNOWN')
                crawled = result.get('inspectionResult', {}).get('indexStatusResult', {}).get('lastCrawlTime', 'never')
                indexing = result.get('inspectionResult', {}).get('indexStatusResult', {}).get('indexingState', 'UNKNOWN')

                print(f"\n  URL: {url}")
                print(f"  Verdict: {verdict}")
                print(f"  Coverage: {coverage}")
                print(f"  Indexing state: {indexing}")
                print(f"  Last crawled: {crawled}")

            except Exception as e:
                print(f"\n  URL: {url}")
                print(f"  ERROR: {e}")

if __name__ == "__main__":
    main()
