from telegram import *
from telegram.ext import *
import os
from dotenv import load_dotenv
from datetime import datetime
import pymongo
from pymongo import MongoClient, DESCENDING, InsertOne
from models import *
import json

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
URL = os.environ['db_url']

cluster = MongoClient(URL)
db = cluster[DATABASE_NAME]
participants = db[COLLECTION_NAME1]
stats = db[COLLECTION_NAME2]
composition = db[COLLECTION_NAME3]


# TODO:This function can be generalized - get_latest_index with a parameter break down to get latest price , data and time => put together in service layer.
def get_latest_index(index_name):
    # WARNING: This is hardcoded to get first element
    latest_index = stats.find({"name": index_name}).sort("_id", DESCENDING)[0]

    name = latest_index["name"]
    full_name = latest_index["full_name"]
    price = latest_index["price"]
    date = latest_index["date"]
    time = latest_index["time"]

    index = Index(name, full_name ,price, date, time)
    return index

def find_index(index_name) -> bool:
    index_stats = tuple(stats.find({"name": index_name}).clone())
    if (len(index_stats) > 0):
        return True
    else:
        return False

def find_participant(sender) -> bool:
    participant = tuple(participants.find({"username": sender}).clone())
    if (len(participant) > 0):
        return True
    else:
        return False

# def add_participant(name, funds):
#     try:
#         participants.insert_one({"username": name, "funds": funds, "position": {"Long": {"shares": 0, "buyIn": {"purchased": 0, "amount_spent": 0}}, "Short": {"shares": 0, "buyIn": {"purchased": 0, "amount_spent": 0}}}, "trades": {"total": 0, "tradeDetails": []}})  # TODO: move schema to service layer
#     except Exception as error:
#         print('Cause{}'.format(error))

def add_participant(name, funds):
    try:
        participants.insert_one({"username": name, "funds": funds, "positions":[{"xci": {"Long": {"shares": 0, "buyIn": {"purchased": 0, "amount_spent": 0}}, "Short": {"shares": 0, "buyIn": {"purchased": 0, "amount_spent": 0}}}}], "trades": {"total": 0, "tradeDetails": []}})  # TODO: move schema to service layer
    except Exception as error:
        print('Cause{}'.format(error))

def add_index(index: Index):
     stats.insert_one(
            {"name": index.name , "full_name" : index.full_name ,"price": index.price, "date": index.date, "time": index.time})


def get_participant(sender):
    return participants.find({"username": sender})[0]


def get_participant_position_info(sender):

    long_amount_spent = get_participant_long_amount_spent(sender)
    short_amount_spent = get_participant_short_amount_spent(sender)
    long_purchased = get_participant_long_purchased(sender)
    short_purchased = get_participant_short_purchased(sender)
    long_shares = get_participant_long_shares(sender)
    short_shares = get_participant_short_shares(sender)

    participant_position_info = Position(
        long_amount_spent, short_amount_spent, long_purchased, short_purchased, long_shares, short_shares)

    return participant_position_info

def get_participant_info(sender):
    username = get_participant_username(sender)
    funds = get_participant_funds(sender)
    number_of_trades = get_participants_trades_total(sender)

    participant = Participant(username, funds, number_of_trades)
    return participant

def append_trade_to_participant_trades(sender, trade: TradeDetails):
    trades = list(get_participant_trades_details(sender))
    trades.append({"direction": trade.direction, "amount": trade.amount,
                  "date": trade.date, "time": trade.time})
    return trades

def update_participant_position(sender , position:Position, participant:Participant, trades):
    participants.update_one({"username": sender}, {"$set": {
                "position": {"Short": {"shares": position.short_shares, "buyIn": {"purchased": position.short_shares, "amount_spent": position.short_amount_spent}}, "Long": {"shares": position.long_shares, "buyIn": {"purchased": position.long_shares, "amount_spent": position.long_amount_spent}}}, "funds": participant.funds, "trades": {"total": participant.number_of_trades, "tradeDetails": trades}}})
    return


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

def get_participant_positions(sender):
    return get_participant(sender)['position']

def get_participant_username(sender):
    return get_participant(sender)['username']
