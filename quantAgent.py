from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes


from langchain.agents import create_agent
from langchain_ollama import ChatOllama

import yfinance as yf

import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()

model = ChatOllama(
    model="qwen2.5:7b",
    temperature=0
)

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



agent = create_agent(
    model=model,
    tools=[get_stock_price, get_market_cap, get_volatility, get_RSI],
    system_prompt="""
You are a quantitative finance assistant.

You must:
- Use tools for financial data
- Perform multi-step reasoning
- Compare stocks when appropriate
- Provide concise quant insights
"""
)

# Telegram Handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    user_message = update.message.text
    
    response = agent.invoke(
        {
            "messages": [
                {"role": "user", "content": user_message}
            ]
        }
    )
    
    reply = response["messages"][-1].content
    
    await update.message.reply_text(reply)


# Main
app = ApplicationBuilder().token(os.getenv("TELEGRAM_KEY")).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot running...")

app.run_polling()