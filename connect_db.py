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
        
        # with self.con.cursor() as cur:
        #     cur.execute("SELECT VERSION()")
        #     version = cur.fetchone()
        #     cur.execute("CREATE DATABASE IF NOT EXISTS `kartoteka_klientov`")
        #     dbname = cur.fetchone()
        #         # print 'db exists'
        #     print(str("Database version: {}".format(version['VERSION()']))) 
            # print(str("Database version: {}".format(dbname['VERSION()']))) 
            
        #     cur.close()
    # def insert_data_by(self, data_list):
        
            # self.cursor = self.con.cursor()
        
        if data_list is not None:
            with self.con.cursor() as cur:
                        # cur.execute("SELECT VERSION()")
                        # version = cur.fetchone()
                # sql = "INSERT INTO `klient_list` (`klient_name`, `klient_age`) VALUES (%s, %s)"
                # cur.execute(sql, (data_list[1]['name'], data_list[1]['date']))
                        # self.con.commit()
                        # cur = self.con.cursor()
                # cur.execute("SELECT (`klient_id`) FROM `klient_list` WHERE `klient_name`=%s", data_list[1]['name'])
                # client_id = cur.fetchall()
                # self.con.commit()
                # cur = self.con.cursor()
                print(str("Клиент: {} - {} года рождения; ".format(data_list[1]['name'], data_list[1]['date'])))  # client_id[0]['klient_id']
                for ph in data_list[1]['phones']:
                    if ph[0] is not None:
                        # sql = "INSERT INTO `phones_list` (`klient_phone_id`, `phone_num`, `abonent_name`) VALUES (%s, %s, %s)"
                        # cur.execute(sql, (client_id[0]['klient_id'], ph[0], ph[1]))
                        # self.con.commit()
                        print(str("Телефон: {} : {} добавлен в базу к {}; ".format(ph[0], ph[1], data_list[1]['name']))) 
               
                cur = self.con.cursor()
                for sr in data_list[1]['servis']:
                    comment = ''
                    if sr[0] is not None:
                        # sql2 = "INSERT INTO `services_received` (`received_klient_id`, `received_text`, `received_date`, `received_comment`) VALUES (%s, %s, %s, %s)"
                        # if sr[1] == 1111:
                        #     comment = sr[0]
                        # cur.execute(sql2, (client_id[0]['klient_id'], sr[0] if comment == '' else None, sr[1] if comment == '' else None, comment))
                        # self.con.commit()
                        print(str("Лечение: {} дата: {} получил клиент: {}; ".format(sr[0], sr[1], data_list[1]['name']))) 
                print("-------------------------------------------------------------------------")
            cur.close() 
            # self.con.commit() 
    