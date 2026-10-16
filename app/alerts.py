"""
alerts.py — Price alert logic for the Stock Portfolio Tracker.

Alert format stored in session state:
    st.session_state.alerts = {
        "AAPL": {"below": 150.0, "above": 200.0},
        "TSLA": {"below": 100.0, "above": None},
    }
"""


def check_alerts(alerts: dict, current_prices: dict) -> list[dict]:
    """
    Compare current prices against user-defined alert thresholds.

    Args:
        alerts:         dict of {ticker: {"below": float|None, "above": float|None}}
        current_prices: dict of {ticker: float}

    Returns:
        List of triggered alerts, each as:
            {"ticker": str, "type": "below"|"above", "threshold": float, "current": float}
    """
    triggered = []

    for ticker, thresholds in alerts.items():
        price = current_prices.get(ticker)
        if price is None or price == 0.0:
            continue

        below = thresholds.get("below")
        above = thresholds.get("above")

        if below is not None and price < below:
            triggered.append({
                "ticker":    ticker,
                "type":      "below",
                "threshold": below,
                "current":   price,
            })

        if above is not None and price > above:
            triggered.append({
                "ticker":    ticker,
                "type":      "above",
                "threshold": above,
                "current":   price,
            })

    return triggered


def format_alert_message(alert: dict) -> str:
    """Return a human-readable alert message."""
    direction = "dropped below" if alert["type"] == "below" else "surged above"
    return (
        f"🔔 **{alert['ticker']}** has {direction} your alert of "
        f"**${alert['threshold']:.2f}** — current price: **${alert['current']:.2f}**"
    )
