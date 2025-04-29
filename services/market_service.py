import yfinance as yf

TICKERS = ["AAPL", "GOOGL", "AMZN", "MSFT", "TSLA", "META", "NVDA", "JPM", "V", "JNJ"]

def fetch_market_data():
    market_data = []
    for ticker in TICKERS:
        stock = yf.Ticker(ticker)
        info = stock.info
        price = info.get("regularMarketPrice", 0)
        previous_close = info.get("regularMarketPreviousClose", price)
        change = price - previous_close
        change_percent = (change / previous_close * 100) if previous_close else 0

        market_data.append({
            "ticker": ticker,
            "price": round(price, 2),
            "change": round(change, 2),
            "changePercent": round(change_percent, 2),
        })
    return market_data
