from collections import Counter, defaultdict
from memory import get_recent

def analyze(days: int = 7) -> dict:
    reels = get_recent(days)
    if not reels:
        return {}

    # --- Top hashtags by average engagement ---
    hashtag_eng = defaultdict(list)
    for r in reels:
        for tag in r.get("hashtags", []):
            hashtag_eng[tag.lower().lstrip("#")].append(r.get("engagement_rate", 0))

    top_hashtags = sorted(
        {tag: sum(vals)/len(vals) for tag, vals in hashtag_eng.items() if len(vals) >= 3}.items(),
        key=lambda x: x[1], reverse=True
    )[:10]

    # --- Best posting times by avg engagement ---
    slot_eng = defaultdict(list)
    for r in reels:
        slot_eng[r.get("time_slot", "unknown")].append(r.get("engagement_rate", 0))

    best_times = sorted(
        {slot: sum(vals)/len(vals) for slot, vals in slot_eng.items()}.items(),
        key=lambda x: x[1], reverse=True
    )

    # --- Top performing categories ---
    cat_eng = defaultdict(list)
    cat_viral = defaultdict(list)
    for r in reels:
        cat = r.get("content_category", "general")
        cat_eng[cat].append(r.get("engagement_rate", 0))
        cat_viral[cat].append(r.get("virality_score", 0))

    category_performance = {
        cat: {
            "avg_engagement": round(sum(cat_eng[cat])/len(cat_eng[cat]), 2),
            "avg_virality": round(sum(cat_viral[cat])/len(cat_viral[cat]), 3),
            "sample_size": len(cat_eng[cat]),
        }
        for cat in cat_eng
    }

    # --- Top 5 viral reels to use as reference ---
    top_reels = sorted(reels, key=lambda r: r.get("virality_score", 0), reverse=True)[:5]

    return {
        "total_reels_analyzed": len(reels),
        "top_hashtags": top_hashtags,
        "best_posting_times": best_times,
        "category_performance": category_performance,
        "top_viral_reels": [
            {
                "shortcode": r["shortcode"],
                "caption_preview": r["caption"][:100],
                "likes": r["likes"],
                "views": r["views"],
                "engagement_rate": r["engagement_rate"],
                "virality_score": r["virality_score"],
                "time_slot": r["time_slot"],
                "category": r["content_category"],
            }
            for r in top_reels
        ],
    }