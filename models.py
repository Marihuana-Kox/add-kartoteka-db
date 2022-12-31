from connect_db import CRUDDB
import pymysql
db = CRUDDB('localhost', 'root', 'root', 'kartoteka_klientov')


class Model:

    def __init__(self, table, colum_list):
        self.table = table
        self.colum_list = colum_list
        self.curs = db.con.cursor()

    def model_select(self):
        self.curs.execute(f"SELECT * FROM {self.table}")
        db_date = self.curs.fetchall()
        return db_date

    def model_select_by(self, tabl_id, id):
        self.curs.execute(f"SELECT * FROM {self.table} WHERE {tabl_id}={id}")
        db_date_by = self.curs.fetchall()
        db.con.close()
        return db_date_by

    def model_insert(self, data):
        columns = ", ".join([row for row in self.colum_list])
        rows = ", ".join(['%s' for i in range(len(data))])
        sql = f"INSERT INTO {self.table} ({columns}) VALUES ({rows})"
        try:
            self.curs.execute(sql, (data))
            print("Запись успешно создана")
        except pymysql.err.IntegrityError:
            print("Такая запись, уже есть в БД")
        db.con.commit()
        db.con.close()

    def model_insert_noduble(self, data, q, match ,tabl_id, id):
        """Игнорирует добавление дублирующих записей"""
        self.curs.execute(f"SELECT * FROM {self.table} WHERE {tabl_id}={id}")
        duble = self.curs.fetchall()
        if len(duble) != 0:
            mtlist = []
            for el in duble:
                mtlist.append(el[match])
            if data[q] in mtlist:
                print(f"Запись: {data[q]} уже есть.")
            else:
                self.model_insert(self, data) 
        else:
            self.model_insert(self, data)

    def model_insert_tables(self, data, tabl_id, id):
        """Встявляет одновременно в несколько таблиц"""
        self.model_insert(data)
        elem = self.model_select_by(self, tabl_id, id)
        print(elem)

    def model_update(self, data, tabl_id, id):
        columns = ", ".join([row + '=%s' for row in self.colum_list])
        sql = f"UPDATE {self.table} SET {columns} WHERE {tabl_id}={id}"
        self.curs.execute(sql, (data))
        db.con.commit()
        db.con.close()

    def model_delete(self, tabl_id, id):
        sql = f"DELETE FROM {self.table} WHERE {tabl_id}={id}"
        try:
            self.curs.execute(sql)
            print("Успешное удаление!")
        except:
            print("Что то пошло не так!")
        db.con.commit()
        db.con.close()
