import streamlit as st
from app.portfolio import Portfolio
from app.data_fetcher import get_stock_price, get_historical_data
from app.metrics import calculate_returns, calculate_portfolio_value
from app.visualizer import plot_price_history, plot_portfolio_pie, plot_returns_bar
from time import time

# Set up Streamlit page configuration
st.set_page_config(page_title="Stock Portfolio Tracker", layout="wide") # This will set the page title and make the layout wide for better visualization.
st.title("📈 Stock Portfolio Tracker & Analytics Dashboard")


# Initialize portfolio in session state
if "portfolio" not in st.session_state:        # This checks the portfolio is already in session state, if not it will create a new one. 
    st.session_state.portfolio = Portfolio()   # 


# Sidebar - Add stock and other data inputs
st.sidebar.header(" Add a Stock ")             
ticker = st.sidebar.text_input("Ticker Symbol (ex: AAPL, TSLA)").upper()         # This get the ticker symbol input from the user and convert it to uppercase.
shares = st.sidebar.number_input("Number of Shares", min_value=1)                # This get the number of shares input from the user and set the minimum value to 1.
buy_price = st.sidebar.number_input("Buy Price per Share ($)", min_value=0.01)   # This get the buy price per share input from the user and set the minimum value to 0.01.


if st.sidebar.button("Add to Portfolio"):                                # This shows the button with name "Add to Portfolio" and when clicks it will add the stock and show a success message.
    st.session_state.portfolio.add_stock(ticker, shares, buy_price)      # This will add the stock to the portfolio using the add_stock method of the Portfolio class.
    st.success(f"Added {ticker} to portfolio!")                          # This shows a success message with the ticker symbol of the stock that was added to the portfolio.


# Main dashboard
holdings = st.session_state.portfolio.get_holdings()                     # This take the current holdings from the portfolio using the get_holdings method of the Portfolio class.      
if holdings:
    with st.spinner("Fetching data and calculating metrics..."):         # This shows a spinner with the message "Fetching data and calculating metrics..." while the data are calculating.
        current_prices = {}                                              # This will store the current prices of the stocks in the portfolio. It will be used to calculate the total portfolio value and returns.
        
        for ticker in holdings:                                          # This loop will iterate through the tickers in the holdings and fetch the current price for each ticker using get_stock_price function. Also handle errors that occur during price fetching.
            price = get_stock_price(ticker)                              
            current_prices[ticker] = price                              
            if price == 0.0:
                st.warning(f"⚠️ No price data for {ticker}. It will be shown as $0 in calculations.")
            #time.sleep(0.5)  # Sleep to avoid hitting API rate limits  #  This is no need now when it have, error handle for price fetching. It will just return 0 and continue without delay.   

    #current_prices = {t: get_stock_price(t) for t in holdings}  
    total_value = calculate_portfolio_value(holdings, current_prices)
    st.metric("Total Portfolio Value", f"${total_value:,.2f}")


# Price history to Bar chart for the first stock in the portfolio
    tickers = list(holdings.keys())  # Get list of tickers from holdings
    returns = [calculate_returns(holdings[t]["buy_price"], current_prices[t]) for t in tickers] # Calculate returns for each stock
    st.plotly_chart(plot_returns_bar(tickers, returns), use_container_width=True) # Show returns bar chart


#Pie chart for portfolio allocation
    st.plotly_chart(plot_portfolio_pie(holdings, current_prices), use_container_width=True)


# Price history for the first stock in the portfolio
    selected = st.selectbox("Select a stock to view price history", tickers)
    hist = get_historical_data(selected)
    st.plotly_chart(plot_price_history(hist, selected), use_container_width=True)



