"""
app.py — Stock Portfolio Tracker & Analytics Dashboard
Enhanced version with 14 new features.
"""

import time
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from app.portfolio    import Portfolio
from app.data_fetcher import get_stock_price, get_historical_data, get_stock_news
from app.metrics      import calculate_returns, calculate_portfolio_value, \
                             calculate_sharpe_ratio, calculate_max_drawdown
from app.visualizer   import (plot_price_history, plot_portfolio_pie,
                               plot_returns_bar,   plot_volume_bar)
from app.alerts       import check_alerts, format_alert_message
from app.ai_insights  import get_stock_insight

load_dotenv()

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Stock Portfolio Tracker",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Auto-refresh every 5 minutes — native Streamlit (Enhancement #10) ────────
# Uses session state timestamp; no external package needed.
_REFRESH_INTERVAL = 5 * 60  # seconds
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = time.time()
if time.time() - st.session_state.last_refresh > _REFRESH_INTERVAL:
    st.session_state.last_refresh = time.time()
    st.rerun()

# ── Custom CSS (Light Theme) ──────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Light main background */
    .stApp { background-color: #f8fafc; }
    /* Metric cards — white with subtle border and shadow */
    div[data-testid="metric-container"] {
        background    : #ffffff;
        border        : 1px solid #e2e8f0;
        border-radius : 10px;
        padding       : 12px 16px;
        box-shadow    : 0 1px 4px rgba(0,0,0,0.06);
    }
    /* Section headers */
    .section-header {
        font-size     : 1.05rem;
        font-weight   : 600;
        color         : #2563eb;
        margin        : 1.2rem 0 0.4rem 0;
        border-bottom : 2px solid #dbeafe;
        padding-bottom: 4px;
    }
    /* News items */
    .news-item { margin-bottom: 6px; }
    a { color: #2563eb; }
</style>
""", unsafe_allow_html=True)

st.title("📈 Stock Portfolio Tracker & Analytics Dashboard")
st.caption("Prices auto-refresh every 5 minutes · Powered by Yahoo Finance")

# ── Session state init ────────────────────────────────────────────────────────
if "portfolio" not in st.session_state:
    st.session_state.portfolio = Portfolio()
    st.session_state.portfolio.load_from_db()   # Load from SQLite on first load

if "alerts" not in st.session_state:
    st.session_state.alerts = {}   # { ticker: {"below": float|None, "above": float|None} }

portfolio: Portfolio = st.session_state.portfolio

# ═══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.header("➕ Add a Stock")
    ticker    = st.text_input("Ticker Symbol (e.g. AAPL, TSLA)").upper().strip()
    shares    = st.number_input("Number of Shares",        min_value=0.01, step=0.01)
    buy_price = st.number_input("Buy Price per Share ($)", min_value=0.01, step=0.01)

    if st.button("Add to Portfolio", use_container_width=True):
        if ticker:
            portfolio.add_stock(ticker, shares, buy_price)
            st.success(f"✅ Added {ticker} to portfolio!")
        else:
            st.warning("Please enter a ticker symbol.")

    # ── Enhancement #1: Remove stock ─────────────────────────────────────────
    holdings = portfolio.get_holdings()
    if holdings:
        st.divider()
        st.subheader("➖ Remove a Stock")
        ticker_to_remove = st.selectbox(
            "Select stock to remove", ["— select —"] + list(holdings.keys()),
            key="remove_select",
        )
        if st.button("Remove", use_container_width=True, type="secondary"):
            if ticker_to_remove != "— select —":
                portfolio.remove_stock(ticker_to_remove)
                st.rerun()

    # ── Enhancement #14: Price Alerts ────────────────────────────────────────
    if holdings:
        st.divider()
        with st.expander("🔔 Price Alerts"):
            alert_ticker = st.selectbox(
                "Stock", list(holdings.keys()), key="alert_ticker"
            )
            col_a, col_b = st.columns(2)
            alert_below  = col_a.number_input("Alert below ($)", min_value=0.0, value=0.0, key="ab")
            alert_above  = col_b.number_input("Alert above ($)", min_value=0.0, value=0.0, key="aa")

            if st.button("Set Alert", use_container_width=True):
                st.session_state.alerts[alert_ticker] = {
                    "below": alert_below if alert_below > 0 else None,
                    "above": alert_above if alert_above > 0 else None,
                }
                st.success(f"Alert set for {alert_ticker}")

            if st.session_state.alerts:
                if st.button("Clear All Alerts", use_container_width=True, type="secondary"):
                    st.session_state.alerts = {}

# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
holdings = portfolio.get_holdings()

if not holdings:
    st.info("👈 Add your first stock using the sidebar to get started!")
    st.stop()

# ── Fetch all current prices ──────────────────────────────────────────────────
with st.spinner("Fetching live prices…"):
    current_prices = {}
    for t in holdings:
        price = get_stock_price(t)
        current_prices[t] = price
        if price == 0.0:
            st.warning(f"⚠️ No live price data for **{t}** — showing $0 in calculations.")

# ── Fire price alerts (Enhancement #14) ──────────────────────────────────────
if st.session_state.alerts:
    triggered = check_alerts(st.session_state.alerts, current_prices)
    for alert in triggered:
        st.error(format_alert_message(alert))

# ── Enhancement #7: Profit / Loss Summary Cards ───────────────────────────────
total_invested = sum(d["shares"] * d["buy_price"] for d in holdings.values())
total_value    = calculate_portfolio_value(holdings, current_prices)
total_gain     = total_value - total_invested
gain_pct       = (total_gain / total_invested * 100) if total_invested else 0

st.markdown('<p class="section-header">💰 Portfolio Summary</p>', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Invested",  f"${total_invested:,.2f}")
c2.metric("Current Value",   f"${total_value:,.2f}")
c3.metric("Total Gain/Loss", f"${total_gain:,.2f}",  delta=f"{gain_pct:.2f}%")
c4.metric("Holdings",        len(holdings))

# ── Enhancement #3: Per-stock metric cards ────────────────────────────────────
st.markdown('<p class="section-header">📋 Holdings Overview</p>', unsafe_allow_html=True)
cols = st.columns(min(len(holdings), 5))
for i, (t, d) in enumerate(holdings.items()):
    ret = calculate_returns(d["buy_price"], current_prices[t])
    cols[i % 5].metric(
        label=t,
        value=f"${current_prices[t]:.2f}",
        delta=f"{ret:.2f}%",
        help=f"{d['shares']} shares · bought at ${d['buy_price']:.2f}",
    )

# ── Enhancement #2: Holdings Table ───────────────────────────────────────────
st.markdown('<p class="section-header">📄 Detailed Holdings</p>', unsafe_allow_html=True)
tickers = list(holdings.keys())
rows = []
for t in tickers:
    d   = holdings[t]
    ret = calculate_returns(d["buy_price"], current_prices[t])
    rows.append({
        "Ticker":        t,
        "Shares":        d["shares"],
        "Avg Buy Price": round(d["buy_price"],    2),
        "Current Price": round(current_prices[t], 2),
        "Market Value":  round(d["shares"] * current_prices[t], 2),
        "Return %":      round(ret, 2),
        "P&L ($)":       round(d["shares"] * (current_prices[t] - d["buy_price"]), 2),
    })

df_table = pd.DataFrame(rows)
st.dataframe(
    df_table.style.map(
        lambda v: "color: #16a34a" if v > 0 else ("color: #dc2626" if v < 0 else ""),
        subset=["Return %", "P&L ($)"],
    ),
    width="stretch",
    hide_index=True,
)

# ── Enhancement #9: CSV Export ────────────────────────────────────────────────
st.download_button(
    label="⬇️ Export Portfolio as CSV",
    data=df_table.to_csv(index=False),
    file_name="my_portfolio.csv",
    mime="text/csv",
)

st.divider()

# ── Charts Row 1: Returns bar + Pie ──────────────────────────────────────────
returns = [calculate_returns(holdings[t]["buy_price"], current_prices[t]) for t in tickers]

col_left, col_right = st.columns(2)
with col_left:
    st.plotly_chart(plot_returns_bar(tickers, returns), width="stretch")
with col_right:
    st.plotly_chart(plot_portfolio_pie(holdings, current_prices), width="stretch")

st.divider()

# ── Enhancement #4: Period picker + Price History + Volume ───────────────────
st.markdown('<p class="section-header">📉 Price & Volume History</p>', unsafe_allow_html=True)

col_sel, col_period = st.columns([2, 1])
with col_sel:
    selected = st.selectbox("Select a stock", tickers)
with col_period:
    period = st.selectbox("Period", ["1mo", "3mo", "6mo", "1y", "2y"], index=2)

hist = get_historical_data(selected, period=period)

if not hist.empty:
    st.plotly_chart(plot_price_history(hist, selected), width="stretch")  # Enhancement #4 range slider
    st.plotly_chart(plot_volume_bar(hist, selected),    width="stretch")   # Enhancement #5 volume
else:
    st.warning(f"No historical data available for {selected}.")

st.divider()

# ── Enhancement #13: Risk Metrics ────────────────────────────────────────────
st.markdown('<p class="section-header">⚖️ Risk Metrics — {}</p>'.format(selected), unsafe_allow_html=True)

if not hist.empty and len(hist) >= 10:
    daily_returns = hist["Close"].pct_change().dropna()
    sharpe    = calculate_sharpe_ratio(daily_returns)
    drawdown  = calculate_max_drawdown(hist["Close"])
    volatility = daily_returns.std() * (252 ** 0.5) * 100  # Annualised volatility %

    r1, r2, r3 = st.columns(3)
    r1.metric(
        "Sharpe Ratio",
        f"{sharpe:.2f}",
        help="Risk-adjusted return. >1 is good, >2 is great, <0 is poor.",
    )
    r2.metric(
        "Max Drawdown",
        f"{drawdown:.2f}%",
        help="Largest peak-to-trough % drop in the selected period.",
    )
    r3.metric(
        "Annual Volatility",
        f"{volatility:.2f}%",
        help="Annualised standard deviation of daily returns.",
    )
else:
    st.info("Not enough historical data to calculate risk metrics.")

st.divider()

# ── Enhancement #8: News Feed ─────────────────────────────────────────────────
st.markdown(f'<p class="section-header">📰 Latest News — {selected}</p>', unsafe_allow_html=True)

news = get_stock_news(selected, limit=5)
if news:
    for article in news:
        st.markdown(
            f'<div class="news-item">📌 <a href="{article["link"]}" target="_blank">'
            f'{article["title"]}</a> &nbsp;'
            f'<span style="color:#888;font-size:0.8em">— {article["publisher"]}</span></div>',
            unsafe_allow_html=True,
        )
else:
    st.info(f"No recent news found for {selected}.")

st.divider()

# ── Enhancement #15: AI Insights ─────────────────────────────────────────────
st.markdown(f'<p class="section-header">🤖 AI Insights — {selected}</p>', unsafe_allow_html=True)

with st.expander("Click to generate AI analysis", expanded=False):
    if st.button("🔍 Analyse with Gemini AI"):
        ret_selected = calculate_returns(
            holdings[selected]["buy_price"], current_prices[selected]
        )
        with st.spinner("Asking Gemini AI…"):
            insight = get_stock_insight(selected, current_prices[selected], ret_selected, hist)
        st.markdown(insight)
