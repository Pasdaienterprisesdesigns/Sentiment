import yfinance as yf
import pandas as pd

def get_crypto_price(
    ticker: str,
    period: str = '7d',
    interval: str = '1h'
) -> pd.DataFrame:
    """
    Fetch historical price data for a given crypto ticker.

    Args:
        ticker:       The yfinance ticker string (e.g. "BTC-USD").
        period:       How far back to fetch data (e.g. '1d', '7d', '1mo').
        interval:     Data granularity (e.g. '5m', '1h', '1d').

    Returns:
        DataFrame with two columns:
          - date:  pandas.Timestamp of each data point
          - Close: closing price at that timestamp
    """

    # 1) Download the OHLCV data
    df = yf.download(
        tickers=ticker,
        period=period,
        interval=interval,
        progress=False,      # suppress progress bar
        auto_adjust=False    # keep raw prices
    )

    # 2) Reset index so the datetime index becomes a column
    df = df.reset_index()  # now first column is usually "Date" or "Datetime"

    # 3) Flatten MultiIndex columns, if any (e.g., for multiple tickers)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [
            "_".join(filter(None, tup)).strip() for tup in df.columns.values
        ]

    # 4) Rename the timestamp column to 'date'
    #    - data.columns[0] is typically 'Date' or 'Datetime'
    df.rename(columns={df.columns[0]: 'date'}, inplace=True)

    # 5) Identify the Close column (case-insensitive)
    close_cols = [col for col in df.columns if col.lower() == 'close' or 'close_' in col.lower()]
    if not close_cols:
        raise KeyError(f"No 'Close' column found for {ticker}. Columns available: {df.columns.tolist()}")
    df.rename(columns={close_cols[0]: 'Close'}, inplace=True)

    # 6) Return only the relevant columns
    return df[['date', 'Close']]
