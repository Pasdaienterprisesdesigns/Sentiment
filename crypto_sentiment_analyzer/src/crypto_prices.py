import yfinance as yf
import pandas as pd

def get_crypto_price(ticker, period='7d', interval='1h'):
    # Download price data
    data = yf.download(ticker, period=period, interval=interval)
    
    # Turn the index into a column
    data.reset_index(inplace=True)
    
    # Rename the first column (usually "Date") to "date"
    data.rename(columns={data.columns[0]: 'date'}, inplace=True)
    
    # If for any reason yfinance returned a MultiIndex (e.g. multiple tickers),
    # flatten it to the lowest level
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(-1)
    
    # Return only the timestamp and Close price
    return data[['date', 'Close']]
