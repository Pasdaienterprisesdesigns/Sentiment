import requests
from typing import List, Dict, Any

# — Use HTTPS, not HTTP, and include a simple User-Agent —
PUSHSHIFT_BASE = "https://api.pushshift.io/reddit/search"
HEADERS = {
    "User-Agent": "crypto-sentiment-analyzer/1.0"
}

def fetch_reddit_data(
    tickers: List[str],
    subreddits: List[str],
    post_limit: int = 100
) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []

    for subreddit in subreddits:
        # 1) Fetch submissions
        params = {
            "subreddit": subreddit,
            "q": " OR ".join(tickers),
            "size": post_limit,
            "fields": ["title", "selftext", "created_utc"],
            "sort": "desc",
            "sort_type": "created_utc"
        }
        resp = requests.get(f"{PUSHSHIFT_BASE}/submission/", params=params, headers=HEADERS)
        resp.raise_for_status()
        for post in resp.json().get("data", []):
            text = (post.get("title") or "") + " " + (post.get("selftext") or "")
            up = text.upper()
            for t in tickers:
                if t in up:
                    results.append({
                        "ticker": t,
                        "text": text,
                        "created_utc": post.get("created_utc", 0)
                    })

        # 2) Fetch comments
        params["fields"] = ["body", "created_utc"]
        resp = requests.get(f"{PUSHSHIFT_BASE}/comment/", params=params, headers=HEADERS)
        resp.raise_for_status()
        for cm in resp.json().get("data", []):
            text = cm.get("body") or ""
            up = text.upper()
            for t in tickers:
                if t in up:
                    results.append({
                        "ticker": t,
                        "text": text,
                        "created_utc": cm.get("created_utc", 0)
                    })

    return results
