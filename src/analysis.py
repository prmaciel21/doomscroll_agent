from collections import Counter, defaultdict
from memory import get_recent

def analyze(days: int = 7) -> dict:
    reels = get_recent(days)
    if not reels:
        return {}

    # --- category distribution (what the agent actually found) ---
    category_counts = Counter(r.get("content_category", "general") for r in reels)

    # --- performance by category ---
    cat_stats = defaultdict(lambda: {"engagement": [], "virality": [], "likes": [], "views": []})
    for r in reels:
        cat = r.get("content_category", "general")
        cat_stats[cat]["engagement"].append(r.get("engagement_rate", 0))
        cat_stats[cat]["virality"].append(r.get("virality_score", 0))
        cat_stats[cat]["likes"].append(r.get("likes", 0))
        cat_stats[cat]["views"].append(r.get("views", 0))

    category_performance = {}
    for cat, stats in cat_stats.items():
        n = len(stats["engagement"])
        category_performance[cat] = {
            "count": n,
            "avg_engagement_rate": round(sum(stats["engagement"]) / n, 2),
            "avg_virality_score": round(sum(stats["virality"]) / n, 3),
            "avg_likes": round(sum(stats["likes"]) / n),
            "avg_views": round(sum(stats["views"]) / n),
        }

    # --- auto-discovered top hashtags across all data ---
    hashtag_eng = defaultdict(list)
    for r in reels:
        for tag in r.get("hashtags", []):
            hashtag_eng[tag.lower().lstrip("#")].append(r.get("engagement_rate", 0))

    top_hashtags = sorted(
        {tag: round(sum(vals)/len(vals), 2)
         for tag, vals in hashtag_eng.items() if len(vals) >= 1}.items(),
        key=lambda x: x[1], reverse=True
    )[:15]

    # --- best posting times ---
    slot_eng = defaultdict(list)
    for r in reels:
        slot_eng[r.get("time_slot", "unknown")].append(r.get("engagement_rate", 0))

    best_times = sorted(
        {slot: round(sum(vals)/len(vals), 2)
         for slot, vals in slot_eng.items()}.items(),
        key=lambda x: x[1], reverse=True
    )

    # --- top viral reels as examples ---
    top_reels = sorted(reels, key=lambda r: r.get("virality_score", 0), reverse=True)[:5]

    return {
        "total_reels_analyzed": len(reels),
        "category_distribution": dict(category_counts.most_common()),
        "category_performance": category_performance,
        "top_hashtags": top_hashtags,
        "best_posting_times": best_times,
        "top_viral_reels": [
            {
                "shortcode": r["shortcode"],
                "caption_preview": r["caption"][:120],
                "category": r["content_category"],
                "likes": r["likes"],
                "views": r["views"],
                "engagement_rate": r["engagement_rate"],
                "virality_score": r["virality_score"],
                "time_slot": r["time_slot"],
                "hashtags": r.get("hashtags", [])[:8],
            }
            for r in top_reels
        ],
    }