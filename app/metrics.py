import numpy as np

def calculate_returns(buy_price, current_price):  # Calculate percentage return based on buy price and current price
    return ((current_price - buy_price) / buy_price) * 100

def calculate_portfolio_value(holdings, current_prices):   # Calculate total portfolio value based on current prices and holdings
    total_value = 0
    for ticker, data in holdings.items():
        total_value = total_value + data["shares"] * current_prices.get(ticker, 0)
    return total_value

def calculate_sharpe_ratio(daily_returns, risk_free_rate= 0.05):  # Calculate Sharpe Ratio based on daily returns and risk-free rate
    excess = daily_returns - (risk_free_rate / 252)              # imagining 252 is trading days in a year
    return (np.sqrt(252) * excess.mean() / excess.std())

def calculate_max_drawdown(price_series): # Calculate maximum drawdown based on portfolio values
    rolling_max = price_series.cummax()  # Calculate the rolling maximum of the portfolio values
    drawdown = (price_series - rolling_max) / rolling_max  # Calculate the drawdown as a percentage
    return drawdown.min() * 100  # Return the maximum drawdown (the minimum value of the drawdown series) as a percentage
