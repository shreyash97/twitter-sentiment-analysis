import db_conn

db = db_conn.db

db.raw_data.delete_many({})
db.clean_data.delete_many({})
db.processed_data.delete_many({})
