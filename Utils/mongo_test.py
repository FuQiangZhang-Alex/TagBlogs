from pymongo import MongoClient


mongo_client = MongoClient('mongodb://localhost:27000/')
db = mongo_client.TagBlogs
collection = db.BlogEntry
rs = list(collection.find(filter={ 'author_url': { '$ne': ''}}, limit=10))
print(rs)
