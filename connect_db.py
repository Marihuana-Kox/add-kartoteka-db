import pymysql


class CRUDDB:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.con = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            cursorclass=pymysql.cursors.DictCursor)
            

    def chench_connect_db(self, data_list):

        if data_list is not None:
            with self.con.cursor() as cur:
                """Ищем совпадения в бд"""
                cur.execute(
                    "SELECT `klient_id`, `klient_name` FROM `klient_list` WHERE `klient_name`=%s", data_list[1]['name'])
                """Сохраняеи id в переменной"""
                client_id = cur.fetchall()

                if len(client_id) == 0:
                    """Пытаемся вставить запись, если такой нет то добавляем"""
                    sql = "INSERT INTO `klient_list` (`klient_name`, `klient_age`) VALUES (%s, %s)"
                    cur.execute(sql, (data_list[1]['name'], data_list[1]['date']))
                    self.con.commit()
                    print(str(
                    "Клиент: {} - {} года рождения;".format(data_list[1]['name'], data_list[1]['date'])))
                    
                    """Получаем id последней доюавленой записи"""
                    cur = self.con.cursor()
                    cur.execute(
                        "SELECT `klient_id`, `klient_name` FROM `klient_list` WHERE `klient_name`=%s", data_list[1]['name'])
                    """Сохраняеи id в переменной"""
                    client_id = cur.fetchall()
                    cli_id = client_id[0]['klient_id']
                   
                    for ph in data_list[1]['phones']:
                        if ph[0] is not None:
                            cur = self.con.cursor()
                            sql = "INSERT INTO `phones_list` (`klient_phone_id`, `phone_num`, `abonent_name`) \
                                VALUES (%s, %s, %s)"
                            cur.execute(
                                sql, (cli_id, ph[0], ph[1]))
                            self.con.commit()
                            print(str("Телефон: {} : {} добавлен в базу к {};".format(
                                ph[0], ph[1], data_list[1]['name'])))

                    for sr in data_list[1]['servis']:
                        comment = ''
                        if sr[0] is not None:
                            cur = self.con.cursor()
                            sql2 = "INSERT INTO `services_received` (`received_klient_id`, `received_text`, \
                                `received_date`, `received_comment`) VALUES (%s, %s, %s, %s)"
                            if sr[1] is None:
                                comment = sr[0]
                            cur.execute(sql2, (cli_id, sr[0] if comment ==
                                        '' else None, sr[1] if comment == '' else None, comment))
                            self.con.commit()
                            print(str("Лечение: {} дата: {} получил клиент: {};".format(
                                sr[0], sr[1], data_list[1]['name'])))
                    print(
                        "-------------------------------------------------------------------------")
                    cur.close()
                else:
                    cli_id = client_id[0]['klient_id']
                    cur = self.con.cursor()
                    """Получаем id последней записи или уже существующей"""
                    cur.execute(
                        "SELECT * FROM `phones_list` WHERE `klient_phone_id`=%s", cli_id)
                    """Сохраняеи id в переменной"""
                    phones_ = cur.fetchall()
                    name = data_list[1]['name']
                    for ph in data_list[1]['phones']:
                        number = ph[0]
                        if number is not None:
                            abo_name = ph[1]
                            if len(phones_) == 0:
                                cur = self.con.cursor()
                                sql = "INSERT INTO `phones_list` (`klient_phone_id`, `phone_num`, `abonent_name`) \
                                    VALUES (%s, %s, %s)"
                                cur.execute(
                                    sql, (cli_id, number, abo_name))
                                self.con.commit()
                                print(str("Новый телефон: {} : {} добавлен в базу;".format(
                                    number, abo_name)))
                            else:
                                for phone in phones_:    
                                    if number == phone['phone_num'] and cli_id == phone['klient_phone_id']:
                                        print(str("Этот номер уже: {} : {} есть в базу".format(
                                            number, abo_name)))
                                        continue
                                    else:
                                        sql = "INSERT INTO `phones_list` (`klient_phone_id`, `phone_num`, `abonent_name`) \
                                        VALUES (%s, %s, %s)"
                                    cur.execute(
                                        sql, (cli_id, number, abo_name))
                                    self.con.commit()
                                    print(str("Еще один номер: {} : {} добавлен в базу к {};".format(
                                            number, abo_name, name)))

                    for sr in data_list[1]['servis']:
                        comment = ''
                        if sr[0] is not None:
                            titls_ervis0 = sr[0]
                            date_servis1 = sr[1]
                            cur = self.con.cursor()
                            """Получаем id последней записи или уже существующей"""
                            cur.execute(
                                "SELECT `received_text`, `received_date` FROM `services_received` \
                                     WHERE `received_klient_id`=%s", cli_id)
                            """Сохраняеи id в переменной"""
                            services_ = cur.fetchall()
                            if len(services_) == 0:
                                cur = self.con.cursor()
                                sql2 = "INSERT INTO `services_received` (`received_klient_id`, `received_text`, \
                                    `received_date`, `received_comment`) VALUES (%s, %s, %s, %s)"
                                if sr[1] is None:
                                    comment = titls_ervis0
                                cur.execute(sql2, (cli_id, titls_ervis0 if comment ==
                                            '' else None, date_servis1 if comment == '' else None, comment))
                                self.con.commit()
                                print(str("Лечение: {} дата: {} получил клиент: {};".format(
                                    titls_ervis0, date_servis1, name)))
                                print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
                            else:
                                ser = services_[0] 
                                if ser['received_text'] == titls_ervis0 and ser['received_date'] == date_servis1:
                                    print(str("Этот сервис уже: {} : {} : {} добавлен в базу".format(
                                        titls_ervis0, date_servis1, name)))
                                    print("__________________________________________________________________")
                                    continue
                                else:
                                    cur = self.con.cursor()
                                    sql2 = "INSERT INTO `services_received` (`received_klient_id`, `received_text`, \
                                        `received_date`, `received_comment`) VALUES (%s, %s, %s, %s)"
                                    if sr[1] is None:
                                        comment = titls_ervis0
                                    cur.execute(sql2, (cli_id, titls_ervis0 if comment ==
                                                '' else None, date_servis1 if comment == '' else None, comment))
                                    self.con.commit()
                                    print(str("Лечение добавлено: {} дата: {} получил клиент: {};".format(
                                        titls_ervis0, date_servis1, name)))
                    print(
                        "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                    cur.close()
                    print(str(
                            f"Клиент: {name} - {date_servis1} \
                                года рождения {cli_id} УЖЕ в базе;"))
                    print(
                        "**************************************************************************")
                
    
    
    def not_db_add_only_view(self, data_list):
        if data_list is not None:
            print(str(
                "Клиент: {} - {} года рождения;".format(data_list[1]['name'], data_list[1]['date'])))
            for ph in data_list[1]['phones']:
                if ph[0] is not None:
                    print(str("Телефон: {} : {} добавлен в базу к {};".format(
                        ph[0], ph[1], data_list[1]['name'])))
                else:
                    print(str("Телефон {} не указал;".format(
                        data_list[1]['name'])))

            
            for sr in data_list[1]['servis']:
                comment = ''
                if sr[0] is not None:
                    print(str("Лечение: {} дата: {} получил клиент: {};".format(sr[0], sr[1], data_list[1]['name'])))
            print("-------------------------------------------------------------------------")    # self.con.commit()