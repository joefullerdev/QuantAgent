<h1>Telegram Quant AI Agent 🤖</h1>

<h3>Features</h3>

- Chat function within Telegram 💬
- Provides near real-time stock prices 📈
- Calculates a series of technical indicators: Relative Strength Index, Exponential Moving Average ❗
- Analyses news sentiment 📰

<h2>Setup: ⚙️</h2>
<ol>
  <li>Clone the repo into your desired workspace</li>
  <li>Set up Telegram</li>
  <ol>
    <li>Download Telegram if you haven't already and search <strong>BotFather</strong>, a chat should then appear</li>
    <li>Type: <strong>/start</strong> (if it hasn't done it already)</li>
    <li>Then Type: <strong>/newbot</strong></li>
    <li>The chat will then prompt you for a Bot name and a username</li>
    <li>You will then recieve a Bot token, this is your API Key, create a .env file and add it.</li>
    <code>TELEGRAM_KEY=your_bot_key_here</code> 
  </ol>
  <li>Get your free <strong>Alpha Vantage API Key</strong> from: https://www.alphavantage.co</li>
  - Add this to your .env as well:
  <code>ALPHA_VANTAGE_API_KEY=your_api_key_here</code>
  <li>Install <strong>qwen2.5:7b</strong> locally through Ollama: </li>
  <code>ollama pull qwen2.5:7b</code>
  <li>Navigate to <strong>quantAgent.py</strong> and run, you should see <code>Bot running...</code> in the terminal</li>
  <li>Test by opening Telegram and asking for the price of a stock </li>
  
</ol>



