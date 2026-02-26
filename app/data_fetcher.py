import yfinance as yf
import pandas as pd

def get_stock_price(ticker: str) -> float:
    stock = yf.Ticker(ticker)
    return stock.history(period="1d")['Close'].iloc[-1]

def get_historical_data(ticker: str, period: str = "6mo") -> pd.DataFrame:
    stock = yf.Ticker(ticker)
    df = stock.history(period=period)
    return df[["Close", "Volume"]]

def get_stock_info(ticker: str) -> dict:
    stock = yf.Ticker(ticker)
    info = stock.info
    return {
        "name": info.get("longName", ticker),
        "sector": info.get("sector", "N/A"),
        "market_cap": info.get("marketCap", 0),
    }

