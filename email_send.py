import smtplib
from email.message import EmailMessage
from datetime import datetime

def send_email(tickers, image_map, volume_dic):
    EMAIL_ADDRESS = "y622000@gmail.com"
    EMAIL_PASSWORD = "frur qrjn bhdb uilv"
    TO_EMAIL_ADDRESS = ["yogevmeller1@gmail.com"] #"Amitczitron40@gmail.com"

    today_str = datetime.today().strftime('%Y-%m-%d %H:%M')
    msg = EmailMessage()
    msg['Subject'] = f'Stocks Gained Over 15% – {today_str}'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = ", ".join(TO_EMAIL_ADDRESS)

    html = f"<h2>📈 Stocks that gained more than 15% on {today_str}:</h2><br>"

    for ticker, percent in tickers.items():
        html += f"<h3>{ticker.upper()} – {percent}</h3>"

        if image_map.get(ticker):
            html += f'<img src="{image_map[ticker]}" width="725" height="273"><br>'
        else:
            html += "<p><i>Chart not available</i></p><br>"

        all_data = volume_dic.get(ticker.upper()) or volume_dic.get(ticker.lower()) or []

        if all_data and len(all_data) >= 5:
            # טבלת 5 ימים אחרונים (כולל היום), כאשר היום ראשון
            recent_data = all_data[:5]
            html += "<table border='1' cellpadding='5' cellspacing='0' style='border-collapse: collapse; margin-top: 10px;'>"
            html += "<tr><th>Date</th>" + "".join([f"<td>{date}</td>" for date, _ in recent_data]) + "</tr>"
            html += "<tr><th>Volume</th>" + "".join([f"<td>{vol:,}</td>" for _, vol in recent_data]) + "</tr>"
            html += "</table><br>"

            today_volume = recent_data[0][1]

            # השוואה מול כל שאר השנה (למעט היום עצמו)
            rest_of_year = [item for item in all_data[1:] if item[1] > 0]

            if rest_of_year:
                max_date, max_vol = max(rest_of_year, key=lambda x: x[1])
                if max_vol > 0 and today_volume >= 8 * max_vol:
                    factor = round(today_volume / max_vol, 1)
                    percent_increase = round((today_volume / max_vol - 1) * 100)
                    html += f"<p style='color:red; font-weight:bold;'>🚨 Today's volume is <b>{factor}×</b> higher than the highest day in the past year ({max_date}, {max_vol:,}) – <b>{percent_increase}%</b> higher.</p>"

        else:
            html += "<p><i>No volume data available, The max of the </i></p>"

        html += "<br><hr><br>"

    msg.set_content("Please view this email in HTML format to see the charts and data.")
    msg.add_alternative(f"<html><body>{html}</body></html>", subtype='html')

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("✅ Email sent successfully.")
    except Exception as e:
        print(f"❌ Error sending email: {e}")


# if __name__ == "__main__":
#     tickers = {"qqq": "23%", "crcl%": "25%"}
#     image_map = {"qqq": "123", "crcl": "12345"}
#     yearly_volume_dic = {'qqq': [('2025-06-20', 108688000), ('2025-06-23', 190716800)],
#                   'crcl': [('2025-06-20', 42237200), ('2025-06-23', 176087900)]}
#     send_email(tickers, image_map, yearly_volume_dic)
