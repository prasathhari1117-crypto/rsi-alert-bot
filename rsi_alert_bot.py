import time
import requests
import pandas as pd
import yfinance as yf

TELEGRAM_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"
WATCHLIST = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "AAPL"]
RSI_PERIOD = 14
OVERSOLD = 30
OVERBOUGHT = 70
CHECK_EVERY_MINUTES = 30


def calculate_rsi(prices, period=14):
    delta = prices.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def get_latest_rsi(symbol):
    data = yf.download(symbol, period="6mo", interval="1d",
                       progress=False, auto_adjust=True)
    if data.empty:
        return None, None
    close = data["Close"].squeeze()
    rsi = calculate_rsi(close, RSI_PERIOD)
    return float(rsi.iloc[-1]), float(close.iloc[-1])


def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": message}, timeout=10)
    except requests.RequestException as e:
        print("Telegram error:", e)


def check_watchlist(already_alerted):
    for symbol in WATCHLIST:
        try:
            rsi, price = get_latest_rsi(symbol)
        except Exception as e:
            print(f"{symbol}: error -> {e}")
            continue
        if rsi is None:
            print(f"{symbol}: data illa")
            continue
        print(f"{symbol}: price={price:.2f}  RSI={rsi:.1f}")
        if rsi < OVERSOLD:
            status = "OVERSOLD"
        elif rsi > OVERBOUGHT:
            status = "OVERBOUGHT"
        else:
            already_alerted.discard(symbol)
            continue
        if symbol not in already_alerted:
            send_telegram(f"{status}: {symbol}\nPrice: {price:.2f}\nRSI({RSI_PERIOD}): {rsi:.1f}")
            already_alerted.add(symbol)


if __name__ == "__main__":
    alerted = set()
    print("RSI bot started...")
    while True:
        check_watchlist(alerted)
        time.sleep(CHECK_EVERY_MINUTES * 60)