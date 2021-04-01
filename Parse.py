import requests
import datetime
from requests.exceptions import HTTPError
import os
import time
import fake_useragent

page_exchanges = "https://www.cmegroup.com/CmeWS/mvc/Volume/TradeDates?exchange="
page_oi_profiles = "https://www.cmegroup.com/CmeWS/mvc/Volume/Details/F/{0}/{1}/{2}?tradeDate={1}"

user = fake_useragent.UserAgent().random

header = {
    'user-agent': user
}

se = requests.session()

oi_profiles = {
    'chicago_srw_wheat_cbot':       {'number': '323',   'exchange': 'CBOT'},
    'kc_hrw_wheat_cbot':            {'number': '348',   'exchange': 'CBOT'},
    'corn_cbot':                    {'number': '300',   'exchange': 'CBOT'},
    'soybean_cbot':                 {'number': '320',   'exchange': 'CBOT'},
    'soybean_meal_cbot':            {'number': '310',   'exchange': 'CBOT'},
    'soybean_oil_cbot':             {'number': '312',   'exchange': 'CBOT'},
    'rough_rice':                   {'number': '336',   'exchange': 'CBOT'},
    'cash-settled_butter_cme':      {'number': '26',    'exchange': 'CME'},
    'cash-settled_cheese_cme':      {'number': '5201',  'exchange': 'CME'},
    'class_iii_milk_cme':           {'number': '27',    'exchange': 'CME'},
    'feeder_cattle_cme':            {'number': '34',    'exchange': 'CME'},
    'lean_hog_cme':                 {'number': '19',    'exchange': 'CME'},
    'live_cattle_cme':              {'number': '22',    'exchange': 'CME'},
    'copper_comex':                 {'number': '438',   'exchange': 'COMEX'},
    'gold_comex':                   {'number': '437',   'exchange': 'COMEX'},
    'silver_comex':                 {'number': '458',   'exchange': 'COMEX'},
    'platinum_nymex':               {'number': '446',   'exchange': 'NYMEX'},
    'palladium_nymex':              {'number': '445',   'exchange': 'NYMEX'},
    'aluminum_mw_us_transaction_premium_platts(25mt)_comex':        {'number': '6746', 'exchange': 'COMEX'},
    'us_midwest_domestic_hot-rolled_coil_steel_(cru)_index_comex':  {'number': '2508', 'exchange': 'COMEX'},
    'wti_crude_oil_nymex':          {'number': '425',   'exchange': 'NYMEX'},
    'henry_hub_natural_gas_nymex':  {'number': '444',   'exchange': 'NYMEX'},
    'e-mini_s&p500_cme':            {'number': '133',   'exchange': 'CME'},
    'e-mini_russell_2000_index_cme':{'number': '8314',  'exchange': 'CME'},
    'e-mini_nasdaq-100_cme':        {'number': '146',   'exchange': 'CME'},
    'e-mini_s&p_midcap_400_cme':    {'number': '166',   'exchange': 'CME'},
    's&p500_cme':                   {'number': '132',   'exchange': 'CME'},
    '10_Year_t-note_cbot':          {'number': '316',   'exchange': 'CBOT'},
    '5_Year_t-note_cbot':           {'number': '329',   'exchange': 'CBOT'},
    '2_Year_t-note_cbot':           {'number': '303',   'exchange': 'CBOT'},
    '30_day_federal_funds_cbot':    {'number': '305',   'exchange': 'CBOT'},
    'us_treasury_bond_cbot':        {'number': '307',   'exchange': 'CBOT'},
    'ultra_10-year_us_treasury_note_cbot':                          {'number': '7978', 'exchange': 'CBOT'},
    'ultra_us_treasury_bond_cbot':  {'number': '3141',  'exchange': 'CBOT'},
    'euro_fx_cme':                  {'number': '58',    'exchange': 'CME'},
    'british_pound_cme':            {'number': '42',    'exchange': 'CME'},
    'canadian_dollar_cme':          {'number': '48',    'exchange': 'CME'},
    'australian_dollar_cme':        {'number': '37',    'exchange': 'CME'},
    'new_zealand_dollar_cme':       {'number': '78',    'exchange': 'CME'},
    'japanese_yen_cme':             {'number': '69',    'exchange': 'CME'},
    'swiss_franc_cme':              {'number': '86',    'exchange': 'CME'},
    'russian_ruble_cme':            {'number': '83',    'exchange': 'CME'},
    'eurodollar_cme':               {'number': '1',     'exchange': 'CME'},
    'bitcoin_cme':                  {'number': '8478',  'exchange': 'CME'},
}

file_directory = ""
point_date = datetime.datetime.now().date() - datetime.timedelta(40)

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
        result = requests.get(page, headers=header)
    except HTTPError as http_err:
        print(f"Ошибка HTTP: {http_err}!")
    except Exception as err:
        print(f"Что-пошло не так при запросе к странице {page}: {err}")
    else:
        print(f"Запрос к странице: {page} \n Успешен!")
        return result.json()

