import pandas as pd

def merge_sentiment_price(sentiment_df, price_df):
    # Convert UNIX timestamps to datetime
    sentiment_df['date'] = pd.to_datetime(sentiment_df['created_utc'], unit='s')
    
    # Sort both DataFrames by date
    sentiment_df.sort_values(by='date', inplace=True)
    price_df.sort_values(by='date', inplace=True)
    
    # Merge “as-of” so each sentiment point picks up the nearest prior price
    merged_df = pd.merge_asof(
        sentiment_df,
        price_df,
        on='date',
        direction='backward'
    )
    return merged_df
