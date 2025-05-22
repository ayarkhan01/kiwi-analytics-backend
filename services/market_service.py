import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
import random
import os
from datetime import datetime

CACHE_FILE = 'popular_stocks_data.csv'
TIMESTAMP_FILE = 'market_data_timestamp.txt'

def get_finviz_stock_info(ticker):
    url = f"https://finviz.com/quote.ashx?t={ticker}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        name_element = soup.find("h2", class_="quote-header_ticker-wrapper_company")
        name = name_element.text.strip() if name_element else "N/A"

        sector = "N/A"
        industry = "N/A"
        quote_links_div = soup.find("div", class_="quote-links")
        if quote_links_div:
            links = quote_links_div.find_all("a")
            for link in links:
                href = link.get('href', '')
                if 'v=111&f=sec_' in href:
                    sector = link.text.strip()
                elif 'v=111&f=ind_' in href:
                    industry = link.text.strip()

        data = {}
        snapshot_table = soup.find("table", class_="snapshot-table2")
        if snapshot_table:
            rows = snapshot_table.find_all("tr")
            for row in rows:
                cells = row.find_all("td")
                for i in range(0, len(cells), 2):
                    if i + 1 < len(cells):
                        data[cells[i].text.strip()] = cells[i + 1].text.strip()

        price = 0.0
        change = 0.0
        market_cap = data.get('Market Cap', "N/A")

        price_element = soup.find("strong", class_="quote-price_wrapper_price")
        if price_element:
            try:
                price = float(price_element.text.strip().replace(",", ""))
            except:
                pass

        if 'Change' in data:
            try:
                change_str = data['Change'].replace('%', '').replace(',', '').strip()
                change = float(change_str)
            except:
                change = 0.0


        return {
            "ticker": ticker,
            "name": name,
            "price": round(price, 2),
            "change": round(change, 2),
            "marketCap": market_cap,
            "sector": sector,
            "industry": industry
        }

    except Exception as e:
        print(f"Error fetching {ticker}: {e}")
        return {
            "ticker": ticker,
            "name": "Error",
            "price": 0.0,
            "change": 0.0,
            "marketCap": "N/A",
            "sector": "N/A",
            "industry": "N/A"
        }

def fetch_and_cache_market_data():
    today = datetime.today().strftime('%Y-%m-%d')

    # Only run if not already run today
    if os.path.exists(TIMESTAMP_FILE):
        with open(TIMESTAMP_FILE, 'r') as f:
            last_run = f.read().strip()
            if last_run == today:
                print("Market data already fetched today.")
                return

    print("Fetching fresh market data...")

    popular_tickers = [
        "AAPL", "MSFT", "AMZN", "GOOGL", "META",
        "TSLA", "JPM", "V", "DIS", "NFLX",
        "AMD", "KO", "PFE", "INTC", "NKE"
    ]

    all_data = []
    for ticker in popular_tickers:
        info = get_finviz_stock_info(ticker)
        all_data.append(info)
        time.sleep(1.5 + random.random())

    df = pd.DataFrame(all_data)
    df.to_csv(CACHE_FILE, index=False)

    with open(TIMESTAMP_FILE, 'w') as f:
        f.write(today)

    print("Market data saved.")

