import pandas as pd

def merge_sentiment_price(sentiment_df, price_df):
    sentiment_df['date'] = pd.to_datetime(sentiment_df['created_utc'], unit='s')
    sentiment_df.sort_values(by='date', inplace=True)
    price_df.sort_values(by='date', inplace=True)
    merged_df = pd.merge_asof(sentiment_df, price_df, on='date')
    return merged_df
