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

agent = create_agent(
    model=model,
    tools=[get_stock_price, get_market_cap, get_volatility],
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