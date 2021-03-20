import requests
import datetime
from requests.exceptions import HTTPError

def delete_mark(str, mark):
    #Удаляет из строки ненужный символ
    new_str = ""
    for x in str:
        if x != mark:
            new_str +=x
    return  new_str

def get_get (page):
    #Получает url и извлекает из него объект json
    try:
        result = requests.get(page)
    except HTTPError as http_err:
        print(f"Ошибка HTTP: {http_err}!")
    except Exception as err:
        print(f"Что-пошло не так: {err}, при запросе к странице {page}!")
    else:
        print(f"Запрос к странице: {page} \n Успешен!")
        return result.json()

with requests.Session() as se:
    se.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en"
    }

page_oi = "https://www.cmegroup.com/CmeWS/mvc/Volume/Details/F/323/{0}/P?tradeDate={0}&pageSize=500&_=1616223940817"
page_status_oi = "https://www.cmegroup.com/CmeWS/mvc/Volume/TradeDates?exchange=CBOT" #финальные данные или предварительные, берем данные с этой страницы

status_dict = get_get(page_status_oi)
file_name = "chicago_srw_wheat_cbot.txt"
file = file = open(file_name, 'w')
current_date = datetime.datetime.now().date() - datetime.timedelta(40)
today_date = datetime.datetime.now().date()

while current_date != today_date:
    string_date = delete_mark(str(current_date), '-')
    oi_dict = get_get(page_oi.format(string_date))

    totals_oi = oi_dict['totals']['atClose']
    if totals_oi == '0':
        print(f"Дата {current_date}, не записывается в файл(торги не велись)\n")
        current_date = current_date + datetime.timedelta(1)
        continue

    status_flag = "FINAL"
    for trade_day in status_dict:
        if trade_day['tradeDate'] == oi_dict['tradeDate'] and trade_day['reportType'] == 'PRELIMINARY':
            status_flag = "PRELIMINARY"
            break

    date_with_point = string_date[0] + string_date[1] + string_date[2] + string_date[3] + '.' + string_date[4] + string_date[5] + '.' + string_date[6] + string_date[7]
    totals_oi = delete_mark(totals_oi, ',')
    file.write(f"{date_with_point}\t{status_flag}\tTOTAL\t{totals_oi}\t")

    for month in oi_dict['monthData']:
        month_name = month['month']
        month_oi = month['atClose']
        month_oi = delete_mark(month_oi, ',')
        file.write(f"{month_name}\t{month_oi}\t")

    file.write('\n')
    print(f"Данные по дате {current_date} успешно добавлены!\n")
    current_date = current_date + datetime.timedelta(1)

print(f"Файл {file_name} успешно обработан!\n")

