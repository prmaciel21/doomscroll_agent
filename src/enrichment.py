import math

def enrich(reels: list[dict]) -> list[dict]:
    for r in reels:
        followers = r.get("owner_followers") or 1
        likes = r.get("likes", 0)
        views = r.get("views", 0)
        comments = r.get("comments", 0)

        # Engagement rate: interactions relative to reach
        r["engagement_rate"] = round((likes + comments) / max(views, 1) * 100, 2)

        # Virality score: views relative to account size
        # A small account getting huge views = more viral signal
        r["virality_score"] = round(math.log1p(views) / math.log1p(followers + 1), 3)

        # Classify posting time as a slot
        hour = r.get("posted_hour")
        r["time_slot"] = _time_slot(hour)

        # Dominant hashtag category (first recognized niche tag)
        r["content_category"] = _categorize(r.get("hashtags", []))

    return reels

def _time_slot(hour: int | None) -> str:
    if hour is None:
        return "unknown"
    if 6 <= hour < 12:
        return "morning"
    if 12 <= hour < 17:
        return "afternoon"
    if 17 <= hour < 21:
        return "evening"
    return "late_night"

CATEGORY_MAP = {
    "fitness": ["fitness","gym","workout","fitspo","health"],
    "food": ["food","recipe","cooking","foodie","eats"],
    "fashion": ["fashion","ootd","style","outfit","clothing"],
    "travel": ["travel","wanderlust","explore","trip","adventure"],
    "beauty": ["beauty","makeup","skincare","glam","hair"],
    "business": ["business","entrepreneur","marketing","money","success"],
    "comedy": ["funny","comedy","humor","meme","lol"],
}

def _categorize(hashtags: list[str]) -> str:
    tags_lower = [h.lower().lstrip("#") for h in hashtags]
    for category, keywords in CATEGORY_MAP.items():
        if any(kw in tags_lower for kw in keywords):
            return category
    return "general"