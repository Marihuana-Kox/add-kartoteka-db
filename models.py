from connect_db import CRUDDB
import pymysql
db = CRUDDB('localhost', 'root', 'root', 'kartoteka_klientov')


class Model:

    def __init__(self, table, colum_list):
        self.table = table
        self.colum_list = colum_list

    def model_select(self):
        with db.con.cursor() as cur:
            cur.execute(f"SELECT * FROM {self.table}")
            db_date = cur.fetchall()
        return db_date

    def model_select_by(self, tabl_id, id):
        cur = db.con.cursor()
        cur.execute(f"SELECT * FROM {self.table} WHERE {tabl_id}='{id}'")
        db_date_by = cur.fetchall()
        return db_date_by

    def model_insert(self, data):
        columns = ", ".join([row for row in self.colum_list])
        rows = ", ".join(['%s' for i in range(len(data))])
        sql = f"INSERT INTO {self.table} ({columns}) VALUES ({rows})"
        with db.con.cursor() as cur:
            try:
                cur.execute(sql, (data))
                db.con.commit()
                print("Запись успешно создана")
            except pymysql.err.IntegrityError:
                print("Такая запись, уже есть в БД")
       
    
    def model_insert_not_duble(self, data ,params):
        """Игнорирует добавление дублирующих записей"""
        colum_list = ['klient_phone_id', 'phone_num', 'abonent_name']
        table = 'phones_list'
        phones = Model(table, colum_list)
        phone_ =[]
        cur = db.con.cursor()
        sql = f"SELECT {params[0]} FROM {self.table} WHERE "\
                    f"{params[1]}='{params[2]}'"
        cur.execute(sql)
        duble = cur.fetchall()
        if len(duble) != 0:
            for ph in duble:
                phone_.append(ph['phone_num'])

            if data[1] in phone_:
                print(f"Номер: {data[1]} уже есть.")
            else:
                phones.model_insert(data)
        else:
            phones.model_insert(data) 
    

    def model_update(self, data, tabl_id, id):
        columns = ", ".join([row + '=%s' for row in self.colum_list])
        sql = f"UPDATE {self.table} SET {columns} WHERE {tabl_id}={id}"
        with db.con.cursor() as cur:
            cur.execute(sql, (data))
        db.con.commit()
        db.con.close()

    def model_delete(self, tabl_id, id):
        sql = f"DELETE FROM {self.table} WHERE {tabl_id}={id}"
        with db.con.cursor() as cur:
            try:
                cur.execute(sql)
                print("Успешное удаление!")
                db.con.commit()
                db.con.close()
            except:
                print("Что то пошло не так!")
