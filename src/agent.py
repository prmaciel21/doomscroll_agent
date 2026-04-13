from scraper import fetch_reels
from enrichment import enrich
from memory import upsert
from insights import generate_report
from pathlib import Path
from datetime import datetime, timezone

def run():
    print(f"[{datetime.now(timezone.utc).isoformat()}] Starting scrape cycle...")

    raw = fetch_reels(results=150)
    enriched = enrich(raw)
    new_count = upsert(enriched)
    print(f"  Stored {new_count} new reels (skipped {len(raw)-new_count} duplicates)")

    print("  Generating insight report...")
    report = generate_report(days=30)

    out_path = Path(f"reports/report_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M')}.md")
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text(report)

    print(f"  Report saved to {out_path}")
    print("\n" + "="*60)
    print(report)
    print("="*60)

if __name__ == "__main__":
    run()