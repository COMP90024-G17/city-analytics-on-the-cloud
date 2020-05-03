import os
import json
import db_util

COUCHDB_URL = 'http://{}:{}@{}:{}/'
COUCHDB_DOMAIN = '172.26.130.149'
COUCHDB_USERNAME = 'admin'
COUCHDB_PASSWORD = 'admin1234'
COUCHDB_PORTS = 5984
DBNAME = 'aurin'

db = db_util.cdb(COUCHDB_URL.format(COUCHDB_USERNAME,COUCHDB_PASSWORD,COUCHDB_DOMAIN,COUCHDB_PORTS), DBNAME)

db.showcurrentDB()

dirpath = './aurin_data/'
for filename in os.listdir(dirpath):
    content = open(os.path.join(dirpath,filename),'r')
    data = json.load(content)
    _id = filename[:-5]
    if filename.endswith('_suburbs.json'):
        db.put(data,_id)
    else:
        data_toload = {}
        data_toload["_id"] = _id
        data_toload["suburbs"] = {}
        i = 1
        for item in data['features']:
            suburbname = item['properties']['sa2_name16']
            suburbdata = item['properties']
            del suburbdata['sa2_name16']

            data_toload['suburbs'][suburbname] = suburbdata
        db.put(data_toload,_id)