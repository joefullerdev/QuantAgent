from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from langchain.agents import create_agent
from langchain_ollama import ChatOllama

import yfinance as yf

import sys
import os
from dotenv import load_dotenv, dotenv_values

from agentTools import * #Loads all functions from agentTools.py

load_dotenv() #Loads environment variables (API Keys)

model = ChatOllama(
    model="qwen2.5:7b",
    temperature=0
) 

#Agent creation - loads LLM, tools and define a system prompt
agent = create_agent( 
    model=model,
    tools=[get_stock_price, get_market_cap, get_volatility, get_RSI, get_news_sentiment, get_multi_ema],
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