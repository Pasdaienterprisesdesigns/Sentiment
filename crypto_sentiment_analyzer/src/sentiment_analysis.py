from textblob import TextBlob
import pandas as pd

def analyze_sentiments(reddit_data):
    sentiments = []
    for entry in reddit_data:
        blob = TextBlob(entry['text'])
        sentiment_score = blob.sentiment.polarity
        sentiments.append({
            'ticker': entry['ticker'],
            'sentiment': sentiment_score,
            'created_utc': entry['created_utc']
        })
    return pd.DataFrame(sentiments)
