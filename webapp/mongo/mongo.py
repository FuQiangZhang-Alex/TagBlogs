import pymongo


class MongoTool:

    def __init__(self, host='localhost:27017'):
        self.host = host
        self.client = pymongo.MongoClient(self.host)

    def get_dbs(self):
        return self.client.database_names()

    def get_db(self, db_name):
        return self.client[db_name]
