import lists
import re
from openpyxl import load_workbook as lw
from datetime import datetime as dt
from connect_db import CRUDDB

db = CRUDDB('localhost', 'root', 'root', 'kartoteka_klientov')
repl = lists.replasment()
filename = 'kartoteka.min.xlsx'
# filename = 'min.test2.xlsx'
# filename = 'КАРТОТЕКА.xlsx'


def format_date(str_date):
    """
    Обработка строки ДАТА и приведение её к нужному формату
    добавляем рандомный день и месяц если их нет
    """
    new_date = str(str_date).strip()
    newdate = re.findall(r"(\d+\.\d*\.\d{4})", new_date)
    if len(newdate) == 0:
        newdate = re.findall(r"(\d{4})", new_date)
        # return newdate
    for new in newdate:
        if len(new) == 4:
            new = "13-10-"+new.strip()
        else:
            new = re.sub("\.", "-", new.strip())
            try:
                value_date = dt.strptime(new, "%d-%m-%Y").date()
            except ValueError:
                value_date = new
                print("Дата введена не коректно {} ".format(value_date))
                break
            return value_date


def servises(value, repl_list):
    """
    Поручаем строку и кортеж с данными для правки строки.
    Исправляем неточности в строке, методом sub() приводим строку к единому стилю написания
    (убираем лишние пробелы и символы). Получаем все совпадения с шаблоном методом findall()
    и возвращаем результат
    """
    servis_list = []
    """Убираем в строке лишнее"""
    for x, y in repl_list:
        value = re.sub(r"{}".format(x), y, value) #"^([а-яА-Я\.;\s]?)+$"gm
    """Поучаем длинну строки"""
    
    count_templ = re.fullmatch(r"^([а-яА-Я\.,;()\s]?)+$", value)
    """И если совпадает добавляем в список"""
    if count_templ is not None:
        servis_list.append((count_templ.group(), None))

    
    """Получаем индекс последнего вхождения даты"""
    vk_l = re.search(r"[^\.\d{2,4}]+[*?\w\s+\.,\+()+][^\d]+$", value)
    """Проверяем, осталось ли еще что нибудь после последней даты"""
    infor = re.search(r"(.*?\w+\s+\d{4}[\s\D]?)$", value)
    
    if vk_l is not None and vk_l.start() > 0:
        komment = value[vk_l.start():].strip()
        komment = re.sub(r"^(/)", "", komment)
        servis_list.append((komment, None))
    elif infor is not None:
        servis_list.append((value[:infor.end()], dt.strptime("01/01/1970", "%d/%m/%Y").date()))
    
    match_date = re.findall(r"(.*?\d+\.\d+\.\d+)[;\s]?", value)

    sub_servis_str = ''
    for i in range(len(match_date)):
        l = re.search(r"(\d+\.\d+\.\d)", match_date[i])

        servis_string = match_date[i][:l.start()]
        data_string = match_date[i][l.start():]
        s = re.search(r"(\.\w{2})$", data_string)
        if s:
            data_string = data_string[:s.start()] + "/20" + data_string[-2:]
        data_string = re.sub("\.", "/", data_string)

        if re.match(r"(\d+\/\d+\/20\d{2})$", data_string) is not None:
            # print(data_string)
            date_by = dt.strptime(data_string, "%d/%m/%Y").date()
        else:
            date_by = dt.strptime("01/01/1970", "%d/%m/%Y").date()

        servis_string = re.sub(r"^(/)", "", servis_string)
        if len(servis_string) != 0:
            sub_servis_str = servis_string
            servis_list.append((servis_string, date_by))
        else:
            servis_list.append((sub_servis_str, date_by))

    if servis_list is not None:
        return servis_list


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
                            id_dist.update(date=format_date(value))
                    else:
                        id_dist.update(date=None)
                elif i == 3:
                    if value is not None:
                        id_dist.update(servis=servises(value, repl))
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
q = 2
for items in massiv:
    if items[1]['name'] is None:
        continue
    else:
        db.chench_connect_db(items, q)
        # print("{} : {}".format(items[1]['name'], items[1]['servis']), end=" ")
        # print(" ")