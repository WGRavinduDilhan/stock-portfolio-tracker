class Portfolio:
    def __init__(self):
        self.holdings = {} # Dictionary to store stock holdings 

    def add_stock(self, ticker, shares, buy_price):
        if ticker in self.holdings:
            old_shares = self.holdings[ticker]["shares"]     #if there are already existing holdings calculate avaerage price and update shares
            old_shares_price = self.holdings[ticker]["buy_price"]
            total_shares = old_shares + shares
            avg_price = (old_shares * old_shares_price + shares * buy_price) / total_shares
            self.holdings[ticker] = {"shares": total_shares, "buy_price": avg_price}  # Update stock in holdings
        else:
            self.holdings[ticker] = {"shares": shares, "buy_price": buy_price}  # Add stock to holdings fromat like given
    

    def remove_stock(self, ticker):
        self.holdings.pop(ticker, None)  # Remove stock from holdings if it inside 

    def get_holdings(self):
        return self.holdings  # Return current holdings         







