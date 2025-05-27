import praw
import streamlit as st
from typing import List, Dict, Any

FALLBACK_CLIENT_ID     = "hPi7skbJRo6j7PHHNfhLFw"
FALLBACK_CLIENT_SECRET = "XwRxWu6Odi5bFW1k_4Hl-dFKps7nKQ"
FALLBACK_USER_AGENT    = "New-Cloud5866"

def reddit_connection() -> praw.Reddit:
    """
    Initialize and return a PRAW Reddit instance, sourcing credentials
    from Streamlit secrets (preferred) or fallback constants (local dev).
    """
    cfg = st.secrets.get("reddit", {})
    client_id     = cfg.get("client_id",     FALLBACK_CLIENT_ID)
    client_secret = cfg.get("client_secret", FALLBACK_CLIENT_SECRET)
    user_agent    = cfg.get("user_agent",    FALLBACK_USER_AGENT)

    return praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
    )

def fetch_reddit_data(
    tickers: List[str],
    subreddits: List[str],
    post_limit: int = 100
) -> List[Dict[str, Any]]:
    """
    Fetch Reddit posts (and their selftext) from given subreddits that mention
    any of the provided tickers.

    Args:
        tickers:     List of uppercase ticker symbols, e.g. ["BTC", "ETH"]
        subreddits:  List of subreddit names to search, e.g. ["CryptoCurrency"]
        post_limit:  Number of top posts to retrieve per subreddit

    Returns:
        A list of dicts with keys:
          - 'ticker':      str, the matched ticker symbol
          - 'text':        str, combined title + selftext
          - 'created_utc': float, UNIX timestamp of the post
    """
    reddit = reddit_connection()
    results: List[Dict[str, Any]] = []

    for subreddit_name in subreddits:
        subreddit = reddit.subreddit(subreddit_name)
        for post in subreddit.hot(limit=post_limit):
            # combine title and body, uppercase for case-insensitive matching
            combined = f"{post.title} {post.selftext or ''}"
            combined_upper = combined.upper()

            # check each ticker
            for ticker in tickers:
                if ticker.upper() in combined_upper:
                    results.append({
                        "ticker":      ticker.upper(),
                        "text":        combined,
                        "created_utc": post.created_utc
                    })
    return results
