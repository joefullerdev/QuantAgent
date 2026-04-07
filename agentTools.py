import yfinance as yf
import os
from dotenv import load_dotenv
import requests

load_dotenv()

def get_stock_price(ticker: str) -> str:
    """Get real-time stock price"""
    
    stock = yf.Ticker(ticker)
    data = stock.history(period="1d")
    
    return f"{ticker} price is {data['Close'].iloc[-1]}"

def get_market_cap(ticker: str) -> str:
    """Get company market cap"""
    
    stock = yf.Ticker(ticker)
    info = stock.info
    
    return str(info.get("marketCap"))

def get_volatility(ticker: str) -> float:
    """Calculate 30 day volatility"""
    
    stock = yf.Ticker(ticker)
    data = stock.history(period="1mo")
    
    returns = data['Close'].pct_change()
    
    return float(returns.std())

def get_RSI(ticker: str) -> str:
    """
    Get RSI indicator for a stock ticker
    """
    
    data = yf.download(ticker, period="3mo")
    
    delta = data["Close"].diff()
    
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    latest_rsi = rsi.iloc[-1].item()
    
    if latest_rsi > 70:
        signal = "Overbought"
    elif latest_rsi < 30:
        signal = "Oversold"
    else:
        signal = "Neutral"
    
    return f"{ticker} RSI: {latest_rsi:.2f} ({signal})"

def get_news_sentiment(tickers: str) -> str:
    """
    Get news sentiment for one or more tickers.
    Example input: "AAPL" or "AAPL,TSLA,NVDA"
    """
    
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    
    ticker_list = [t.strip().upper() for t in tickers.split(",")]
    
    results = []

    for ticker in ticker_list:
        try:
            url = "https://www.alphavantage.co/query"
            
            params = {
                "function": "NEWS_SENTIMENT",
                "tickers": ticker,
                "apikey": api_key
            }

            response = requests.get(url, params=params)
            data = response.json()

            articles = data.get("feed", [])[:10]

            if not articles:
                results.append(f"{ticker}: No news found")
                continue

            sentiments = [
                float(article["overall_sentiment_score"])
                for article in articles
            ]

            avg_sentiment = sum(sentiments) / len(sentiments)

            if avg_sentiment > 0.2:
                signal = "Bullish"
            elif avg_sentiment < -0.2:
                signal = "Bearish"
            else:
                signal = "Neutral"

            results.append(
                f"{ticker}: {avg_sentiment:.2f} ({signal})"
            )

        except Exception as e:
            results.append(f"{ticker}: Error")

    return "News Sentiment:\n\n" + "\n".join(results)

def get_multi_ema(ticker: str) -> str:
    """
    Get multiple EMAs for a stock
    """
    
    data = yf.download(ticker, period="6mo")
    
    data["EMA_9"] = data["Close"].ewm(span=9, adjust=False).mean()
    data["EMA_20"] = data["Close"].ewm(span=20, adjust=False).mean()
    data["EMA_50"] = data["Close"].ewm(span=50, adjust=False).mean()
    
    price = data["Close"].iloc[-1].item()
    ema9 = data["EMA_9"].iloc[-1].item()
    ema20 = data["EMA_20"].iloc[-1].item()
    ema50 = data["EMA_50"].iloc[-1].item()
    
    if ema9 > ema20 > ema50:
        trend = "Strong Bullish"
    elif ema9 < ema20 < ema50:
        trend = "Strong Bearish"
    else:
        trend = "Mixed"
    
    return (
        f"{ticker}\n"
        f"Price: {price:.2f}\n"
        f"9 EMA: {ema9:.2f}\n"
        f"20 EMA: {ema20:.2f}\n"
        f"50 EMA: {ema50:.2f}\n"
        f"Trend: {trend}"
    )