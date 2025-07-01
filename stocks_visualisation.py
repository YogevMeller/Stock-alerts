import urllib.parse

def generate_chart_image_urls(tickers):
    """
    For each ticker, generate a direct Finviz chart URL with SMA overlays (50, 100, 200) and custom colors.
    :param tickers: List of ticker symbols
    :return: Dictionary with ticker as key and chart URL as value
    """
    image_map = {}

    # רשימת הממוצעים + צבעים מותאמים (hex RGBA)
    overlays = [
        ("sma", 50, "FF8F33C6"),   # כתום
        ("sma", 100, "0099CCFF"),  # כחול
        ("sma", 200, "32B363FF")   # ירוק
    ]

    for ticker in tickers:
        base_url = f"https://charts2-node.finviz.com/chart.ashx?cs=l&t={ticker.upper()}&tf=d&s=linear&pm=0&am=0&ct=candle_stick"

        overlay_params = ""
        for i, (typ, period, color) in enumerate(overlays):
            overlay_params += f"&o[{i}][ot]={typ}&o[{i}][op]={period}&o[{i}][oc]={color}"

        # קידוד בטוח ל-URL
        encoded_overlay = urllib.parse.quote(overlay_params, safe='=&')

        final_url = base_url + encoded_overlay
        image_map[ticker] = final_url

        print(f"✅ URL ready for {ticker}")

    return image_map



# if __name__ == "__main__":
#     # tickers = ['ADTX', 'NVDA', 'GCTK']
#     # images = generate_chart_image_urls(tickers)
#
#     print("\n📊 Generated Chart URLs:")
#     for ticker, url in images.items():
#         print(f"{ticker}: {url}")
