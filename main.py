import time
from datetime import datetime, timedelta
from finds_stock import get_all_gainers
from email_send import send_email
from stocks_visualisation import generate_chart_image_urls
from volume import get_volumes_with_dates_for_ticker_dict

def is_market_monitoring_time():
    now = datetime.now()
    hour = now.hour
    minute = now.minute

    # שעות ארה"ב – לפי שעון ישראל:
    # Pre-market בישראל: 11:00 עד 16:30 (בהתאם לשעון קיץ)
    # Regular market: 16:30 עד 23:00
    # After-hours: 23:00 עד 02:00
    return (
            (11 <= hour <= 23) or
            (hour < 2)
    )


if __name__ == "__main__":
    while True:
        now = datetime.now()
        next_run = now + timedelta(minutes=15)

        if is_market_monitoring_time():
            print(f"🔁 Running scan at {now.strftime('%Y-%m-%d %H:%M:%S')}")
            tickers_dic = get_all_gainers()
            images_dic = generate_chart_image_urls(tickers_dic.keys())
            yearly_volume_dic = get_volumes_with_dates_for_ticker_dict(tickers_dic)
            send_email(tickers_dic, images_dic, yearly_volume_dic)
        else:
            print(f"⏳ Not in monitoring hours, waiting... ({now.strftime('%H:%M')})")

        print(f"⏰ Next run at: {next_run.strftime('%H:%M:%S')}")
        time.sleep(15 * 60)
