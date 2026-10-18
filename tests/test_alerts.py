from app.alerts import check_alerts, format_alert_message


def test_check_alerts_returns_below_and_above_alerts():
    alerts = {
        "AAPL": {"below": 150.0, "above": None},
        "MSFT": {"below": None, "above": 400.0},
    }

    result = check_alerts(alerts, {"AAPL": 140.0, "MSFT": 410.0})

    assert result == [
        {"ticker": "AAPL", "type": "below", "threshold": 150.0, "current": 140.0},
        {"ticker": "MSFT", "type": "above", "threshold": 400.0, "current": 410.0},
    ]


def test_check_alerts_ignores_missing_and_zero_prices():
    alerts = {"AAPL": {"below": 150.0, "above": 200.0}}

    assert check_alerts(alerts, {"AAPL": 0.0}) == []
    assert check_alerts(alerts, {}) == []


def test_format_alert_message_describes_direction_and_values():
    message = format_alert_message(
        {"ticker": "AAPL", "type": "below", "threshold": 150.0, "current": 140.0}
    )

    assert "AAPL" in message
    assert "dropped below" in message
    assert "$150.00" in message
