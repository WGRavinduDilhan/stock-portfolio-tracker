"""
ai_insights.py — Google Gemini AI stock analysis for the Stock Portfolio Tracker.

Requires:  GEMINI_API_KEY in .env
Package:   google-generativeai (already in requirements.txt)
"""

import os
import pandas as pd


def get_stock_insight(
    ticker: str,
    current_price: float,
    return_pct: float,
    hist_df: pd.DataFrame,
) -> str:
    """
    Call Google Gemini to generate a brief stock analysis.

    Args:
        ticker:        Stock symbol (e.g. "AAPL")
        current_price: Latest price in USD
        return_pct:    Portfolio return % since buy
        hist_df:       DataFrame with Close + Volume columns

    Returns:
        AI-generated insight text, or an error/placeholder message.
    """
    api_key = os.getenv("GEMINI_API_KEY", "")

    if not api_key or api_key == "your_gemini_api_key_here":
        return (
            "🔑 **AI Insights not configured.**\n\n"
            "To enable this feature:\n"
            "1. Get a free API key at https://aistudio.google.com/app/apikey\n"
            "2. Add `GEMINI_API_KEY=your_key` to your `.env` file\n"
            "3. Restart the app / rebuild Docker"
        )

    try:
        import google.generativeai as genai

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Build a compact context from historical data
        if not hist_df.empty:
            recent  = hist_df["Close"].tail(30)
            high_30 = recent.max()
            low_30  = recent.min()
            avg_30  = recent.mean()
            vol_avg = hist_df["Volume"].tail(30).mean()
        else:
            high_30 = low_30 = avg_30 = vol_avg = 0

        prompt = f"""
You are a concise financial analyst assistant. Provide a brief, factual analysis 
(3-4 sentences max) for the following stock data. Do NOT give buy/sell advice.

Stock: {ticker}
Current Price: ${current_price:.2f}
My Portfolio Return: {return_pct:.2f}%
30-Day High: ${high_30:.2f}
30-Day Low:  ${low_30:.2f}
30-Day Avg:  ${avg_30:.2f}
Avg Volume (30d): {vol_avg:,.0f}

Summarise the recent price trend and any notable observations from these numbers.
""".strip()

        response = model.generate_content(prompt)
        return response.text

    except ImportError:
        return "⚠️ `google-generativeai` package not installed. Rebuild Docker."
    except Exception as e:
        return f"⚠️ AI Insights error: {e}"
