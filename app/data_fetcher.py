import yfinance as yf
import pandas as pd


# ── Current price ─────────────────────────────────────────────────────────────
def get_stock_price(ticker: str) -> float:
    """Fetch latest closing price. Returns 0.0 on any error."""
    try:
        stock = yf.Ticker(ticker)
        hist  = stock.history(period="1d")
        if hist.empty:
            print(f"Warning: No price data for {ticker}.")
            return 0.0
        return float(hist["Close"].iloc[-1])
    except Exception as e:
        print(f"Error fetching price for {ticker}: {e}")
        return 0.0


# ── Historical OHLCV ──────────────────────────────────────────────────────────
def get_historical_data(ticker: str, period: str = "6mo") -> pd.DataFrame:
    """Fetch historical Close + Volume. Returns empty DataFrame on error."""
    try:
        stock = yf.Ticker(ticker)
        df    = stock.history(period=period)
        if df.empty:
            print(f"No historical data for {ticker}")
            return pd.DataFrame(columns=["Close", "Volume"])
        return df[["Close", "Volume"]]
    except Exception as e:
        print(f"Error fetching historical data for {ticker}: {e}")
        return pd.DataFrame(columns=["Close", "Volume"])


# ── Company info ──────────────────────────────────────────────────────────────
def get_stock_info(ticker: str) -> dict:
    """Fetch company name, sector, market cap."""
    try:
        info = yf.Ticker(ticker).info
        return {
            "name":       info.get("longName", ticker),
            "sector":     info.get("sector", "N/A"),
            "market_cap": info.get("marketCap", 0),
        }
    except Exception as e:
        print(f"Error fetching info for {ticker}: {e}")
        return {"name": ticker, "sector": "N/A", "market_cap": 0}


# ── News feed ─────────────────────────────────────────────────────────────────
def get_stock_news(ticker: str, limit: int = 5) -> list[dict]:
    """
    Fetch the latest news articles for a ticker via yfinance.

    Returns a list of dicts with keys:
        title     – headline text
        link      – article URL
        publisher – source name
    """
    try:
        raw_news = yf.Ticker(ticker).news or []
        articles = []
        for item in raw_news[:limit]:
            # yfinance v0.2+ nests content inside a 'content' key
            content = item.get("content", item)
            title   = content.get("title", "No title")
            # Link can be in different fields depending on yfinance version
            link    = (
                content.get("canonicalUrl", {}).get("url")
                or content.get("clickThroughUrl", {}).get("url")
                or item.get("link", "#")
            )
            publisher = (
                content.get("provider", {}).get("displayName")
                or content.get("publisher", "Unknown")
            )
            articles.append({"title": title, "link": link, "publisher": publisher})
        return articles
    except Exception as e:
        print(f"Error fetching news for {ticker}: {e}")
        return []
