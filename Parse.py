import requests
import datetime
from requests.exceptions import HTTPError
import os



pages_oi = {
    'chicago_srw_wheat_cbot': {
        'page_oi': 'https://www.cmegroup.com/CmeWS/mvc/Volume/Details/F/323/{0}/{1}?tradeDate={0}',
        'page_status': 'https://www.cmegroup.com/CmeWS/mvc/Volume/TradeDates?exchange=CBOT'
    },
    'kc_hrw_wheat_cbot': {
        'page_oi': 'https://www.cmegroup.com/CmeWS/mvc/Volume/Details/F/348/{0}/{1}?tradeDate={0}',
        'page_status': 'https://www.cmegroup.com/CmeWS/mvc/Volume/TradeDates?exchange=CBOT'
    },
    'corn_cbot': {
        'page_oi': 'https://www.cmegroup.com/CmeWS/mvc/Volume/Details/F/300/{0}/{1}?tradeDate={0}',
        'page_status': 'https://www.cmegroup.com/CmeWS/mvc/Volume/TradeDates?exchange=CBOT'
    },
    'soybean_cbot': {
        'page_oi': 'https://www.cmegroup.com/CmeWS/mvc/Volume/Details/F/320/{0}/{1}?tradeDate={0}',
        'page_status': 'https://www.cmegroup.com/CmeWS/mvc/Volume/TradeDates?exchange=CBOT'
    },
    'soybean_meal_cbot': {
        'page_oi': 'https://www.cmegroup.com/CmeWS/mvc/Volume/Details/F/310/{0}/{1}?tradeDate={0}',
        'page_status': 'https://www.cmegroup.com/CmeWS/mvc/Volume/TradeDates?exchange=CBOT'
    },
    'soybean_oil_cbot': {
        'page_oi': 'https://www.cmegroup.com/CmeWS/mvc/Volume/Details/F/312/{0}/{1}?tradeDate={0}',
        'page_status': 'https://www.cmegroup.com/CmeWS/mvc/Volume/TradeDates?exchange=CBOT'
    },
    'rough_rice': {
        'page_oi': 'https://www.cmegroup.com/CmeWS/mvc/Volume/Details/F/336/{0}/{1}?tradeDate={0}',
        'page_status': 'https://www.cmegroup.com/CmeWS/mvc/Volume/TradeDates?exchange=CBOT'
    },
    'cash-settled_butter_cme': {
        'page_oi': 'https://www.cmegroup.com/CmeWS/mvc/Volume/Details/F/26/{0}/{1}?tradeDate={0}',
        'page_status': 'https://www.cmegroup.com/CmeWS/mvc/Volume/TradeDates?exchange=CME'
    },
    'cash-settled_cheese_cme': {
        'page_oi': 'https://www.cmegroup.com/CmeWS/mvc/Volume/Details/F/5201/{0}/{1}?tradeDate={0}',
        'page_status': 'https://www.cmegroup.com/CmeWS/mvc/Volume/TradeDates?exchange=CME'
    },
    'class_iii_milk_cme': {
        'page_oi': 'https://www.cmegroup.com/CmeWS/mvc/Volume/Details/F/27/{0}/{1}?tradeDate={0}',
        'page_status': 'https://www.cmegroup.com/CmeWS/mvc/Volume/TradeDates?exchange=CME'
    },
    'feeder_cattle_cme': {
        'page_oi': 'https://www.cmegroup.com/CmeWS/mvc/Volume/Details/F/34/{0}/{1}?tradeDate={0}',
        'page_status': 'https://www.cmegroup.com/CmeWS/mvc/Volume/TradeDates?exchange=CME'
    },
    'lean_hog_cme': {
        'page_oi': 'https://www.cmegroup.com/CmeWS/mvc/Volume/Details/F/19/{0}/{1}?tradeDate={0}',
        'page_status': 'https://www.cmegroup.com/CmeWS/mvc/Volume/TradeDates?exchange=CME'
    },
    'live_cattle_cme': {
        'page_oi': 'https://www.cmegroup.com/CmeWS/mvc/Volume/Details/F/22/{0}/{1}?tradeDate={0}',
        'page_status': 'https://www.cmegroup.com/CmeWS/mvc/Volume/TradeDates?exchange=CME'
    },
    'copper_comex': {
        'page_oi': 'https://www.cmegroup.com/CmeWS/mvc/Volume/Details/F/438/{0}/{1}?tradeDate={0}',
        'page_status': 'https://www.cmegroup.com/CmeWS/mvc/Volume/TradeDates?exchange=COMEX'
    },
    'gold_comex': {
        'page_oi': 'https://www.cmegroup.com/CmeWS/mvc/Volume/Details/F/437/{0}/{1}?tradeDate={0}',
        'page_status': 'https://www.cmegroup.com/CmeWS/mvc/Volume/TradeDates?exchange=COMEX'
    },
    'silver_comex': {
        'page_oi': 'https://www.cmegroup.com/CmeWS/mvc/Volume/Details/F/458/{0}/{1}?tradeDate={0}',
        'page_status': 'https://www.cmegroup.com/CmeWS/mvc/Volume/TradeDates?exchange=COMEX'
    },
    'platinum_nymex': {
        'page_oi': 'https://www.cmegroup.com/CmeWS/mvc/Volume/Details/F/446/{0}/{1}?tradeDate={0}',
        'page_status': 'https://www.cmegroup.com/CmeWS/mvc/Volume/TradeDates?exchange=NYMEX'
    },
    'palladium_nymex': {
        'page_oi': 'https://www.cmegroup.com/CmeWS/mvc/Volume/Details/F/445/{0}/{1}?tradeDate={0}',
        'page_status': 'https://www.cmegroup.com/CmeWS/mvc/Volume/TradeDates?exchange=NYMEX'
    },
    'aluminum_mw_us_transaction_premium_platts(25mt)': {
        'page_oi': 'https://www.cmegroup.com/CmeWS/mvc/Volume/Details/F/6746/{0}/{1}?tradeDate={0}',
        'page_status': 'https://www.cmegroup.com/CmeWS/mvc/Volume/TradeDates?exchange=COMEX'
    },
    'us_midwest_domestic_hot-rolled_coil_steel_(cru)_index': {
        'page_oi': 'https://www.cmegroup.com/CmeWS/mvc/Volume/Details/F/2508/{0}/{1}?tradeDate={0}',
        'page_status': 'https://www.cmegroup.com/CmeWS/mvc/Volume/TradeDates?exchange=COMEX'
    },
    'wti_crude_oil': {
        'page_oi': 'https://www.cmegroup.com/CmeWS/mvc/Volume/Details/F/425/{0}/{1}?tradeDate={0}',
        'page_status': 'https://www.cmegroup.com/CmeWS/mvc/Volume/TradeDates?exchange=NYMEX'
    },
    'henry_hub_natural_gas': {
        'page_oi': 'https://www.cmegroup.com/CmeWS/mvc/Volume/Details/F/444/{0}/{1}?tradeDate={0}',
        'page_status': 'https://www.cmegroup.com/CmeWS/mvc/Volume/TradeDates?exchange=NYMEX'
    },
    'e-mini_s&p500': {
        'page_oi': 'https://www.cmegroup.com/CmeWS/mvc/Volume/Details/F/133/{0}/{1}?tradeDate={0}',
        'page_status': 'https://www.cmegroup.com/CmeWS/mvc/Volume/TradeDates?exchange=CME'
    },
    'e-mini_russell_2000_index': {
        'page_oi': 'https://www.cmegroup.com/CmeWS/mvc/Volume/Details/F/8314/{0}/{1}?tradeDate={0}',
        'page_status': 'https://www.cmegroup.com/CmeWS/mvc/Volume/TradeDates?exchange=CME'
    },
    'e-mini_nasdaq-100': {
        'page_oi': 'https://www.cmegroup.com/CmeWS/mvc/Volume/Details/F/146/{0}/{1}?tradeDate={0}',
        'page_status': 'https://www.cmegroup.com/CmeWS/mvc/Volume/TradeDates?exchange=CME'
    },
    'e-mini_s&p_midcap_400': {
        'page_oi': 'https://www.cmegroup.com/CmeWS/mvc/Volume/Details/F/166/{0}/{1}?tradeDate={0}',
        'page_status': 'https://www.cmegroup.com/CmeWS/mvc/Volume/TradeDates?exchange=CME'
    },
    's&p500': {
        'page_oi': 'https://www.cmegroup.com/CmeWS/mvc/Volume/Details/F/132/{0}/{1}?tradeDate={0}',
        'page_status': 'https://www.cmegroup.com/CmeWS/mvc/Volume/TradeDates?exchange=CME'
    },
    '10_Year_t-note': {
        'page_oi': 'https://www.cmegroup.com/CmeWS/mvc/Volume/Details/F/316/{0}/{1}?tradeDate={0}',
        'page_status': 'https://www.cmegroup.com/CmeWS/mvc/Volume/TradeDates?exchange=CBOT'
    },
    '5_Year_t-note': {
        'page_oi': 'https://www.cmegroup.com/CmeWS/mvc/Volume/Details/F/329/{0}/{1}?tradeDate={0}',
        'page_status': 'https://www.cmegroup.com/CmeWS/mvc/Volume/TradeDates?exchange=CBOT'
    },
    '2_Year_t-note': {
        'page_oi': 'https://www.cmegroup.com/CmeWS/mvc/Volume/Details/F/303/{0}/{1}?tradeDate={0}',
        'page_status': 'https://www.cmegroup.com/CmeWS/mvc/Volume/TradeDates?exchange=CBOT'
    },
    '30_day_federal_funds': {
        'page_oi': 'https://www.cmegroup.com/CmeWS/mvc/Volume/Details/F/305/{0}/{1}?tradeDate={0}',
        'page_status': 'https://www.cmegroup.com/CmeWS/mvc/Volume/TradeDates?exchange=CBOT'
    },
    'us_treasury_bond': {
        'page_oi': 'https://www.cmegroup.com/CmeWS/mvc/Volume/Details/F/307/{0}/{1}?tradeDate={0}',
        'page_status': 'https://www.cmegroup.com/CmeWS/mvc/Volume/TradeDates?exchange=CBOT'
    },
    'ultra_10-year_us_treasury_note': {
        'page_oi': 'https://www.cmegroup.com/CmeWS/mvc/Volume/Details/F/7978/{0}/{1}?tradeDate={0}',
        'page_status': 'https://www.cmegroup.com/CmeWS/mvc/Volume/TradeDates?exchange=CBOT'
    },
    'ultra_us_treasury_bond': {
        'page_oi': 'https://www.cmegroup.com/CmeWS/mvc/Volume/Details/F/3141/{0}/{1}?tradeDate={0}',
        'page_status': 'https://www.cmegroup.com/CmeWS/mvc/Volume/TradeDates?exchange=CBOT'
    },
    'euro_fx': {
        'page_oi': 'https://www.cmegroup.com/CmeWS/mvc/Volume/Details/F/58/{0}/{1}?tradeDate={0}',
        'page_status': 'https://www.cmegroup.com/CmeWS/mvc/Volume/TradeDates?exchange=CME'
    },
    'british_pound': {
        'page_oi': 'https://www.cmegroup.com/CmeWS/mvc/Volume/Details/F/42/{0}/{1}?tradeDate={0}',
        'page_status': 'https://www.cmegroup.com/CmeWS/mvc/Volume/TradeDates?exchange=CME'
    },
    'canadian_dollar': {
        'page_oi': 'https://www.cmegroup.com/CmeWS/mvc/Volume/Details/F/48/{0}/{1}?tradeDate={0}',
        'page_status': 'https://www.cmegroup.com/CmeWS/mvc/Volume/TradeDates?exchange=CME'
    },
    'japanese_yen': {
        'page_oi': 'https://www.cmegroup.com/CmeWS/mvc/Volume/Details/F/69/{0}/{1}?tradeDate={0}',
        'page_status': 'https://www.cmegroup.com/CmeWS/mvc/Volume/TradeDates?exchange=CME'
    },
    'swiss_franc': {
        'page_oi': 'https://www.cmegroup.com/CmeWS/mvc/Volume/Details/F/86/{0}/{1}?tradeDate={0}',
        'page_status': 'https://www.cmegroup.com/CmeWS/mvc/Volume/TradeDates?exchange=CME'
    },
    'russian_ruble': {
        'page_oi': 'https://www.cmegroup.com/CmeWS/mvc/Volume/Details/F/83/{0}/{1}?tradeDate={0}',
        'page_status': 'https://www.cmegroup.com/CmeWS/mvc/Volume/TradeDates?exchange=CME'
    },
    'eurodollar': {
        'page_oi': 'https://www.cmegroup.com/CmeWS/mvc/Volume/Details/F/1/{0}/{1}?tradeDate={0}',
        'page_status': 'https://www.cmegroup.com/CmeWS/mvc/Volume/TradeDates?exchange=CME'
    },
    'bitcoin_cme': {
        'page_oi': 'https://www.cmegroup.com/CmeWS/mvc/Volume/Details/F/8478/{0}/{1}?tradeDate={0}',
        'page_status': 'https://www.cmegroup.com/CmeWS/mvc/Volume/TradeDates?exchange=CME'
    }
}



