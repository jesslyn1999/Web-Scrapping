from pymongo import MongoClient
import os


mongodb_uri = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/')
mongodb_db = "crawler_db"
mongodb_request_collection = "crawler_request"
mongodb_result_collection = "crawler_result"

client = MongoClient(mongodb_uri)
db = client[mongodb_db]
crawl_result_collection = db[mongodb_result_collection]
crawl_request_collection = db[mongodb_request_collection]
