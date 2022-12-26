import pymysql


class CRUDDB:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.con = ''

        self.con = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            cursorclass=pymysql.cursors.DictCursor)

    def chench_connect_db(self, data_list):

        if data_list is not None:
            with self.con.cursor() as cur:

                sql = "INSERT INTO `klient_list` (`klient_name`, `klient_age`) VALUES (%s, %s)"
                cur.execute(sql, (data_list[1]['name'], data_list[1]['date']))
                       
                self.con.commit()
                cur.execute(
                    "SELECT (`klient_id`) FROM `klient_list` WHERE `klient_name`=%s", data_list[1]['name'])
                client_id = cur.fetchall()

                print(str(
                    "Клиент: {} - {} года рождения;".format(data_list[1]['name'], data_list[1]['date'])))
                for ph in data_list[1]['phones']:
                    if ph[0] is not None:
                        cur = self.con.cursor()
                        sql = "INSERT INTO `phones_list` (`klient_phone_id`, `phone_num`, `abonent_name`) VALUES (%s, %s, %s)"
                        cur.execute(
                            sql, (client_id[0]['klient_id'], ph[0], ph[1]))
                        cur.commit()
                        print(str("Телефон: {} : {} добавлен в базу к {};".format(
                            ph[0], ph[1], data_list[1]['name'])))

                for sr in data_list[1]['servis']:
                    comment = ''
                    if sr[0] is not None:
                        cur = self.con.cursor()
                        sql2 = "INSERT INTO `services_received` (`received_klient_id`, `received_text`, `received_date`, `received_comment`) VALUES (%s, %s, %s, %s)"
                        if sr[1] is None:
                            comment = sr[0]
                        cur.execute(sql2, (client_id[0]['klient_id'], sr[0] if comment ==
                                    '' else None, sr[1] if comment == '' else None, comment))
                        cur.commit()
                        print(str("Лечение: {} дата: {} получил клиент: {};".format(
                            sr[0], sr[1], data_list[1]['name'])))
                print(
                    "-------------------------------------------------------------------------")
            cur.close()
    
    
    def not_db_add_only_view(self, data_list):
        if data_list is not None:
            print(data_list[1]['servis'])
            # if data_list[1]['servis'] is None:
            #     print(str(
            #         "Клиент: {} - {} года рождения;".format(data_list[1]['name'], data_list[1]['date'])))
            #     for ph in data_list[1]['phones']:
            #         if ph[0] is not None:
            #             print(str("Телефон: {} : {} добавлен в базу к {};".format(
            #                 ph[0], ph[1], data_list[1]['name'])))

                
            #     for sr in data_list[1]['servis']:
            #         comment = ''
            #         if sr[0] is not None:
            #             print(str("Лечение: {} дата: {} получил клиент: {};".format(sr[0], sr[1], data_list[1]['name'])))
            print("-------------------------------------------------------------------------")    # self.con.commit()
    
    
    def add_db_if_none(self, data_list):
            with self.con.cursor() as cur:

                # sql = "INSERT INTO `klient_list` (`klient_name`, `klient_age`) VALUES (%s, %s)"
                # cur.execute(sql, (data_list[1]['name'], data_list[1]['date']))
                if data_list[1]['date'] is not None:        
                    cur.execute(
                        "SELECT (`klient_id`) FROM `klient_list` WHERE `klient_name`=%s AND `klient_age`=%s", (data_list[1]['name'], data_list[1]['date']))
                else:
                    cur.execute(
                        "SELECT (`klient_id`) FROM `klient_list` WHERE `klient_name`=%s", data_list[1]['name'])
                
                client_id = cur.fetchall()
                # self.con.commit()
                # cur = self.con.cursor()
                if len(client_id) != 0:
                    print(str(
                            f"Клиент: {data_list[1]['name']} - {data_list[1]['date']} года рождения {client_id[0]['klient_id']} УЖЕ в базе;"))
                else:
                    print(str(
                        "Клиент: {} - {} года рождения;".format(data_list[1]['name'], data_list[1]['date'])))
                        # raise ind

                for ph in data_list[1]['phones']:
                    if ph[0] is not None:
                        print(str("Телефон: {} : {} ) добавлен в базу к {};".format(
                            ph[0], ph[1], data_list[1]['name'])))

                
                for sr in data_list[1]['servis']:
                    comment = ''
                    if sr[0] is not None:
                        print(str("Лечение: {} дата: {} получил клиент: {};".format(sr[0], sr[1], data_list[1]['name'])))
                cur.close()
                print("-------------------------------------------------------------------------")    # self.con.commit()
