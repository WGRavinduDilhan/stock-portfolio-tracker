from app.portfolio import Portfolio

def test_add_stock():
    p = Portfolio()
    p.add_stock("AAPL", 10, 150.0)
    assert "AAPL" in p.get_holdings()
    assert p.get_holdings()["AAPL"]["shares"] == 10
    assert p.get_holdings()["AAPL"]["buy_price"] == 150.0

def test_add_multiple_stocks():
    p = Portfolio()
    p.add_stock("AAPL", 10, 150.0)
    p.add_stock("TSLA", 5, 200.0)
    assert len(p.get_holdings()) == 2

def test_remove_stock():
    p = Portfolio()
    p.add_stock("AAPL", 10, 150.0)
    p.remove_stock("AAPL")
    assert len(p.get_holdings()) == 0

def test_remove_nonexistent_stock():
    p = Portfolio()
    p.remove_stock("FAKE")  # Should not crash
    assert len(p.get_holdings()) == 0

def test_overwrite_stock():
    p = Portfolio()
    p.add_stock("AAPL", 10, 150.0)
    p.add_stock("AAPL", 20, 160.0)  # Overwrite

    assert p.get_holdings()["AAPL"]["shares"] == 30  # Should sum shares
    expected_price = (10 * 150.0 + 20 * 160.0) / 30
    
    assert abs(p.get_holdings()["AAPL"]["buy_price"] - expected_price) < 0.01  # Should calculate average price correctly
    #assert p.get_holdings()["AAPL"]["buy_price"] == 160.0

def test_replace_stock():
    p = Portfolio()
    p.add_stock("AAPL", 10, 150.0)
    
    # Remove and re-add to replace
    p.remove_stock("AAPL")
    p.add_stock("AAPL", 20, 160.0)
    
    assert p.get_holdings()["AAPL"]["shares"] == 20
    assert p.get_holdings()["AAPL"]["buy_price"] == 160.0
    

