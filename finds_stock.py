
import requests
import time
import random
from bs4 import BeautifulSoup

BASE_URL = "https://finviz.com/screener.ashx?v=111&f=ta_perf_d15o&ft=3&r="


def generate_headers():
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
    }

def get_all_gainers(max_pages=10):
    all_tickers = {}
    seen_tickers = set()
    page = 1

    while page <= max_pages:
        r_value = (page - 1) * 20 + 1
        url = BASE_URL + str(r_value)
        headers = generate_headers()

        print(f"\n🔄 page {page} | URL: {url}")

        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"❌ network error: {e}")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        ticker_links = soup.find_all("a", class_="tab-link")

        tickers = []
        for link in ticker_links:
            href = link.get("href")
            if href and "quote.ashx?t=" in href:
                ticker = link.text.strip()
                if ticker not in seen_tickers:
                    row = link.find_parent("tr")
                    percent = "N/A"

                    if row:
                        all_tds = row.find_all("td")
                        if len(all_tds) >= 10:
                            percent_span = all_tds[9].find("span")
                            if percent_span:
                                percent = percent_span.text.strip()

                    all_tickers[ticker] = percent
                    seen_tickers.add(ticker)
                    tickers.append(ticker)

        if not tickers:
            print(f"❌Finish in page: {page}, there is no new tickers")
            break

        print(f"✅ Find {len(tickers)} new tickers: {tickers}")
        page += 1
        time.sleep(random.randint(3, 10))

    print(f"\n📊 Total Stocks: {len(all_tickers)}")
    for t, pct in all_tickers.items():
        print(f"{t}: {pct}")


    return all_tickers

if __name__ == "__main__":
    tickers = get_all_gainers() #dict
    print(f"\n📊 Total Stocks: {len(tickers)}")
    for t, pct in tickers.items():
        print(f"{t}: {pct}")
