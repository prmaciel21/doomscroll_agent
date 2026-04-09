from apify_client import ApifyClient
from datetime import datetime

client = ApifyClient("YOUR_APIFY_API_TOKEN")

def fetch_reels(hashtags: list[str], results_per_hashtag: int = 30) -> list[dict]:
    run_input = {
        "hashtags": hashtags,
        "resultsLimit": results_per_hashtag,
        "scrapeType": "posts",         # reels show up as posts with video=True
    }

    run = client.actor("apify/instagram-hashtag-scraper").call(run_input=run_input)
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
            "fetched_at": datetime.utcnow().isoformat(),
            "hashtag_source": item.get("hashtag"),
        })
    return reels

def _extract_hour(ts: str | None) -> int | None:
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00")).hour
    except Exception:
        return None