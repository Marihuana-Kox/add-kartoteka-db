from connect_db import CRUDDB

db = CRUDDB('localhost', 'root', 'root', 'kartoteka_klientov')


class Model:

    def __init__(self, data, table, colum_list):
        self.data = data
        self.table = table
        self.colum_list = colum_list
        self.col = len(self.data)
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

    def model_insert(self):
        columns = ", ".join([row  for row in self.colum_list])
        rows = ", ".join(['%s' for i in range(self.col)])
        sql = f"INSERT INTO {self.table} ({columns}) VALUES ({rows})" 
        self.curs.execute(sql, (self.data))
        db.con.commit()
        db.con.close()

    def model_update(self, tabl_id, id):
        columns = ", ".join([row + '=%s'  for row in self.colum_list])
        sql = f"UPDATE {self.table} SET {columns} WHERE {tabl_id}={id}"
        self.curs.execute(sql, (self.data))
        db.con.commit()
        db.con.close()

    def model_delete(self, tabl_id, id):
        sql = f"DELETE FROM {self.table} WHERE {tabl_id}={id}"
        self.curs.execute(sql)
        db.con.commit()
        db.con.close()