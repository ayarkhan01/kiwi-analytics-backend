import yfinance as yf
import logging

TICKERS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "META",
    "TSLA", "NVDA", "JPM", "WMT", "JNJ", "DIS", "PFE"
]

def format_market_cap(market_cap):
    if market_cap >= 1_000_000_000_000:
        return f"{round(market_cap / 1_000_000_000_000, 2)}T"
    elif market_cap >= 1_000_000_000:
        return f"{round(market_cap / 1_000_000_000, 2)}B"
    elif market_cap >= 1_000_000:
        return f"{round(market_cap / 1_000_000, 2)}M"
    return str(market_cap)

def fetch_market_data():
    market_data = []
    for ticker in TICKERS:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            price = info.get("regularMarketPrice", 0)
            previous_close = info.get("regularMarketPreviousClose", price)
            change = price - previous_close

            market_cap = info.get("marketCap", 0)
            formatted_cap = format_market_cap(market_cap)

            market_data.append({
                "ticker": ticker,
                "name": info.get("shortName", "N/A"),
                "price": round(price, 2),
                "change": round(change, 2),
                "marketCap": formatted_cap,
                "sector": info.get("sector", "N/A")
            })
        except Exception as e:
            logging.error(f"Error fetching data for {ticker}: {str(e)}")
            market_data.append({
                "ticker": ticker,
                "name": "Error",
                "price": 0,
                "change": 0,
                "marketCap": "N/A",
                "sector": "N/A",
                "error": str(e)
            })
    return market_data