import requests
from typing import List, Dict, Any

# Use HTTPS, not HTTP
PUSHSHIFT_BASE = "https://api.pushshift.io/reddit/search"

# A simple User-Agent so the API knows who you are
HEADERS = {
    "User-Agent": "crypto-sentiment-analyzer/1.0"
}

def fetch_reddit_data(
    tickers: List[str],
    subreddits: List[str],
    post_limit: int = 100
) -> List[Dict[str, Any]]:
    """
    Fetch recent Reddit submissions and comments via Pushshift (HTTPS).
    """
    results: List[Dict[str, Any]] = []

    for subreddit in subreddits:
        # 1) Submissions
        params = {
            "subreddit":  subreddit,
            "q":          " OR ".join(tickers),
            "size":       post_limit,
            "fields":     ["title", "selftext", "created_utc"],
            "sort":       "desc",
            "sort_type":  "created_utc"
        }
        resp = requests.get(f"{PUSHSHIFT_BASE}/submission/", params=params, headers=HEADERS)
        resp.raise_for_status()
        for post in resp.json().get("data", []):
            text = (post.get("title") or "") + " " + (post.get("selftext") or "")
            up = text.upper()
            for ticker in tickers:
                if ticker in up:
                    results.append({
                        "ticker":      ticker,
                        "text":        text,
                        "created_utc": post.get("created_utc", 0)
                    })

        # 2) Comments
        params["fields"] = ["body", "created_utc"]
        resp = requests.get(f"{PUSHSHIFT_BASE}/comment/", params=params, headers=HEADERS)
        resp.raise_for_status()
        for cm in resp.json().get("data", []):
            text = cm.get("body") or ""
            up = text.upper()
            for ticker in tickers:
                if ticker in up:
                    results.append({
                        "ticker":      ticker,
                        "text":        text,
                        "created_utc": cm.get("created_utc", 0)
                    })

    return results
