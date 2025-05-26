import praw
import os
from dotenv import load_dotenv

load_dotenv()

def reddit_connection():
    return praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT")
    )

def fetch_reddit_data(tickers, subreddits, post_limit=100):
    reddit = reddit_connection()
    data = []
    for subreddit_name in subreddits:
        subreddit = reddit.subreddit(subreddit_name)
        for post in subreddit.hot(limit=post_limit):
            for ticker in tickers:
                if ticker in post.title.upper() or ticker in post.selftext.upper():
                    data.append({
                        'ticker': ticker,
                        'text': post.title + ' ' + post.selftext,
                        'created_utc': post.created_utc
                    })
    return data
