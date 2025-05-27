import streamlit as st
import pandas as pd

from src.reddit_scraper import fetch_reddit_data
from src.sentiment_analysis import analyze_sentiments
from src.crypto_prices import get_crypto_price
from src.utils import merge_sentiment_price

st.set_page_config(
    page_title="🚀 Crypto Sentiment Analyzer",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🚀 Reddit Crypto Market Sentiment Analyzer")
st.markdown(
    """
    This app fetches Reddit posts mentioning your chosen cryptocurrency tickers,
    analyzes their sentiment, and aligns that with historic price data to show
    how social mood correlates with price movements.
    """
)

# --- Sidebar configuration ---
st.sidebar.header("🔧 Configuration")

# Mapping human-friendly names to yfinance tickers
CRYPTO_MAPPING = {
    "Bitcoin (BTC)":   "BTC-USD",
    "Ethereum (ETH)":  "ETH-USD",
    "Solana (SOL)":    "SOL-USD",
    "Ripple (XRP)":    "XRP-USD",
    "Tether (USDT)":   "USDT-USD",
    "USD Coin (USDC)": "USDC-USD",
    "Dai (DAI)":       "DAI-USD",
}

crypto_choice = st.sidebar.selectbox(
    "Select Cryptocurrency:",
    list(CRYPTO_MAPPING.keys()),
    index=0
)

num_posts = st.sidebar.slider(
    "Number of Reddit posts to fetch:",
    min_value=50,
    max_value=500,
    value=150,
    step=50
)

subreddits = st.sidebar.multiselect(
    "Subreddits to search:",
    options=["CryptoCurrency", "Bitcoin", "Ethereum", "CryptoMarkets", "Solana"],
    default=["CryptoCurrency", "CryptoMarkets"]
)

period = st.sidebar.selectbox(
    "Price history period:",
    options=["1d", "7d", "1mo", "3mo", "6mo"],
    index=1
)

interval = st.sidebar.selectbox(
    "Price data interval:",
    options=["5m", "15m", "1h", "1d"],
    index=2
)

run_button = st.sidebar.button("🔍 Run Analysis")

st.sidebar.markdown("---")
st.sidebar.markdown(
    "Built by Dairus Okoh • Using PRAW, TextBlob, yfinance & Streamlit"
)

# --- Main app logic ---
if run_button:
    st.info("Fetching Reddit data… this can take 10–20 seconds depending on your settings.")
    try:
        # 1) Fetch Reddit posts/comments
        reddit_data = fetch_reddit_data(
            tickers=[CRYPTO_MAPPING[crypto_choice].split("-")[0]],  # e.g. "BTC"
            subreddits=subreddits,
            post_limit=num_posts
        )

        if not reddit_data:
            st.warning("No Reddit mentions found for that ticker in the selected subreddits.")
            st.stop()

        # 2) Analyze sentiment
        sentiment_df = analyze_sentiments(reddit_data)

        # 3) Fetch price history
        price_df = get_crypto_price(
            ticker=CRYPTO_MAPPING[crypto_choice],
            period=period,
            interval=interval
        )

        # 4) Merge sentiment + price
        merged_df = merge_sentiment_price(sentiment_df, price_df)

    except Exception as e:
        st.error(f"An unexpected error occurred:\n\n```{e}```")
        st.stop()

    # --- Display Results ---
    st.success("Analysis complete!")

    # 1) Overview metrics
    avg_sentiment = merged_df["sentiment"].mean()
    newest_price  = merged_df["Close"].iloc[-1]
    col1, col2 = st.columns(2)
    col1.metric("Average Sentiment", f"{avg_sentiment:.3f}")
    col2.metric(f"{crypto_choice} Latest Close", f"${newest_price:,.2f}")

    # 2) Time-series chart
    st.subheader("📈 Sentiment vs. Price Over Time")
    chart_data = merged_df.set_index("date")[["sentiment", "Close"]]
    st.line_chart(chart_data)

    # 3) Recent raw sentiment entries
    st.subheader("🗒️ Recent Sentiment Samples")
    st.dataframe(
        sentiment_df
        .assign(date=lambda df: pd.to_datetime(df["created_utc"], unit="s"))
        .loc[:, ["date", "ticker", "sentiment"]]
        .sort_values("date", ascending=False)
        .reset_index(drop=True)
        .head(10),
        width=800,
        height=300
    )

    # 4) Download CSV
    csv = merged_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download merged data as CSV",
        data=csv,
        file_name=f"{crypto_choice.replace(' ', '_')}_sentiment_price.csv",
        mime="text/csv"
    )

else:
    st.write(
        "👉 Use the controls in the sidebar and click **Run Analysis** to start."
    )
