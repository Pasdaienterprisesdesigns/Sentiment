import yfinance as yf
import pandas as pd

def get_crypto_price(ticker: str, period: str = '7d', interval: str = '1h') -> pd.DataFrame:
    # 1) Download. Turn off auto_adjust so columns stay predictable.
    data = yf.download(ticker, period=period, interval=interval, auto_adjust=False)

    # 2) Reset index → 'Date' becomes a column.
    data = data.reset_index()

    # 3) If columns are a MultiIndex (e.g. [("Close","BTC-USD")]), flatten them.
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = [
            col[1] if col[1] else col[0]
            for col in data.columns.values
        ]

    # 4) Rename the first column (timestamp) to 'date'
    data.rename(columns={data.columns[0]: 'date'}, inplace=True)

    # 5) Ensure we have a 'Close' column. If not, pick whichever column contains "Close"
    if 'Close' not in data.columns:
        for col in data.columns:
            if 'Close' in col:
                data.rename(columns={col: 'Close'}, inplace=True)
                break

    # 6) Return only the timestamp and the closing price
    return data[['date', 'Close']]
