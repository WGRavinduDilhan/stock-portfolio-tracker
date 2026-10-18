"""
app.py — Stock Portfolio Tracker & Analytics Dashboard
Enhanced version with 14 new features.
"""

import time
import math
import re
from datetime import datetime

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

_TICKER_PATTERN = re.compile(r"^[A-Z][A-Z0-9.-]{0,9}$")


def _is_valid_ticker(ticker: str) -> bool:
    return bool(_TICKER_PATTERN.fullmatch(ticker))


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
    .stApp { background-color: #f8fafc; }
    [data-testid="stHeader"] { background: rgba(248,250,252,0.86); }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #eff6ff 0%, #f8fafc 42%);
        border-right: 1px solid #dbeafe;
    }
    .hero {
        background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 58%, #60a5fa 100%);
        border-radius: 18px;
        padding: 1.5rem 1.8rem;
        margin: 0.3rem 0 1.2rem;
        color: white;
        box-shadow: 0 10px 24px rgba(37,99,235,0.18);
    }
    .hero-eyebrow {
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        opacity: 0.82;
        text-transform: uppercase;
    }
    .hero-title {
        font-size: clamp(1.8rem, 4vw, 2.65rem);
        font-weight: 750;
        line-height: 1.1;
        margin: 0.3rem 0 0.45rem;
    }
    .hero-subtitle { margin: 0; opacity: 0.9; }
    .status-strip {
        background: #ffffff;
        border: 1px solid #dbeafe;
        border-radius: 10px;
        color: #475569;
        font-size: 0.86rem;
        padding: 0.55rem 0.8rem;
        margin: 0.4rem 0 1rem;
    }
    div[data-testid="metric-container"] {
        background    : #ffffff;
        border        : 1px solid #e2e8f0;
        border-radius : 10px;
        padding       : 12px 16px;
        box-shadow    : 0 1px 4px rgba(0,0,0,0.06);
        min-height    : 92px;
    }
    .section-header {
        font-size     : 1.05rem;
        font-weight   : 600;
        color         : #2563eb;
        margin        : 1.4rem 0 0.5rem 0;
        border-bottom : 2px solid #dbeafe;
        padding-bottom: 7px;
    }
    .sidebar-note {
        background: rgba(255,255,255,0.72);
        border: 1px solid #dbeafe;
        border-radius: 10px;
        color: #475569;
        font-size: 0.82rem;
        line-height: 1.45;
        padding: 0.7rem 0.8rem;
    }
    .news-item {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 3px solid #60a5fa;
        border-radius: 8px;
        margin-bottom: 8px;
        padding: 0.65rem 0.8rem;
    }
    .news-item a { color: #1d4ed8; font-weight: 600; }
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <div class="hero">
        <div class="hero-eyebrow">Personal investing workspace</div>
        <div class="hero-title">📈 Stock Portfolio Tracker</div>
        <p class="hero-subtitle">
            Monitor holdings, understand performance, and explore market trends in one place.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

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
    st.markdown(
        '<div class="sidebar-note">Add a Yahoo Finance ticker, shares, and '
        'your average purchase price to start tracking a position.</div>',
        unsafe_allow_html=True,
    )
    st.header("➕ Add a Stock")
    ticker = st.text_input(
        "Ticker Symbol",
        placeholder="AAPL or MSFT",
        help="Use the Yahoo Finance symbol, for example GOOGL rather than GOOGLE.",
    ).upper().strip()
    shares = st.number_input(
        "Number of Shares", min_value=0.01, step=0.01, format="%.2f"
    )
    buy_price = st.number_input(
        "Buy Price per Share ($)", min_value=0.01, step=0.01, format="%.2f"
    )

    if st.button("Add to Portfolio", use_container_width=True):
        if not _is_valid_ticker(ticker):
            st.error("Enter a valid ticker symbol, such as AAPL or GOOGL.")
        elif not math.isfinite(shares) or not math.isfinite(buy_price):
            st.error("Shares and buy price must be valid numbers.")
        elif ticker:
            portfolio.add_stock(ticker, shares, buy_price)
            st.success(f"✅ Added {ticker} to portfolio!")

    if st.button("🔄 Refresh Market Data", use_container_width=True):
        st.rerun()

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
                st.success(f"Removed {ticker_to_remove} from the portfolio.")
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

    st.divider()
    st.caption("Market data is provided by Yahoo Finance and may be delayed.")

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
            st.warning(
                f"⚠️ No live price data for **{t}** — check that it is a valid "
                "Yahoo Finance symbol."
            )

st.caption(
    f"Last updated: {datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z')}"
)
available_prices = sum(price > 0 for price in current_prices.values())
st.markdown(
    f'<div class="status-strip">🟢 Market data available for '
    f'<strong>{available_prices}/{len(holdings)}</strong> holdings · '
    "Use Refresh Market Data in the sidebar to fetch the latest values.</div>",
    unsafe_allow_html=True,
)

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
    column_config={
        "Shares": st.column_config.NumberColumn(format="%.2f"),
        "Avg Buy Price": st.column_config.NumberColumn(format="$%.2f"),
        "Current Price": st.column_config.NumberColumn(format="$%.2f"),
        "Market Value": st.column_config.NumberColumn(format="$%.2f"),
        "Return %": st.column_config.NumberColumn(format="%.2f%%"),
        "P&L ($)": st.column_config.NumberColumn(format="$%.2f"),
    },
)

# ── Enhancement #9: CSV Export ────────────────────────────────────────────────
export_col, export_hint = st.columns([1, 2])
with export_col:
    st.download_button(
        label="⬇️ Export CSV",
        data=df_table.to_csv(index=False),
        file_name="my_portfolio.csv",
        mime="text/csv",
        use_container_width=True,
    )
with export_hint:
    st.caption("Download a snapshot of your holdings and performance.")

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
