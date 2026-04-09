import json
from pathlib import Path
from datetime import datetime

STORE = Path("data/reels_store.json")

def load() -> dict:
    if STORE.exists():
        return json.loads(STORE.read_text())
    return {"seen_ids": [], "reels": []}

def save(store: dict):
    STORE.parent.mkdir(exist_ok=True)
    STORE.write_text(json.dumps(store, indent=2))

def upsert(reels: list[dict]) -> int:
    store = load()
    seen = set(store["seen_ids"])
    new = [r for r in reels if r["id"] not in seen]
    store["reels"].extend(new)
    store["seen_ids"].extend(r["id"] for r in new)
    save(store)
    return len(new)

def get_recent(days: int = 7) -> list[dict]:
    store = load()
    cutoff = datetime.utcnow().timestamp() - (days * 86400)
    results = []
    for r in store["reels"]:
        try:
            ts = datetime.fromisoformat(r["fetched_at"]).timestamp()
            if ts >= cutoff:
                results.append(r)
        except Exception:
            continue
    return results