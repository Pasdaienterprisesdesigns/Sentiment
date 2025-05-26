import yfinance as yf
import pandas as pd

def get_crypto_price(ticker: str, period: str = '7d', interval: str = '1h') -> pd.DataFrame:
    # 1) Download data with no progress bar
    df = yf.download(ticker, period=period, interval=interval, progress=False)

    # 2) Reset index so the timestamp becomes a column
    df = df.reset_index()

    # 3) If columns are a MultiIndex, flatten them to strings like "Close_BTC-USD"
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [
            "_".join(filter(None, tup)).strip() 
            for tup in df.columns.values
        ]

    # 4) Rename the first column (usually "Date") to "date"
    df.rename(columns={df.columns[0]: "date"}, inplace=True)

    # 5) Find whichever column contains "Close" (case-insensitive)
    close_cols = [col for col in df.columns if "close" in col.lower()]
    if not close_cols:
        raise ValueError(f"No 'Close' column found for {ticker}. Available columns: {df.columns.tolist()}")
    df.rename(columns={close_cols[0]: "Close"}, inplace=True)

    # 6) Return only the date and the closing price
    return df[["date", "Close"]]
