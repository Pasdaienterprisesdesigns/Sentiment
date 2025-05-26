import streamlit as st
from src.reddit_scraper import fetch_reddit_data
from src.sentiment_analysis import analyze_sentiments
from src.crypto_prices import get_crypto_price
from src.utils import merge_sentiment_price

st.title("🚀 Reddit Crypto Market Sentiment Analyzer")

tickers_dict = {
    'BTC': 'BTC-USD', 'ETH': 'ETH-USD', 'SOL': 'SOL-USD', 
    'XRP': 'XRP-USD', 'USDT': 'USDT-USD', 'USDC': 'USDC-USD', 'DAI': 'DAI-USD'
}

crypto_choice = st.sidebar.selectbox("Select Cryptocurrency", list(tickers_dict.keys()))
num_posts = st.sidebar.slider("Number of Reddit posts", 50, 500, 100)

if st.button("Run Analysis"):
    with st.spinner('Analyzing data...'):
        reddit_data = fetch_reddit_data(
            tickers=[crypto_choice],
            subreddits=['CryptoCurrency', 'Bitcoin', 'Ethereum', 'CryptoMarkets'],
            post_limit=num_posts
        )

        sentiment_df = analyze_sentiments(reddit_data)
        price_df = get_crypto_price(tickers_dict[crypto_choice])
        final_df = merge_sentiment_price(sentiment_df, price_df)

        st.success("Analysis complete!")

        st.subheader("📈 Sentiment and Price Trend")
        st.line_chart(final_df.set_index('date')[['sentiment', 'Close']])

        st.subheader("📊 Recent Sentiment Data")
        st.dataframe(sentiment_df.tail(10))
