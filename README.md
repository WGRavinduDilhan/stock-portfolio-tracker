# 📈 Stock Portfolio Tracker & Analytics Dashboard

A professional-grade **Stock Portfolio Tracker & Analyzer** built with Python that allows users to track live stock prices, analyze portfolio performance, and visualize their investments through an interactive Streamlit dashboard. Perfect for individual investors, financial analysts, and anyone interested in monitoring their stock market investments in real-time.

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.54.0-FF4B4B.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 🌟 Features

### Core Functionality
- ✅ **Real-time Stock Price Tracking** - Fetch live stock prices using Yahoo Finance API
- ✅ **Portfolio Management** - Add, remove, and manage multiple stock holdings
- ✅ **Automatic Average Price Calculation** - Smart averaging when adding more shares of existing stocks
- ✅ **Multi-Stock Support** - Track unlimited stocks in your portfolio simultaneously

### Analytics & Metrics
- 📊 **Return Percentage Calculation** - Calculate gains/losses for each stock position
- 💰 **Total Portfolio Value** - Real-time calculation of total portfolio worth
- 📉 **Sharpe Ratio** - Measure risk-adjusted returns (optional advanced metric)
- 📈 **Maximum Drawdown** - Track the largest peak-to-trough decline

### Visualizations
- 🥧 **Portfolio Allocation Pie Chart** - Visual breakdown of portfolio composition
- 📊 **Returns Bar Chart** - Color-coded profit/loss visualization (green for gains, red for losses)
- 📈 **Historical Price Charts** - Interactive 6-month price history for each stock
- 🌙 **Dark Theme UI** - Professional dark mode for comfortable viewing

### User Experience
- 🚀 **Interactive Dashboard** - Built with Streamlit for seamless user interaction
- ⚡ **Fast Performance** - Efficient data fetching with error handling
- 🛡️ **Robust Error Handling** - Graceful handling of API failures and invalid tickers
- 🔄 **Session Persistence** - Portfolio data persists during the session

---

## 🛠️ Tech Stack For this Project

| Technology        | Purpose                                    | 
|-------------------|--------------------------------------------|
| **Python 3.11+**  | Core programming language                  |
| **Streamlit**     | Web application framework and dashboard UI |
| **yfinance**      | Yahoo Finance API wrapper for stock data   |
| **Pandas**        | Data manipulation and analysis             |
| **NumPy**         | Numerical computations                     |
| **Plotly**        | Interactive data visualizations            |
| **Pytest**        | Unit testing framework                     |
| **Docker**        | Containerization for easy deployment       |

---

## 📂 Project File Structure

