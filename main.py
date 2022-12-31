import re, lists
from openpyxl import load_workbook as lw
from datetime import datetime as dt
from connect_db import CRUDDB
import models

db = CRUDDB('localhost', 'root', 'root', 'kartoteka_klientov')
repl = lists.replasment()
# filename = 'kartoteka.new.xlsx'
filename = 'kartoteka.min.xlsx'
# filename = 'КАРТОТЕКА.xlsx'


def new_format_date(value_date):
    """
    Обработка строки ДАТА и приведение её к нужному формату
    добавляем рандомный день и месяц если их нет
    """
    search = re.search(r"(\d+\.\d+\.\d{2,4})", str(value_date))
    
    if search:
        new_date = re.sub(r"[\.,]", "-", search.group())
        kz = re.search(r"(\-\d{2})$", new_date)
        if kz is not None:
            left = new_date[kz.start():]
            right = new_date[:kz.start()]
            new_date_ = right + '-20' + left[1:]
            return dt.strptime(new_date_.strip(), "%d-%m-%Y").date()
        else:
            return dt.strptime(new_date, "%d-%m-%Y").date()
    else:
        one_yahr_ = re.search(r"(\d{4})", str(value_date))
        one_yahr = "01-01-" + one_yahr_.group()
        return dt.strptime(one_yahr.strip(), "%d-%m-%Y").date()
        
    


def new_servises(value, repl_list):
    servis_ = []
    """Убираем в строке лишнее"""
    for x, y in repl_list:
        value = re.sub(r"{}".format(x), y, value)
   
    """Если в строке есть дата добавляем в список"""
    servis_list = re.findall(r"(.*?\d+\.\d+\.\d+)[;\s/]?", value)
    
    if len(servis_list) > 0:
        for ser in servis_list:
            val = str(ser).strip(". / ,")
            by_date = re.search(r"(\d+\.\d+\.\d+)", val)
            new_date = new_format_date(by_date.group())
            by_text = val[:by_date.start()].strip()
            if by_text:
                servis_.append((by_text, new_date))
                sub_by_text = by_text
            else:
                servis_.append((sub_by_text, new_date))

    # """Если в строке есть что то после даты"""
    # string_no_date = re.search(r"[\D]+(\w)+\s?$", value)# "[^\.\d]{2,4}?([а-яА-Я0-9_\+\"\-\s]*)([\d]{4})?$"
    # if string_no_date:
    #     servis_.append((string_no_date.group().strip(), None)) "^(\w)+(?:\d{0,2}[^\.])+$"

    """Если в строке только текст без даты"""
    text_yahr = re.search(r"[^\.\d]{2,4}?([а-яА-Я0-9_!(,)\+\"\-\s]*)([\d]{4})?$", value)
    if text_yahr:
        servis_.append((text_yahr.group().strip(), None))

    return servis_


def phones_names(phonesnames):
    phone_list = []
    if len(str(phonesnames).strip()) >= 11:
        ph_list = str(phonesnames).split('/')
    else:
        phone_list.append((None, "Телефон не указан"))
        return phone_list
    col = len(ph_list)
    for t in range(col):
        phon_name = ph_list[t].strip()
        if phon_name.isdigit() is False:
            tel_name = phon_name.split(' ', 1)
            if len(tel_name) == 2:
                phone_list.append((tel_name[0], tel_name[1]))
            else:
                phone_list.append((None, "Телефон не указан"))
        else:
            if len(phon_name) == 11:
                phone_list.append((ph_list[t], None))
    return phone_list


def add_list_exel():
    """
    Получаем файл exel, построчно проверяем данные, исправляем где нужно и
    собираем в словарь. Затем передаем в функцию для добавления в базу данных
    """
    wrkbk = lw(filename)
    file = wrkbk['alk']   # active
    id = 1

    main_dist = {}
    for row in file.values:
        i = 1
        id_dist = {}        
        col = len(str(row[0]))
        if col < 2 or row[0] is None:
            continue
        else:
            for value in row:
                if value is not None and i == 1:
                    fio = value.replace("*", "")
                    id_dist.update(name=fio.strip())
                elif i == 2:
                    if value is not None:
                        try:
                            id_dist.update(date=value.date())
                        except AttributeError:
                            id_dist.update(date=new_format_date(value))
                    else:
                        id_dist.update(date=None)
                elif i == 3:
                    if value is not None:
                        id_dist.update(servis=new_servises(value, repl))
                    else:
                        id_dist.update(servis=[('Информация отсутствует', None)])
                elif i == 4:
                    id_dist.update(phones=phones_names(value))

                i += 1
        main_dist.update({id: id_dist})
        id += 1
    return main_dist.items()

massiv = add_list_exel()
# 1 Пставляем в БД
# 0 Просто распечатываем
# 2 Проверяем есть ли уже в БД
# q = 1
# for items in massiv:
#     if items[1]['name'] is None:
#         continue
#     else:
#         if q == 0:
#             db.not_db_add_only_view(items)
#         elif q == 1:
#             db.chench_connect_db(items)
#         else:
#             db.add_db_if_none(items)
        # print("{} : {}".format(items[1]['name'], items[1]['servis']), end=" ")
        # print(" ")
age = dt.strptime('12-10-1948', "%d-%m-%Y").date()

data = ['Петрушкина Людмила Прокофьевна', age]

colum_list = ['klient_name', 'klient_age']  

table = 'klient_list'

mode = models.Model(data, table, colum_list)
# list_klients = mode.model_select()
# klient_by = mode.model_select_by('klient_id', 126)
# mode.model_insert()
# mode.model_update('klient_id', 120)
mode.model_delete('klient_id', 124)
# print(klient_by[0]['klient_age'])
# for m in list_klients:
#     print(m['klient_id'])