import pandas as pd
import numpy as np
from app.metrics import (
    calculate_returns,
    calculate_portfolio_value,
    calculate_sharpe_ratio,
    calculate_max_drawdown
)

def test_calculate_returns_positive():
    result = calculate_returns(100, 150)
    assert result == 50.0

def test_calculate_returns_negative():
    result = calculate_returns(200, 100)
    assert result == -50.0

def test_calculate_returns_zero():
    result = calculate_returns(100, 100)
    assert result == 0.0

def test_portfolio_value_single_stock():
    holdings = {"AAPL": {"shares": 10, "buy_price": 150}}
    current = {"AAPL": 175}
    result = calculate_portfolio_value(holdings, current)
    assert result == 1750.0

def test_portfolio_value_multiple_stocks():
    holdings = {
        "AAPL": {"shares": 10, "buy_price": 150},
        "TSLA": {"shares": 5, "buy_price": 200}
    }
    current = {"AAPL": 175, "TSLA": 250}
    result = calculate_portfolio_value(holdings, current)
    assert result == 3000.0

def test_portfolio_value_missing_price():
    holdings = {"AAPL": {"shares": 10, "buy_price": 150}}
    current = {}  # Missing price
    result = calculate_portfolio_value(holdings, current)
    assert result == 0.0  # Should use default 0

def test_sharpe_ratio():
    daily_returns = pd.Series([0.01, 0.02, -0.01, 0.015, 0.005])
    result = calculate_sharpe_ratio(daily_returns)
    assert isinstance(result, float)
    assert not np.isnan(result)

def test_max_drawdown():
    prices = pd.Series([100, 120, 80, 90, 110])
    result = calculate_max_drawdown(prices)
    assert result < 0  # Should be negative
    assert abs(result - (-33.33)) < 0.1  # Should be close to -33.33%

def test_max_drawdown_no_decline():
    prices = pd.Series([100, 110, 120, 130])
    result = calculate_max_drawdown(prices)
    assert result == 0.0  # No drawdown