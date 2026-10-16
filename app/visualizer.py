import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# ── Shared light-theme layout defaults ────────────────────────────────────────
_LAYOUT = dict(
    template       = "plotly_white",
    paper_bgcolor  = "#ffffff",
    plot_bgcolor   = "#f8fafc",
    font           = dict(color="#1e293b", family="Inter, sans-serif"),
    hovermode      = "x unified",
    margin         = dict(l=40, r=20, t=50, b=40),
)

_ACCENT   = "#2563eb"   # Blue
_POSITIVE = "#16a34a"   # Green
_NEGATIVE = "#dc2626"   # Red
_GRID     = "#e2e8f0"   # Light grey grid lines


# ── Price History Line Chart ──────────────────────────────────────────────────
def plot_price_history(df: pd.DataFrame, ticker: str) -> go.Figure:
    """
    Line chart of closing price with interactive range selector buttons.
    Buttons: 1M / 3M / 6M / 1Y / All
    """
    fig = px.line(
        df, x=df.index, y="Close",
        title=f"📈 {ticker} — Price History",
        labels={"Close": "Price (USD)", "index": "Date"},
    )
    fig.update_traces(line_color=_ACCENT, line_width=2.5)
    fig.update_layout(
        **_LAYOUT,
        xaxis=dict(
            showgrid=True, gridcolor=_GRID,
            rangeselector=dict(
                buttons=[
                    dict(count=1,  label="1M", step="month", stepmode="backward"),
                    dict(count=3,  label="3M", step="month", stepmode="backward"),
                    dict(count=6,  label="6M", step="month", stepmode="backward"),
                    dict(count=1,  label="1Y", step="year",  stepmode="backward"),
                    dict(step="all", label="All"),
                ],
                bgcolor="#f0f4f8",
                activecolor=_ACCENT,
                font=dict(color="#1e293b"),
            ),
            rangeslider=dict(visible=True, bgcolor="#f0f4f8"),
            type="date",
        ),
        yaxis=dict(showgrid=True, gridcolor=_GRID),
    )
    return fig


# ── Volume Bar Chart ──────────────────────────────────────────────────────────
def plot_volume_bar(df: pd.DataFrame, ticker: str) -> go.Figure:
    """Bar chart of daily trading volume."""
    fig = go.Figure(
        go.Bar(
            x=df.index,
            y=df["Volume"],
            marker_color=_ACCENT,
            marker_opacity=0.7,
            name="Volume",
        )
    )
    fig.update_layout(
        **_LAYOUT,
        title=f"📊 {ticker} — Trading Volume",
        xaxis=dict(title="Date", showgrid=False),
        yaxis=dict(title="Volume", showgrid=True, gridcolor=_GRID),
    )
    return fig


# ── Portfolio Allocation Donut Chart ─────────────────────────────────────────
def plot_portfolio_pie(holdings: dict, current_prices: dict) -> go.Figure:
    """Donut chart showing portfolio allocation by current market value."""
    labels, values, custom = [], [], []
    colors = px.colors.qualitative.Pastel   # Soft pastel palette for light theme

    for ticker, data in holdings.items():
        val = data["shares"] * current_prices.get(ticker, 0)
        labels.append(ticker)
        values.append(val)
        custom.append(
            f"Shares: {data['shares']}<br>"
            f"Price: ${current_prices.get(ticker, 0):.2f}<br>"
            f"Value: ${val:,.2f}"
        )

    fig = go.Figure(
        go.Pie(
            labels=labels,
            values=values,
            hole=0.45,
            marker_colors=colors,
            customdata=custom,
            hovertemplate="%{label}<br>%{customdata}<extra></extra>",
            textinfo="label+percent",
            textfont=dict(color="#1e293b"),
        )
    )
    fig.update_layout(
        **_LAYOUT,
        title="🥧 Portfolio Allocation",
        legend=dict(orientation="h", yanchor="bottom", y=-0.25),
    )
    return fig


# ── Returns Bar Chart ─────────────────────────────────────────────────────────
def plot_returns_bar(tickers: list, returns: list) -> go.Figure:
    """Bar chart of % return per stock with value labels."""
    colors = [_POSITIVE if r > 0 else _NEGATIVE for r in returns]
    text   = [f"{r:.2f}%" for r in returns]

    fig = go.Figure(
        go.Bar(
            x=tickers,
            y=returns,
            marker_color=colors,
            marker_opacity=0.85,
            text=text,
            textposition="outside",
            textfont=dict(color="#1e293b"),
        )
    )
    fig.update_layout(
        **_LAYOUT,
        title="📊 Return % per Stock",
        yaxis=dict(
            title="Return (%)",
            showgrid=True,
            gridcolor=_GRID,
            zeroline=True,
            zerolinecolor="#94a3b8",
            zerolinewidth=1.5,
        ),
    )
    return fig
