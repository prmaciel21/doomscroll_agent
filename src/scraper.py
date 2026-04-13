from apify_client import ApifyClient
from datetime import datetime, timezone
from dotenv import load_dotenv
import os

load_dotenv()  # load env vars from .env file

client = ApifyClient(os.getenv("APIFY_API_TOKEN"))  # use env var for token in production

def fetch_reels(results: int = 100) -> list[dict]:
    run_input = {
        "urls": [
            "https://www.instagram.com/explore/",
            "https://www.instagram.com/reels/",
        ],
        "resultsLimit": results,
    }

    run = client.actor("apify/instagram-scraper").call(run_input=run_input)
    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

    reels = []
    for item in items:
        if not item.get("videoUrl"):   # filter to video/reels only
            continue
        reels.append({
            "id": item.get("id"),
            "shortcode": item.get("shortCode"),
            "caption": item.get("caption", ""),
            "hashtags": item.get("hashtags", []),
            "likes": item.get("likesCount", 0),
            "views": item.get("videoViewCount", 0),
            "comments": item.get("commentsCount", 0),
            "owner_username": item.get("ownerUsername"),
            "owner_followers": item.get("ownerFollowersCount", 0),
            "posted_at": item.get("timestamp"),          # ISO string
            "posted_hour": _extract_hour(item.get("timestamp")),
            "fetched_at": datetime.now(timezone.utc).isoformat(),
        })
    return reels

def _extract_hour(ts: str | None) -> int | None:
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00")).hour
    except Exception:
        return None