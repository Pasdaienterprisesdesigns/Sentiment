# src/reddit_scraper.py

import praw
import streamlit as st

# ——— CONFIGURATION ———
# Local dev fallbacks (dummy values; replace with your own for testing):
REDDIT_CLIENT_ID     = "hPi7skbJRo6j7PHHNfhLFw"
REDDIT_CLIENT_SECRET = "XwRxWu6Odi5bFW1k_4Hl-dFKps7nKQ"
REDDIT_USER_AGENT    = "crypto_sentiment_analyzer_by_dairus"

# In Streamlit Cloud, you’ll override these via st.secrets:
# [reddit]
# client_id     = "YOUR_CLIENT_ID"
# client_secret = "YOUR_CLIENT_SECRET"
# user_agent    = "script:crypto.sentiment:v1.0 (by /u/your_reddit_username)"

def reddit_connection():
    cfg = st.secrets.get("reddit", {})
    client_id     = cfg.get("client_id",     REDDIT_CLIENT_ID)
    client_secret = cfg.get("client_secret", REDDIT_CLIENT_SECRET)
    user_agent    = cfg.get("user_agent",    REDDIT_USER_AGENT)

    return praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
    )

def fetch_reddit_data(tickers, subreddits, post_limit=100):
    reddit = reddit_connection()
    data = []
    for subreddit_name in subreddits:
        for post in reddit.subreddit(subreddit_name).hot(limit=post_limit):
            text = f"{post.title} {post.selftext or ''}"
            text_upper = text.upper()
            for ticker in tickers:
                if ticker in text_upper:
                    data.append({
                        'ticker':      ticker,
                        'text':        text,
                        'created_utc': post.created_utc
                    })
    return data
