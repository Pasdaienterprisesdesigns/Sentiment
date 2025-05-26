import pandas as pd

def merge_sentiment_price(sentiment_df, price_df):
    # — Flatten any MultiIndex columns (e.g. from yfinance) to a single level
    if isinstance(price_df.columns, pd.MultiIndex):
        price_df.columns = price_df.columns.get_level_values(-1)
    
    # — Convert Reddit timestamps and sort both DataFrames
    sentiment_df['date'] = pd.to_datetime(sentiment_df['created_utc'], unit='s')
    sentiment_df.sort_values(by='date', inplace=True)
    price_df.sort_values(by='date', inplace=True)
    
    # — Perform the asof merge
    merged_df = pd.merge_asof(sentiment_df, price_df, on='date')
    return merged_df
