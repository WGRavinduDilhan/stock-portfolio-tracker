import yfinance as yf
import pandas as pd
import time

def get_stock_price(ticker: str) -> float: # This will return 0.0 if there is any error getting price, instead of crashing the app.

    try:
        stock = yf.Ticker(ticker) # This indicate the ticker is valid and exist, if not it will raise error and return 0.0
        hist = stock.history(period="1d") 

        if hist.empty:
            print(f"Warning: No price data found for {ticker}. Returning 0.")
            return 0.0

        price = hist['Close'].iloc[-1] # Get the latest closing price
        return float(price)       

    #stock = yf.Ticker(ticker)
    #return stock.history(period="1d")['Close'].iloc[-1]

    except Exception as e:
        print(f" X Error fetching price for {ticker}: {e}")
        return 0.0



def get_historical_data(ticker: str, period: str = "6mo") -> pd.DataFrame:  # This will return an empty DataFrame with the correct columns if there is any error getting historical data, instead of crashing the app.
    
    try:         # This checks the data fetching and if error happens will raise error without crashing the app
        stock = yf.Ticker(ticker)   
        df = stock.history(period=period) 

        if df.empty:
            print(f"⚠️ No historical data for {ticker}")
            return pd.DataFrame(columns=["Close", "Volume"])
        
        return df[["Close", "Volume"]]

    except Exception as e:
        print(f" X Error fetching historical data for {ticker}: {e}")
        return pd.DataFrame(columns=["Close", "Volume"])
    


def get_stock_info(ticker: str) -> dict: # This return a dictionary with default values if error occer it will show error message withour crashing.

    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        return {
        "name": info.get("longName", ticker),
        "sector": info.get("sector", "N/A"),
        "market_cap": info.get("marketCap", 0),
    }

    except Exception as e:
        print(f" X Error fetching info for {ticker}: {e}")
        return {
            "name": ticker,
            "sector": "N/A",
            "market_cap": 0,
        }

    
    