file_directory = ""

def delete_mark(str, mark):
    #Удаляет из строки ненужный символ
    new_str = ""
    for x in str:
        if x != mark:
            new_str +=x
    return new_str

def get_get (page):
    #Получает url и извлекает из него объект json
    try:
        result = requests.get(page)
    except HTTPError as http_err:
        print(f"Ошибка HTTP: {http_err}!")
    except Exception as err:
        print(f"Что-пошло не так goпри запросе к странице {page}: {err}")
    else:
        print(f"Запрос к странице: {page} \n Успешен!")
        return result.json()

def parse_to_file(instrument):
    try:
        print(f"Обработка инструмента {instrument}")
        status_dict = get_get(pages_oi[instrument]['page_status'])
        if file_directory == "":
            file = open(f"{instrument}.txt", 'w')
        else:
            directory_folder = r"{}\{}.txt".format(file_directory, instrument)
            folder_path = os.path.dirname(directory_folder)  # Путь к папке с файлом
            if not os.path.exists(folder_path):  # Если пути не существует создаем его
                os.makedirs(folder_path)
            file = open(directory_folder, 'w')

        current_date = datetime.datetime.now().date() - datetime.timedelta(40)
        today_date = datetime.datetime.now().date()

        while current_date <= today_date:
            string_date = delete_mark(str(current_date), '-')
            oi_dict = get_get(pages_oi[instrument]['page_oi'].format(string_date, 'F'))

            totals_oi = oi_dict['totals']['atClose']

            status_flag = "FINAL"
            for trade_day in status_dict:
                if trade_day['tradeDate'] == oi_dict['tradeDate'] and trade_day['reportType'] == 'PRELIMINARY':
                    status_flag = "PRELIM"
                    break

            if totals_oi == '0':
                if status_flag == "PRELIM":
                    oi_dict = get_get(pages_oi[instrument]['page_oi'].format(string_date, 'P'))
                    totals_oi = oi_dict['totals']['atClose']
                else:
                    print(f"Дата {current_date}, не записывается в файл {instrument}.txt (торги не велись)\n")
                    current_date = current_date + datetime.timedelta(1)
                    continue

            date_with_point = string_date[0] + string_date[1] + string_date[2] + string_date[3] + '.' + string_date[4] + \
                              string_date[5] + '.' + string_date[6] + string_date[7]
            totals_oi = delete_mark(totals_oi, ',')
            file.write(f"{date_with_point}\t{status_flag}\tTOTAL\t{totals_oi}\t")

            for month in oi_dict['monthData']:
                month_name = month['month']
                month_oi = month['atClose']
                month_oi = delete_mark(month_oi, ',')
                file.write(f"{month_name}\t{month_oi}\t")

            file.write('\n')
            print(f"Данные по дате {current_date} для инструмента {instrument} успешно добавлены!\n")
            current_date = current_date + datetime.timedelta(1)

    except Exception as err:
        print(f"Что-пошло не так при обработке инструмента {instrument}: {err}")
    else:
        print(f"Файл {instrument}.txt успешно обработан!\n")


