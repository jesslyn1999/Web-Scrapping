from pymongo import MongoClient
import os


mongodb_uri = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/')
print("mongodb server: ", mongodb_uri)
client = MongoClient(mongodb_uri)
db = client.crawler_db

crawl_result_collection = db.crawl_result
