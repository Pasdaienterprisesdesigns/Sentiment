import requests
from typing import List, Dict, Any

PUSHSHIFT_BASE = "https://api.pushshift.io/reddit/search"

def fetch_reddit_data(
    tickers: List[str],
    subreddits: List[str],
    post_limit: int = 100
) -> List[Dict[str, Any]]:
    """
    Fetch recent Reddit submissions mentioning specified tickers
    via the Pushshift API (no authentication required).

    Args:
        tickers:     List of uppercase ticker symbols, e.g. ["BTC","ETH"]
        subreddits:  List of subreddit names to search in, e.g. ["CryptoCurrency"]
        post_limit:  Maximum number of posts per subreddit to retrieve.

    Returns:
        A list of dicts, each with:
          - 'ticker':      str, matched ticker symbol
          - 'text':        str, title + selftext
          - 'created_utc': int, UNIX timestamp of the post
    """
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
        resp = requests.get(f"{PUSHSHIFT_BASE}/submission/", params=params)
        resp.raise_for_status()
        submissions = resp.json().get("data", [])

        for post in submissions:
            text = (post.get("title", "") or "") + " " + (post.get("selftext") or "")
            up = text.upper()
            for ticker in tickers:
                if ticker in up:
                    results.append({
                        "ticker":      ticker,
                        "text":        text,
                        "created_utc": post.get("created_utc", 0)
                    })

        # 2) (Optional) Fetch comments too
        params["fields"] = ["body", "created_utc"]
        resp = requests.get(f"{PUSHSHIFT_BASE}/comment/", params=params)
        resp.raise_for_status()
        comments = resp.json().get("data", [])
        for cm in comments:
            text = cm.get("body", "") or ""
            up = text.upper()
            for ticker in tickers:
                if ticker in up:
                    results.append({
                        "ticker":      ticker,
                        "text":        text,
                        "created_utc": cm.get("created_utc", 0)
                    })

    return results
