import pandas as pd

def merge_sentiment_price(sentiment_df: pd.DataFrame, price_df: pd.DataFrame) -> pd.DataFrame:
    # 1) Flatten price_df columns again just in case
    if isinstance(price_df.columns, pd.MultiIndex):
        price_df.columns = price_df.columns.get_level_values(-1)

    # 2) Convert timestamps into datetime
    sentiment_df["date"] = pd.to_datetime(sentiment_df["created_utc"], unit="s")
    price_df["date"]     = pd.to_datetime(price_df["date"])

    # 3) Sort both DataFrames by date
    sentiment_df = sentiment_df.sort_values("date")
    price_df     = price_df.sort_values("date")

    # 4) As-of merge: each sentiment picks up the latest prior price
    merged = pd.merge_asof(
        sentiment_df,
        price_df,
        on="date",
        direction="backward"
    )
    return merged
