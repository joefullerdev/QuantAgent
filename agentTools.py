import yfinance as yf

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