def parse_to_file(instrument, date, recording_mode):
    try:
        print(f"Обработка инструмента {instrument}")
        page_status = page_exchanges + oi_profiles[instrument]['exchange']
        status_dict = get_get(page_status)
        if file_directory == "":
            directory_folder = r"{}\{}.txt".format(os.path.dirname(os.path.abspath(__file__)), instrument)
            file = open(directory_folder, recording_mode)
        else:
            directory_folder = r"{}\{}.txt".format(file_directory, instrument)
            folder_path = os.path.dirname(directory_folder)  # Путь к папке с файлом
            if not os.path.exists(folder_path):  # Если пути не существует создаем его
                os.makedirs(folder_path)
            file = open(directory_folder, recording_mode)

        current_date = date
        today_date = datetime.datetime.now().date()

        while current_date <= today_date:
            string_date = delete_mark(str(current_date), '-')
            page_oi = page_oi_profiles.format(oi_profiles[instrument]['number'], string_date, 'F')
            oi_dict = get_get(page_oi)

            totals_oi = oi_dict['totals']['atClose']

            status_flag = "FINAL"
            for trade_day in status_dict:
                if trade_day['tradeDate'] == oi_dict['tradeDate'] and trade_day['reportType'] == 'PRELIMINARY':
                    status_flag = "PRELIM"
                    break

            if totals_oi == '0':
                if status_flag == "PRELIM":
                    page_oi = page_oi_profiles.format(oi_profiles[instrument]['number'], string_date, 'P')
                    oi_dict = get_get(page_oi)
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
            time.sleep(5)

    except Exception as err:
        print(f"Что-пошло не так при обработке инструмента {instrument}: {err}")
    else:
        print(f"Файл {instrument}.txt успешно обработан!\n")

def red_end_line(file, number_line_fr_end = 0):
    count_n = -1
    pos = 2
    while count_n != number_line_fr_end:
        str = ""
        ch = ''
        while True:
            pos += 1
            file.seek(-pos, 2)
            ch = file.read(1)
            ch = ch.decode('UTF-8')
            if ch == '\n' or ch == '\r':
                break
            str = ch + str
        count_n +=1
    return str

def get_seek_endline(file, number_line_fr_end = 0):
    count_n = -1
    pos = 1
    while count_n != number_line_fr_end:
        while True:
            pos += 1
            file.seek(-pos, 2)
            ch = file.read(1)
            ch = ch.decode('UTF-8')
            if ch == '\n':
                break
        count_n += 1
    return pos

def update():
    if file_directory == "":
        directory_folder = r"{}".format(os.path.dirname(os.path.abspath(__file__)))
    else:
        directory_folder = r"{}".format(file_directory)

    files = os.listdir(directory_folder)
    files_list = list(filter(lambda x: x.endswith('.txt'), files))
    instr_list = []
    for file in files_list:
        instr = file.split('.')[0]
        if instr in oi_profiles.keys():
            instr_list.append(instr)

    for instrument in instr_list:
        file_instr = open(f"{instrument}.txt", 'ab+')
        ln = red_end_line(file_instr)
        list_line = ln.split('\t')
        date_str = list_line[0].split('.')
        date = datetime.date(year=int(date_str[0]), month=int(date_str[1]), day=int(date_str[2]))
        if (list_line[1] == "PRELIM"):
            pos = get_seek_endline(file_instr)
            file_instr.seek(-pos, 2)
            file_instr.truncate()
        else:
            date += datetime.timedelta(1)

        file_instr.close()
        parse_to_file(instrument, date, 'a+')



def keep_window_open():
    a = ""
    while a != "~~":
        a = input("Для выхода из программы введите '~~'")

try:
    with requests.Session() as se:
        se.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
            "Accept-Encoding": "gzip, deflate",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en"
        }
        instrument_list = list(oi_profiles.keys())

        my_instrument_list = instrument_list

        print("Добро пожаловать в программу-парсер Open Interest\n")
        print("Для выбора копируемых биржевых инструментов введите 1, для ввода директории копирования 2.\nДля старта первоначального копирования введите go, для обновления по инстументам up\n")

        while True:
            print(f"Текущие настройки:\nКопируемые инструменты:")
            for instr in my_instrument_list:
                print(instr)
            print(f"Текущая директория: {file_directory}. Если директория пустая, то файлы создаются в директории с программой.")
            a = input(">>>")
            if a == '1':
                my_instrument_list = []
                print("Введите через пробел номера копируемых инстументов:")
                for i in range(1, len(instrument_list)+ 1):
                    print(f"{i} - {instrument_list[i-1]}")
                b = input(">>>").split()

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
                    parse_to_file(instr, point_date, 'w')
                break
            if a == 'up':
                print("Запуск обновления инструментов...")
                update()
                break

except Exception as err:
    print(f"Что-пошло не так при работе программы: {err}")
    keep_window_open()

else:
    print("Программа завершена")
    keep_window_open()

