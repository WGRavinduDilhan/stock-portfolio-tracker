from app.data_fetcher import get_historical_data, get_stock_price
from app.visualizer import plot_price_history, plot_portfolio_pie, plot_returns_bar
import time

# Test 1: Price history chart
print("Test 1: Creating price history chart...")
df = get_historical_data("AAPL", "3mo")
fig = plot_price_history(df, "AAPL")
print(f"-/ Figure created: {type(fig)}")
fig.show()  # Opens in browser for preview
time.sleep(2)


# Test 2: Portfolio pie chart
print("\nTest 2: Creating portfolio pie chart...")
holdings = {
    "AAPL": {"shares": 10, "buy_price": 150},
    "TSLA": {"shares": 5, "buy_price": 200},
    "GOOGL": {"shares": 3, "buy_price": 140}
}
current_prices = {
    "AAPL": get_stock_price("AAPL"),
    "TSLA": get_stock_price("TSLA"),
    "GOOGL": get_stock_price("GOOGL")
}
fig = plot_portfolio_pie(holdings, current_prices)
print(f"-/ Figure created: {type(fig)}")
fig.show()
time.sleep(2)


# Test 3: Returns bar chart
print("\nTest 3: Creating returns bar chart...")
tickers = ["AAPL", "TSLA", "GOOGL"]
returns = [16.7, -12.5, 5.3]
fig = plot_returns_bar(tickers, returns)
print(f"-/ Figure created: {type(fig)}")
fig.show()

print("\n *** All visualizations created successfully! *** ")