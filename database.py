import math
from telegram import *
from telegram.ext import *
import requests
import re
import os
from dotenv import load_dotenv
import configparser
import requests
from datetime import datetime
from pymongo import MongoClient
from models import Index


load_dotenv()


PASSWORD = os.environ['password']
USERNAME = os.environ['username']
BOT_TOKEN = os.environ['bot_token']
API = os.environ['api']
CHAT = os.environ['chat']
DATABASE_NAME = os.environ['db_name']
COLLECTION_NAME1 = os.environ['collection_name1']
COLLECTION_NAME2 = os.environ['collection_name2']
URL = os.environ['db_url']

cluster = MongoClient(URL)
db = cluster[DATABASE_NAME]
stats = db[COLLECTION_NAME2]
participants = db[COLLECTION_NAME1]


def get_database():
    return db

def get_stats_collection():
    return stats

def get_participants_collection():
    return participants

#TODO:This function can be generalized - get_latest_index with a parameter.
def get_latest_xci_price():
    latest_xci_info = stats.find().sort("_id", -1)[0] #WARNING: This is hardcoded to get first element
    price = round(latest_xci_info["price"], 2)
    date = latest_xci_info["date"]
    time = latest_xci_info["time"]
    xci_index = Index(price, date, time)
    return  xci_index

def find_participant(sender):
    participant = tuple(participants.find({"username": sender}).clone)
    if(len(participant) > 0):
        return True
    else:
        return False



def create_participant():
    return