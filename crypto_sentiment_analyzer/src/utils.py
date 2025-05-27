import pandas as pd

def merge_sentiment_price(
    sentiment_df: pd.DataFrame,
    price_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Align sentiment scores with historical price data using an as-of merge.

    Args:
        sentiment_df: DataFrame with columns:
            - 'ticker':      str, crypto ticker
            - 'created_utc': float, UNIX timestamp
            - 'date':        datetime64[ns], conversion of 'created_utc'
            - sentiment columns (e.g. 'polarity', 'subjectivity')
        price_df:     DataFrame with columns:
            - 'date':      datetime64[ns], timestamps of each price point
            - 'Close':     float, closing price at that timestamp

    Returns:
        merged_df: DataFrame containing all columns from sentiment_df plus
                   a 'Close' column, where each sentiment row is matched
                   to the nearest prior price.
    """

    # 1) Flatten any MultiIndex columns in price_df
    if isinstance(price_df.columns, pd.MultiIndex):
        price_df.columns = price_df.columns.get_level_values(-1)

    # 2) Ensure 'date' columns are datetime and sort both DataFrames
    sentiment_df['date'] = pd.to_datetime(sentiment_df['date'])
    price_df['date']     = pd.to_datetime(price_df['date'])

    sentiment_df = sentiment_df.sort_values('date').reset_index(drop=True)
    price_df     = price_df.sort_values('date').reset_index(drop=True)

    # 3) Perform a backward as-of merge: each sentiment uses the latest price at or before its timestamp
    merged_df = pd.merge_asof(
        left=sentiment_df,
        right=price_df[['date', 'Close']],
        on='date',
        direction='backward'
    )

    return merged_df
