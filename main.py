from finds_stock import get_all_gainers
from email_send import send_email
from stocks_visualisation import generate_chart_image_urls
from volume import get_volumes_with_dates_for_ticker_dict

if __name__ == "__main__":
    tickers_dic = get_all_gainers()
    images_dic = generate_chart_image_urls(tickers_dic.keys())
    yearly_volume_dic = get_volumes_with_dates_for_ticker_dict(tickers_dic)
    send_email(tickers_dic, images_dic, yearly_volume_dic)  # tickers - {ticker:%} , images_dic -{ticker:url}
