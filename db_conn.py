from pymongo import MongoClient

conn = MongoClient(
    'mongodb+srv://admin:admin@cluster0.t6wkj.mongodb.net/tweets?retryWrites=true&w=majority')

db = conn.tweets
raw_data_collection = db.raw_data
clean_data_collection = db.clean_data
processed_data_collection = db.processed_data
