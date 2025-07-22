# Project Auriga
  

### CI/CD TODOs
  
 - Deploy service
 - Check the scp




ML Notes  

| Model    | Purpose                                            |
| -------- | -------------------------------------------------- |
| 1D CNN   | Detect short-term patterns in price/volume         |
| LSTM/GRU | Capture short-term sequences (last 5–30 seconds)   |
| MLP      | Combine engineered features into a fast classifier |



✅ Smart Features to Train On:
📈 Price-based indicators:

    RSI, MACD, Bollinger Bands, EMAs

📊 Trend recognition:

    Use convolution layers on candlestick data

🌪️ Volatility modeling:

    Rolling standard deviation

    ATR

    Volume shocks

✅ Model Types:

    LSTM (for sequential price prediction)

    GRU + attention (faster than LSTM with same power)

    Transformers (e.g., Informer, Time2Vec)

    Reinforcement Learning (for strategy learning directly)

✅ Data Sources:

    Use Binance WebSocket + REST:

    wss://stream.binance.com:9443/ws/btcusdt@kline_1s

    Train on OHLCV data from the last 3–12 months using ccxt or python-binance

📊 3. Logging & Backtesting

🎯 Goal: Know what’s working, and why.
✅ Logging Tips:

    Log every trade: timestamp, price, side, profit/loss

    Store in CSV or SQLite format:

timestamp,pair,side,price,amount,pnl
2025-07-20T13:00:01Z,BTC/USDT,BUY,64750.0,0.001,-0.23

Use a rotating logger for both live console + file logs:

    from logging.handlers import RotatingFileHandler

✅ Backtesting Engine:

To estimate profitability before deploying:

    Use Backtrader

    Or build a custom vectorized backtester using pandas:

        Simulate entries/exits using signal thresholds

        Track cash balance and portfolio value

        Compare strategies side-by-side

✅ Ready-to-Start Next Steps?

Let me know which you'd like next:
Menu:

    🚀 [A] Async live Binance trading core

    🧠 [B] AI model training on Binance OHLCV

    📊 [C] Logging system with CSV + backtester template

Just pick one (or all), and I’ll generate the code for you.