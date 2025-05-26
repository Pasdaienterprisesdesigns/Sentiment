import yfinance as yf
import pandas as pd

def get_crypto_price(ticker, period='7d', interval='1h'):
    data = yf.download(ticker, period=period, interval=interval)
    data.reset_index(inplace=True)
    data.rename(columns={'Datetime': 'date'}, inplace=True)
    return data[['date', 'Close']]
