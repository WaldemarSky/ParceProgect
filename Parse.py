import requests
import datetime

def delete_mark(str, mark):
    new_str = ""
    for x in str:
        if x != mark:
            new_str +=x
    return  new_str

def get_get (page_oi, page_status):
    start_date = datetime.datetime.now().date() -


with requests.Session() as se:
    se.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en"
    }
site_date = "https://www.cmegroup.com/CmeWS/mvc/Volume/TradeDates?exchange=CBOT"
select_date = requests.get(site_date).json()
start_date = datetime.date(2021, 1, 1)
current_date = datetime.datetime.now().date()
file_name = input("Введите имя файла")
file = open(file_name, 'w')
while start_date != current_date:
    string_date = delete_mark(str(start_date), '-')
    site = "https://www.cmegroup.com/CmeWS/mvc/Volume/Details/F/323/{0}/P?tradeDate={0}&pageSize=500&_=1616223940817".format(string_date)
    html = requests.get(site).json()
    date = html['tradeDate']
    date_with_point = date[0] + date[1] + date[2] + date[3] + '.' + date[4] + date[5] + '.' + date[6] + date[7]

    date_flag = "FINAL"
    for trade_day in select_date:
        if trade_day['tradeDate'] == html['tradeDate'] and trade_day['reportType'] == 'PRELIMINARY':
            date_flag = "PRELIMINARY"
            break


    totals_oi = html['totals']['atClose']
    print(totals_oi)
    totals_oi = delete_mark(totals_oi, ',')
    if totals_oi == '0':
        start_date = start_date + datetime.timedelta(1)
        print("ogromni hui")
        continue



    file.write(date_with_point + '\t')
    file.write(date_flag + '\t' + "TOTAL" + '\t')
    file.write(totals_oi + '\t')

    for month in html['monthData']:
        month_name = month['month']
        month_oi = month['atClose']
        month_oi = delete_mark(month_oi, ',')
        file.write(month_name + '\t' + month_oi + '\t')

    file.write('\n')
    start_date = start_date + datetime.timedelta(1)

print("Done")

