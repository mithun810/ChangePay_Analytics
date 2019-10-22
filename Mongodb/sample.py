from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint
import pymongo
import json
# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
client = MongoClient("localhost:27017")
db=client.CHANGEPAY
# mycollection = db["TRANSACTIONS"]
print(db.TRANSACTIONS.find_one())
# for p in db.TRANSACTIONS.find():
#     print(p)

# pprint(db)

import pymongo
import json

if __name__ == '__main__':
    client = pymongo.MongoClient("localhost", 27017, maxPoolSize=50)
    d = dict((db, [collection for collection in client[db].collection_names()])
             for db in client.database_names())
    print json.dumps(d)