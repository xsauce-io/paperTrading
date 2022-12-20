from telegram import *
from telegram.ext import *
import os
from dotenv import load_dotenv
from datetime import datetime
import pymongo
from pymongo import MongoClient, DESCENDING , InsertOne
from models import Index, Position


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

#TODO:This function can be generalized - get_latest_index with a parameter break down to get latest price , data and time => put together in service layer.
def get_latest_xci_info():
    latest_xci_info = stats.find().sort("_id", DESCENDING)[0] #WARNING: This is hardcoded to get first element
    price = round(latest_xci_info["price"], 2) #TODO: rm rounding and put in service layer
    date = latest_xci_info["date"]
    time = latest_xci_info["time"]
    xci_index = Index(price, date, time)
    return  xci_index

def find_participant(sender):
    participant = tuple(participants.find({"username": sender}).clone())
    if(len(participant) > 0):
        return True
    else:
        return False

def create_participant(sender):
    try:
        participants.insert_one(
                {"username": sender, "funds": 10000, "position": {"Long": {"shares": 0, "buyIn": {"purchased": 0, "amount_spent": 0}}, "Short": {"shares": 0, "buyIn": {"purchased": 0, "amount_spent": 0}}}, "trades": {"total": 0, "tradeDetails": []}})  #TODO: move schema to service layer
    except Exception as error:
        print('Cause{}'.format(error))

def get_participant(sender):
    return participants.find({"username": sender})[0]

def get_participant_position_info(sender):

    long_amount_spent = get_participant_long_amount_spent(sender)
    short_amount_spent = get_participant_short_amount_spent(sender)
    long_purchased = get_participant_long_purchased(sender)
    short_purchased = get_participant_short_purchased(sender)
    long_shares = get_participant_long_shares(sender)
    short_shares = get_participant_short_shares(sender)
    funds = get_participant_funds(sender)

    participant_position_info = Position(long_amount_spent, short_amount_spent, long_purchased, short_purchased, long_shares, short_shares, funds)

    return participant_position_info

def get_participant_long_amount_spent(sender):
    return get_participant(sender)['position']['Long']['buyIn']['amount_spent']

def get_participant_short_amount_spent(sender):
    return get_participant(sender)['position']['Short']['buyIn']['amount_spent']

def get_participant_long_purchased(sender):
    return get_participant(sender)['position']['Long']['buyIn']['purchased']

def get_participant_short_purchased(sender):
    return get_participant(sender)['position']['Short']['buyIn']['purchased']

def get_participant_long_shares(sender):
    return get_participant(sender)['position']['Long']['shares']

def get_participant_short_shares(sender):
    return get_participant(sender)['position']['Short']['shares']

def get_participant_funds(sender):
    return get_participant(sender)['funds']

def get_participants_trades_total(sender):
    return get_participant(sender)['trades']['total']

def get_participant_trades_details(sender):
    return get_participant(sender)['trades']['tradeDetails']

def append_trade_to_participant(sender, position, wager, date, time ):
    print("here")
    trades = get_participant_trades_details(sender)
    print(trades)
    here = trades.append({"direction": position, "amount": wager, "date": date, "time": time}) #TODO: move schema to service layer
    print(trades)
    return