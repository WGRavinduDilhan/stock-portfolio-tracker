import pandas as pd

from app.visualizer import (
    plot_portfolio_pie,
    plot_price_history,
    plot_returns_bar,
    plot_volume_bar,
)


def test_plot_price_history_creates_line_figure():
    frame = pd.DataFrame(
        {"Close": [100.0, 105.0], "Volume": [1000, 1200]},
        index=pd.date_range("2026-01-01", periods=2),
    )

    figure = plot_price_history(frame, "AAPL")

    assert len(figure.data) == 1
    assert list(figure.data[0].y) == [100.0, 105.0]


def test_plot_volume_bar_creates_bar_figure():
    frame = pd.DataFrame(
        {"Close": [100.0], "Volume": [1000]},
        index=pd.date_range("2026-01-01", periods=1),
    )

    figure = plot_volume_bar(frame, "AAPL")

    assert len(figure.data) == 1
    assert figure.data[0].name == "Volume"


def test_plot_portfolio_pie_uses_current_market_values():
    holdings = {"AAPL": {"shares": 2, "buy_price": 100.0}}

    figure = plot_portfolio_pie(holdings, {"AAPL": 150.0})

    assert list(figure.data[0].values) == [300.0]


def test_plot_returns_bar_colours_positive_and_negative_returns():
    figure = plot_returns_bar(["AAPL", "TSLA"], [10.0, -5.0])

    assert list(figure.data[0].marker.color) == ["#16a34a", "#dc2626"]
