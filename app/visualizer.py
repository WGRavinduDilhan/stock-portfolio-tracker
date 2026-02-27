import plotly.graph_objects as go
import plotly.express as px

def plot_price_history(df, ticker): # Function to plot price history of a stock using Plotly Express
    fig = px.line(df, x=df.index, y="Close", title=f"{ticker} Price History", template="plotly_dark")
    # Customize the layout

    return fig # Return the figure object to be displayed in the Streamlit app


def plot_portfolio_pie(holdings, current_prices):
    labels, values = [], []
    for ticker, data in holdings.items():
        labels.append(ticker)
        values.append(data["shares"] * current_prices.get(ticker, 0))  # Calculate the total value of each stock holding
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3)])
    fig.update_layout(title="Portfolio Allocation", template="plotly_dark")

    return fig # Return the figure object to be displayed in the Streamlit app as a pie chart


def plot_returns_bar(tickers, returns):
    colors = ["green" if r > 0 else "red" for r in returns]
    fig = go.Figure([go.Bar(x=tickers, y=returns, marker_color=colors)])
    fig.update_layout(title="Return % per Stock", template="plotly_dark")

    return fig # Return the figure object to be displayed in the Streamlit app as barchart 
