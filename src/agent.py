from scraper import fetch_reels
from enrichment import enrich
from memory import upsert
from insights import generate_report
from pathlib import Path
from datetime import datetime

TARGET_HASHTAGS = ["reels", "viral", "trending", "explore"]
CLIENT_NICHE = "fitness"  # change per client

def run():
    print(f"[{datetime.utcnow().isoformat()}] Starting scrape cycle...")

    raw = fetch_reels(TARGET_HASHTAGS, results_per_hashtag=40)
    enriched = enrich(raw)
    new_count = upsert(enriched)
    print(f"  Stored {new_count} new reels (skipped {len(raw)-new_count} duplicates)")

    print("  Generating insight report...")
    report = generate_report(niche=CLIENT_NICHE)

    out_path = Path(f"reports/report_{datetime.utcnow().strftime('%Y%m%d_%H%M')}.md")
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text(report)

    print(f"  Report saved to {out_path}")
    print("\n" + "="*60)
    print(report)
    print("="*60)

if __name__ == "__main__":
    run()