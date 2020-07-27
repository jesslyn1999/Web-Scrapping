from pymongo import MongoClient
import os


mongodb_uri = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/')
mongodb_db = "crawler_db"
mongodb_request_collection = "crawler_request"

client = MongoClient(mongodb_uri)
db = client[mongodb_db]
crawl_request_collection = db[mongodb_request_collection]
