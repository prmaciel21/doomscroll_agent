import math
from collections import Counter

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
        r["content_category"] = _auto_categorize(
            r.get("hashtags", []),
            r.get("caption", "")
            )

    return reels

CATEGORY_SIGNALS = {
    "fitness":      ["fitness","gym","workout","fitspo","health","training","bodybuilding","running","yoga","crossfit"],
    "food":         ["food","recipe","cooking","foodie","eats","chef","baking","vegan","restaurant","dinner"],
    "fashion":      ["fashion","ootd","style","outfit","clothing","streetwear","luxury","designer","trend","drip"],
    "travel":       ["travel","wanderlust","explore","trip","adventure","vacation","roadtrip","hiking","beach","nature"],
    "beauty":       ["beauty","makeup","skincare","glam","hair","nails","selfcare","glow","tutorial","cosmetics"],
    "business":     ["business","entrepreneur","marketing","money","success","startup","investing","finance","hustle","passive"],
    "comedy":       ["funny","comedy","humor","meme","lol","viral","prank","skit","relatable","wtf"],
    "music":        ["music","song","dance","singer","producer","hiphop","pop","edm","cover","newmusic"],
    "tech":         ["tech","ai","coding","programming","software","gadgets","apple","android","cybersecurity","developer"],
    "lifestyle":    ["lifestyle","motivation","mindset","daily","vlog","aesthetic","minimal","productivity","routine","selfimprovement"],
    "pets":         ["dog","cat","pets","puppy","kitten","animals","doglover","catlover","petlife","wildlife"],
    "sports":       ["sports","nba","nfl","soccer","football","basketball","baseball","tennis","golf","esports"],
}

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

def _auto_categorize(hashtags: list[str], caption: str) -> str:
    text_pool = set(
        [h.lower().lstrip("#") for h in hashtags] +
        [w.lower().strip(".,!?") for w in caption.split()]
    )

    scores = Counter()
    for category, keywords in CATEGORY_SIGNALS.items():
        scores[category] = sum(1 for kw in keywords if kw in text_pool)

    best = scores.most_common(1)
    if best and best[0][1] > 0:
        return best[0][0]
    return "general"