import pandas as pd

def merge_sentiment_price(
    sentiment_df: pd.DataFrame,
    price_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Align sentiment scores with historical price data using an as-of merge.

    Args:
        sentiment_df: DataFrame with at least:
            - 'date' datetime64[ns] (timestamp of each sentiment point)
            - other sentiment columns (e.g. 'polarity')
        price_df: DataFrame with:
            - 'date' datetime64[ns] (timestamp of each price point)
            - 'Close' float (closing price)

    Returns:
        merged_df: sentiment_df plus a 'Close' column, where each sentiment row
                   is matched to the latest prior price.
    """

    # 1) Flatten MultiIndex columns in price_df (if any)
    if isinstance(price_df.columns, pd.MultiIndex):
        price_df.columns = price_df.columns.get_level_values(-1)

    # 2) Ensure both DataFrames have a datetime 'date' and sort by it
    sentiment_df['date'] = pd.to_datetime(sentiment_df['date'])
    price_df   ['date'] = pd.to_datetime(price_df['date'])

    sentiment_df = sentiment_df.sort_values('date').reset_index(drop=True)
    price_df     = price_df.sort_values('date').reset_index(drop=True)

    # 3) As-of merge: for each sentiment timestamp, bring in the last prior Close
    merged_df = pd.merge_asof(
        left=sentiment_df,
        right=price_df[['date', 'Close']],
        on='date',
        direction='backward'
    )

    return merged_df
