import yfinance as yf

# def get_volumes_with_dates_for_ticker_dict(ticker_dict):
#     """
#  get a dic and return dic too
#     """
#     results = {}
#
#     for ticker in ticker_dict:
#         try:
#             stock = yf.Ticker(ticker)
#             df = stock.history(period='10d', interval='1d')
#             df = df.dropna(subset=['Volume'])
#             volumes = df['Volume'].astype(int)
#             dates = df.index.strftime('%Y-%m-%d')
#             last_6 = list(zip(dates[-6:], volumes[-6:]))[::-1] #six last days
#
#             results[ticker] = last_6
#         except Exception as e:
#             print(f"ticker error {ticker}: {e}")
#             results[ticker] = []
#
#     return results

def get_volumes_with_dates_for_ticker_dict(ticker_dict):
    """
    מקבל מילון {ticker: percent_gain} ומחזיר מילון {ticker: [(date, volume)]} עבור כל השנה האחרונה
    """
    results = {}

    for ticker in ticker_dict:
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(period='1y', interval='1d')  # שנה אחורה, יומי
            df = df.dropna(subset=['Volume'])
            volumes = df['Volume'].astype(int)
            dates = df.index.strftime('%Y-%m-%d')

            yearly_data = list(zip(dates, volumes))[::-1]  # הופך כך שהתאריך של היום יהיה ראשון

            results[ticker] = yearly_data
        except Exception as e:
            print(f"ticker error {ticker}: {e}")
            results[ticker] = []

    return results



if __name__ == "__main__":
    ticker_dict = {
    'TSLA': 16,
    'HIMS': 17.3
}
    print(get_volumes_with_dates_for_ticker_dict(ticker_dict))