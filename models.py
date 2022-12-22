from connect_db import CRUDDB

from main import add_list_exel as add

db = CRUDDB('localhost', 'root', 'root', 'kartoteka_klientov')

db.chench_connect_db()
# db.insert_data('insert')

db.insert_data_by(add)
# print(db.chench_connect_db)