import smtplib
from email.message import EmailMessage
from datetime import datetime, timedelta
import json
import os

SENT_LOG_FILE = "sent_log.json"

def load_sent_log():
    if os.path.exists(SENT_LOG_FILE):
        with open(SENT_LOG_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_sent_log(log):
    with open(SENT_LOG_FILE, 'w') as f:
        json.dump(log, f, indent=2)

def send_email(tickers, image_map, volume_dic):
    EMAIL_ADDRESS = "y622000@gmail.com"
    EMAIL_PASSWORD = "frur qrjn bhdb uilv"
    TO_EMAIL_ADDRESS = ["yogevmeller1@gmail.com","Amitczitron40@gmail.com"]

    sent_log = load_sent_log()
    now_str = datetime.today().strftime('%Y-%m-%d %H:%M')
    now = datetime.now()
    tickers_to_send = {}

    for ticker, percent in tickers.items():
        all_data = volume_dic.get(ticker.upper()) or volume_dic.get(ticker.lower()) or []
        if len(all_data) < 5:
            continue

        today_volume = all_data[0][1]
        rest_of_year = [item for item in all_data[1:] if item[1] > 0]
        if not rest_of_year:
            continue

        max_date, max_vol = max(rest_of_year, key=lambda x: x[1])
        avg_vol = sum([v for _, v in rest_of_year]) / len(rest_of_year)

        notes = ""
        passed = False

        # תנאי מול מקסימום
        if today_volume >= 8 * max_vol:
            factor = round(today_volume / max_vol, 1)
            percent_increase = round((today_volume / max_vol - 1) * 100)
            notes += (
                f"<p style='color:red; font-weight:bold;'>"
                f"🚨 Today's volume: <b>{today_volume:,}</b><br>"
                f"is <b>{factor}×</b> higher than the highest volume in the past year: "
                f"<b>{max_vol:,}</b> on <b>{max_date}</b><br>"
                f"(an increase of <b>{percent_increase}%</b>).</p>"
            )
            passed = True

        # תנאי מול ממוצע
        if today_volume >= 8 * avg_vol:
            factor = round(today_volume / avg_vol, 1)
            percent_increase = round((today_volume / avg_vol - 1) * 100)
            notes += (
                f"<p style='color:blue; font-weight:bold;'>"
                f"📊 Today's volume: <b>{today_volume:,}</b><br>"
                f"is <b>{factor}×</b> higher than the average daily volume over the past year: "
                f"<b>{int(avg_vol):,}</b><br>"
                f"(an increase of <b>{percent_increase}%</b> over average).</p>"
            )
            passed = True

        if passed:
            last_sent = sent_log.get(ticker)
            if last_sent:
                last_sent_time = datetime.strptime(last_sent, '%Y-%m-%d %H:%M')
                if now - last_sent_time < timedelta(hours=24):
                    continue  # נשלח לאחרונה
            tickers_to_send[ticker] = {
                "percent": percent,
                "notes": notes,
                "volume_table": all_data[:5]
            }

    if not tickers_to_send:
        print("📭 No tickers passed the filter – no email sent.")
        return

    # יצירת מייל
    msg = EmailMessage()
    msg['Subject'] = f'STOCKS ALERT – {now_str}'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = ", ".join(TO_EMAIL_ADDRESS)

    html = f"<h2>📈 Stocks that passed volume filters on {now_str}:</h2><br>"

    for ticker, info in tickers_to_send.items():
        html += f"<h3>{ticker.upper()} – {info['percent']}</h3>"
        if image_map.get(ticker):
            html += f'<img src="{image_map[ticker]}" width="725" height="273"><br>'
        html += info['notes']

        volume_data = info["volume_table"]
        html += "<table border='1' cellpadding='5' cellspacing='0' style='border-collapse: collapse; margin-top: 10px;'>"
        html += "<tr><th>Date</th>" + "".join([f"<td>{d}</td>" for d, _ in volume_data]) + "</tr>"
        html += "<tr><th>Volume</th>" + "".join([f"<td>{v:,}</td>" for _, v in volume_data]) + "</tr>"
        html += "</table><br><hr><br>"

    msg.set_content("Please view this email in HTML format to see the charts and data.")
    msg.add_alternative(f"<html><body>{html}</body></html>", subtype='html')

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print(f"✅ Email sent for {len(tickers_to_send)} tickers.")
        for ticker in tickers_to_send:
            sent_log[ticker] = now.strftime('%Y-%m-%d %H:%M')
        save_sent_log(sent_log)

    except Exception as e:
        print(f"❌ Error sending email: {e}")

# if __name__ == "__main__":
#     tickers = {"qqq": "23%", "crcl%": "25%"}
#     image_map = {"qqq": "123", "crcl": "12345"}
#     yearly_volume_dic = {'qqq': [('2025-06-20', 108688000), ('2025-06-23', 190716800)],
#                   'crcl': [('2025-06-20', 42237200), ('2025-06-23', 176087900)]}
#     send_email(tickers, image_map, yearly_volume_dic)