```
stock-portfolio-tracker/
│
├── app.py                      # Main Streamlit application entry point
├── requirements.txt            # Python dependencies
├── setup.py                    # Package setup configuration
├── Dockerfile                  # Docker container configuration
├── README.md                   # Project documentation
│
├── app/                        # Core application modules
│   ├── __init__.py            # Package initializer
│   ├── portfolio.py           # Portfolio management logic
│   ├── data_fetcher.py        # Stock data fetching from Yahoo Finance
│   ├── metrics.py             # Financial calculations (returns, Sharpe, etc.)
│   └── visualizer.py          # Plotly chart generation functions
│
├── tests/                      # Unit tests
│   ├── test_portfolio.py      # Portfolio class tests
│   ├── test_data_fetcher.py   # Data fetching tests
│   ├── test_metrics.py        # Metrics calculation tests
│   └── test_visualizer.py     # Visualization tests
│
└── stock_portfolio_tracker.egg-info/  # Package metadata (auto-generated)
```

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11 or higher** ([Download Python](https://www.python.org/downloads/))
- **pip** (Python package installer - comes with Python)
- **Git** (optional, for cloning the repository)
- **Docker** (optional, for containerized deployment)

---

## 🚀 Installation & Setup

### Method 1: Local Installation (Recommended for Development)

#### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/stock-portfolio-tracker.git
cd stock-portfolio-tracker
```

Or download and extract the ZIP file from the repository.

#### Step 2: Create a Virtual Environment (Recommended)
```bash
# Windows

python -m venv venv
venv\Scripts\activate

# macOS/Linux

python3 -m venv venv
source venv/bin/activate
```

#### Step 3: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Or install the package in development mode:
```bash
pip install -e .
```

#### Step 4: Run the Application
```bash
streamlit run app.py
```

The application will automatically open in your default web browser at `http://localhost:8501`

---

### Method 2: Docker Installation (Recommended for Production)

#### Step 1: Build the Docker Image
```bash
docker build -t stock-portfolio-tracker .
```

#### Step 2: Run the Container
```bash
docker run -p 8501:8501 stock-portfolio-tracker
```

#### Step 3: Access the Application
Open your browser and navigate to: `http://localhost:8501`

**To stop the container:**
```bash
# Find the container ID
docker ps

# Stop the container
docker stop <container_id>
```

---

## 📖 Usage Guide

### Adding Stocks to Your Portfolio

1. **Launch the Application** - Run `streamlit run app.py`
2. **Enter Stock Details** in the sidebar:
   - **Ticker Symbol**: Enter the stock symbol (e.g., AAPL, TSLA, MSFT, GOOGL)
   - **Number of Shares**: Input how many shares you own
   - **Buy Price per Share**: Enter the price you paid per share
3. **Click "Add to Portfolio"** - The stock will be added to your dashboard

### Adding More Shares of Existing Stock

If you add more shares of a stock you already own, the application will:
- Automatically calculate the **average buy price** across all purchases
- Update the **total share count**

**Example:**
- First purchase: 10 shares of AAPL at $150
- Second purchase: 20 shares of AAPL at $160
- **Result**: 30 shares at average price of $156.67

### Viewing Analytics

Once you have stocks in your portfolio, you'll see:

1. **Total Portfolio Value** - Displayed at the top (updates in real-time)
2. **Returns Bar Chart** - Shows profit/loss percentage for each stock
   - Green bars = Profit
   - Red bars = Loss
3. **Portfolio Allocation Pie Chart** - Visual breakdown of your investment distribution
4. **Historical Price Chart** - Select any stock from the dropdown to view its 6-month price history

### Understanding the Metrics

- **Return %**: `((Current Price - Buy Price) / Buy Price) × 100`
- **Portfolio Value**: Sum of (Shares × Current Price) for all holdings
- **Sharpe Ratio**: Risk-adjusted return metric (higher is better)
- **Max Drawdown**: Largest peak-to-trough decline (shown as negative percentage)

---

## 🧪 Running Tests

The project includes comprehensive unit tests for all core functionality.

### Run All Tests
```bash
pytest
```

### Run Tests with Verbose Output
```bash
pytest -v
```

### Run Tests for Specific Module
```bash
pytest tests/test_portfolio.py
pytest tests/test_metrics.py
pytest tests/test_data_fetcher.py
```

### Check Test Coverage
```bash
pip install pytest-cov
pytest --cov=app --cov-report=html
```

---

## 🔧 Module Documentation

### `portfolio.py` - Portfolio Management

```python
class Portfolio:
    def add_stock(ticker, shares, buy_price)
        # Adds stock to portfolio or updates if exists with average pricing
    
    def remove_stock(ticker)
        # Removes stock from portfolio
    
    def get_holdings()
        # Returns dictionary of all holdings
```

### `data_fetcher.py` - Stock Data Retrieval

```python
def get_stock_price(ticker: str) -> float
    # Fetches current stock price from Yahoo Finance
    # Returns 0.0 if error occurs

def get_historical_data(ticker: str, period: str = "6mo") -> DataFrame
    # Retrieves historical price data
    # Default period: 6 months

def get_stock_info(ticker: str) -> dict
    # Gets stock metadata (name, sector, market cap)
```

### `metrics.py` - Financial Calculations

```python
def calculate_returns(buy_price, current_price)
    # Returns percentage gain/loss

def calculate_portfolio_value(holdings, current_prices)
    # Calculates total portfolio worth

def calculate_sharpe_ratio(daily_returns, risk_free_rate=0.05)
    # Computes risk-adjusted returns

def calculate_max_drawdown(price_series)
    # Finds maximum peak-to-trough decline
```

### `visualizer.py` - Chart Generation

```python
def plot_price_history(df, ticker)
    # Creates line chart of historical prices

def plot_portfolio_pie(holdings, current_prices)
    # Generates donut chart of portfolio allocation

def plot_returns_bar(tickers, returns)
    # Creates bar chart with color-coded returns
```

---

## 🎨 Customization

### Change Default Time Period for Historical Data

Edit `app.py` line where `get_historical_data` is called:

```python
hist = get_historical_data(selected, period="1y")  # Change from "6mo" to "1y"
```

Available periods: `1d`, `5d`, `1mo`, `3mo`, `6mo`, `1y`, `2y`, `5y`, `10y`, `ytd`, `max`

### Modify Risk-Free Rate for Sharpe Ratio

Edit `metrics.py`:

```python
def calculate_sharpe_ratio(daily_returns, risk_free_rate=0.03)  # Change from 0.05
```

### Change Chart Theme

Edit `visualizer.py` - replace `template="plotly_dark"` with:
- `"plotly"` (light theme)
- `"plotly_white"`
- `"seaborn"`
- `"ggplot2"`

---

## ⚠️ Troubleshooting

### Issue: "No price data found for [TICKER]"

**Cause**: Invalid ticker symbol or Yahoo Finance API issue

**Solution**:
- Verify the ticker symbol is correct (use Yahoo Finance website to confirm)
- Try again after a few minutes (API rate limiting)
- Check your internet connection

### Issue: Application won't start

**Cause**: Missing dependencies or Python version incompatibility

**Solution**:
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Check Python version (must be 3.11+)
python --version
```

### Issue: Docker container fails to build

**Cause**: Docker daemon not running or insufficient permissions

**Solution**:
- Ensure Docker Desktop is running
- On Linux, add user to docker group: `sudo usermod -aG docker $USER`
- Restart terminal/computer

### Issue: Slow performance when adding many stocks

**Cause**: Yahoo Finance API rate limiting

**Solution**:
- Add delay between API calls (uncomment `time.sleep(0.5)` in `app.py`)
- Consider implementing caching mechanism
- Use fewer stocks simultaneously

---

## 🔐 Security & Privacy

- ✅ **No API Keys Required** - Uses public Yahoo Finance data
- ✅ **No Data Storage** - All portfolio data is session-based (not saved to disk)
- ✅ **No Personal Information Collected** - Completely private and local
- ⚠️ **Yahoo Finance Terms** - Ensure compliance with [Yahoo Finance Terms of Service](https://legal.yahoo.com/us/en/yahoo/terms/otos/index.html)

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/AmazingFeature`
3. **Make your changes** and add tests
4. **Commit your changes**: `git commit -m 'Add some AmazingFeature'`
5. **Push to the branch**: `git push origin feature/AmazingFeature`
6. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guidelines
- Write unit tests for new features
- Update documentation for API changes
- Add comments for complex logic

---

## 🗺️ Roadmap & Future Features

- [ ] **Portfolio Persistence** - Save/load portfolio data to JSON/Database
- [ ] **Multiple Portfolios** - Support for managing multiple portfolios
- [ ] **Export Reports** - Generate PDF/Excel reports
- [ ] **Advanced Analytics** - Add more metrics (Beta, Alpha, Volatility)
- [ ] **Alerts & Notifications** - Price alerts and thresholds
- [ ] **News Integration** - Display relevant stock news
- [ ] **Cryptocurrency Support** - Track crypto alongside stocks
- [ ] **User Authentication** - Multi-user support with accounts
- [ ] **Mobile Responsive Design** - Improved mobile experience
- [ ] **Dark/Light Theme Toggle** - User-selectable themes

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Ravindu**

- GitHub: [@WGRavinduDilhan]
- LinkedIn: [My LinkedIn](www.linkedin.com/in/ravindu-dilhan-7aa47231b)

---

## 🙏 Acknowledgments

- [Yahoo Finance](https://finance.yahoo.com/) for providing free stock market data
- [Streamlit](https://streamlit.io/) for the amazing web app framework
- [Plotly](https://plotly.com/) for beautiful interactive visualizations
- The Python open-source community for excellent libraries

---

## 📞 Support

If you encounter any issues or have questions:

1. **Check the [Troubleshooting](#-troubleshooting) section** above
2. **Open an issue** on GitHub with detailed description
3. **Check existing issues** - your question might already be answered

---

## ⭐ Show Your Support

If you find this project useful, please consider:

- ⭐ **Starring the repository** on GitHub
- 🍴 **Forking the project** to build your own version
- 🐛 **Reporting bugs** to help improve the project
- 💡 **Suggesting features** for future enhancements

---

## 📊 Project Status

**Status**: Active Development 🟢

**Current Version**: 0.1.0

**Last Updated**: March 2026

---

**Happy Investing! 📈💰**
