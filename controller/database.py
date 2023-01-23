import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

PASSWORD = os.environ['password']
USERNAME = os.environ['username']
BOT_TOKEN = os.environ['bot_token']
API = os.environ['api']
CHAT = os.environ['chat']
DATABASE_NAME = os.environ['db_name']
COLLECTION_NAME1 = os.environ['collection_name1']
COLLECTION_NAME2 = os.environ['collection_name2']
COLLECTION_NAME3 = os.environ['collection_name3']
COLLECTION_NAME4 = os.environ['collection_name4']
COLLECTION_NAME5 = os.environ['collection_name5']
URL = os.environ['db_url']

cluster = MongoClient(URL)
db = cluster[DATABASE_NAME]
participants = db[COLLECTION_NAME1]
stats = db[COLLECTION_NAME2]
composition = db[COLLECTION_NAME3]
trackers = db[COLLECTION_NAME4]
asset_statistics = db[COLLECTION_NAME5]