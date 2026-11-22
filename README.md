# RSI Alert Bot

A Python bot that watches a list of stocks and sends a Telegram alert when RSI goes oversold (below 30) or overbought (above 70).

## Features
- Fetches daily price data with yfinance
- Calculates 14-period RSI
- Sends Telegram alerts, without repeating the same alert
- Easy to change the watchlist and RSI levels

## Setup
1. Install Python 3
2. Run: python -m pip install yfinance pandas requests
3. Add your Telegram bot token and chat id in the file
4. Run: python rsi_alert_bot.py

## Note
This is an educational tool. It does not give investment advice.