try:
    with requests.Session() as se:
        se.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
            "Accept-Encoding": "gzip, deflate",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en"
        }
    instrument_list = list(pages_oi.keys())

    my_instrument_list = instrument_list
    file_directory = ""

    print("Добро пожаловать в программу-парсер Open Interest\n")
    print("Для выбора копируемых биржевых инструментов введите 1, для ввода директории копирования 2.\nДля старта программы введите go\n")

    while True:
        print(f"Текущие настройки:\nКопируемые инструменты:")
        for instr in my_instrument_list:
            print(instr)
        print(f"Текущая директория: {file_directory}. Если директория пустая, то файлы создаются в директории с программой.")
        a = input(">>>")
        if a == '1':
            my_instrument_list = []
            b = input("Введите через пробел номера копируемых инстументов:\n1 - chicago_srw_wheat_cbot,\n2 - bitcoin_cme\n>>>").split()
            num_list = list(map(int, b))
            for x in num_list:
                if x > 0 and x <= len(instrument_list):
                    my_instrument_list.append(instrument_list[x-1])
                else:
                    print(f"Нет инструмента с таким номером: {x}")
        if a == '2':
           file_directory = input("Введите необходимую директорию для сохранения файлов:\n>>>")
        if a == 'go':
            print("Запуск парсинга...")
            for instr in my_instrument_list:
                parse_to_file(instr)
            break

except Exception as err:
    print(f"Что-пошло не так при работе программы: {err}")
else:
    print("Программа завершена")
    while a != "~~":
        a = input("Для выхода из программы введите '~~'")

