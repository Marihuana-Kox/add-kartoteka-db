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
                # db.con.close()
                print("Запись успешно создана")
            except pymysql.err.IntegrityError:
                print("Такая запись, уже есть в БД")
            
    def model_insert_not_duble(self, **params):
        """Игнорирует добавление дублирующих записей"""
        with db.con.cursor() as cur:
            cur.execute(f"SELECT * FROM {self.table} WHERE {tabl_id}='{id}'")
        pass
    
    
    def model_insert_noduble(self, data, q, match ,tabl_id, id):
        """Игнорирует добавление дублирующих записей"""
        print(data)
        with db.con.cursor() as cur:
            cur.execute(f"SELECT {match} FROM {self.table} WHERE {tabl_id}='{id}'")
        duble = cur.fetchall()
        if len(duble) != 0:
            mtlist = []
            for el in duble[0]:
                mtlist.append(duble[0][match])
                
            if data[q] in mtlist:
                print(f"Запись: {data[q]} уже есть.")
            else:
                self.model_insert(self, data) 
        else:
            self.model_insert(self, data)
        

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
