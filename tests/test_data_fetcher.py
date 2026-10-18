from unittest.mock import Mock, patch

import pandas as pd

from app.data_fetcher import get_historical_data, get_stock_info, get_stock_news


@patch("app.data_fetcher.yf.Ticker")
def test_get_historical_data_returns_close_and_volume(mock_ticker):
    mock_ticker.return_value.history.return_value = pd.DataFrame(
        {"Close": [100.0], "Volume": [1000]}
    )

    result = get_historical_data("AAPL")

    assert list(result.columns) == ["Close", "Volume"]
    assert result.iloc[0]["Close"] == 100.0


@patch("app.data_fetcher.yf.Ticker")
def test_get_stock_info_maps_company_fields(mock_ticker):
    mock_ticker.return_value.info = {
        "longName": "Example Corp",
        "sector": "Technology",
        "marketCap": 123456,
    }

    assert get_stock_info("AAPL") == {
        "name": "Example Corp",
        "sector": "Technology",
        "market_cap": 123456,
    }


@patch("app.data_fetcher.yf.Ticker")
def test_get_stock_news_supports_nested_yfinance_format(mock_ticker):
    mock_ticker.return_value.news = [
        {
            "content": {
                "title": "Example headline",
                "canonicalUrl": {"url": "https://example.com/article"},
                "provider": {"displayName": "Example News"},
            }
        }
    ]

    assert get_stock_news("AAPL") == [
        {
            "title": "Example headline",
            "link": "https://example.com/article",
            "publisher": "Example News",
        }
    ]


@patch("app.data_fetcher.yf.Ticker")
def test_get_historical_data_returns_empty_frame_on_provider_error(mock_ticker):
    mock_ticker.return_value.history.side_effect = RuntimeError("provider unavailable")

    result = get_historical_data("AAPL")

    assert result.empty
    assert list(result.columns) == ["Close", "Volume"]
