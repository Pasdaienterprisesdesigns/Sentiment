from textblob import TextBlob
import pandas as pd
from typing import List, Dict, Any

def analyze_sentiments(
    reddit_data: List[Dict[str, Any]]
) -> pd.DataFrame:
    """
    Analyze sentiment of Reddit posts/comments using TextBlob.

    Args:
        reddit_data: List of dicts, each with keys:
          - 'ticker':      str, the matched ticker symbol
          - 'text':        str, combined title + selftext
          - 'created_utc': float, UNIX timestamp

    Returns:
        pandas.DataFrame with columns:
          - ticker:       str, the crypto ticker
          - created_utc:  float, original UNIX timestamp
          - date:         datetime64[ns], converted timestamp
          - polarity:     float, sentiment polarity (-1 to +1)
          - subjectivity: float, text subjectivity (0 to 1)
    """
    records = []
    for entry in reddit_data:
        text = entry.get("text", "")
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity

        records.append({
            "ticker":      entry.get("ticker", ""),
            "created_utc": entry.get("created_utc", 0.0),
            "date":        pd.to_datetime(entry.get("created_utc", 0.0), unit="s"),
            "polarity":    polarity,
            "subjectivity": subjectivity
        })

    # Build DataFrame
    df = pd.DataFrame.from_records(records)

    # Sort by date for downstream merging/plotting
    df.sort_values(by="date", inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df
