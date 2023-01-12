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


#Index

def add_index(index: Index):
     stats.insert_one(
            {"name": index.name , "full_name" : index.full_name ,"price": index.price, "date": index.date, "time": index.time})

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


def does_index_exist(index_name) -> bool:
    index_stats = tuple(stats.find({"name": index_name}).clone())
    if (len(index_stats) > 0):
        return True
    else:
        return False

#Participant

def find_participant(sender) -> bool:
    participant = tuple(participants.find({"username": sender}).clone())
    if (len(participant) > 0):
        return True
    else:
        return False

def does_participant_have_position_for_index(sender, index_name) -> bool:
    participant_position = tuple(participants.find({"username": sender, f"positions.{index_name}": {"$exists": True}}).clone())
    if (len(participant_position) > 0):
        return True
    else:
        return False

def add_participant(name, funds):
    try:
        participants.insert_one({"username": name, "funds": funds, "positions":{"xci": {"Long": {"shares": 0, "buyIn": {"purchased": 0, "amount_spent": 0}}, "Short": {"shares": 0, "buyIn": {"purchased": 0, "amount_spent": 0}}}}, "trades": {"total": 0, "tradeDetails": []}})  # TODO: move schema to service layer
    except Exception as error:
        print('Cause{}'.format(error))


def update_participant_position(sender, index_name, position:Position, participant:Participant, trades):

    participants.update_one({"username": sender}, {"$set": {
                f"positions.{index_name}": {"Short": {"shares": position.short_shares, "buyIn": {"purchased": position.short_shares, "amount_spent": position.short_amount_spent}}, "Long": {"shares": position.long_shares, "buyIn": {"purchased": position.long_shares, "amount_spent": position.long_amount_spent}}}, "funds": participant.funds, "trades": {"total": participant.number_of_trades, "tradeDetails": trades}}})
    return

def add_index_to_participant_positions(sender, index_name):
    participants.update_one({"username": sender}, {"$set": {
                f"positions.{index_name}": {"Short": {"shares": 0, "buyIn": {"purchased": 0, "amount_spent": 0}}, "Long": {"shares": 0, "buyIn": {"purchased": 0, "amount_spent": 0}}}}})

    return

def add_trade_to_participant_trades(sender, trade: TradeDetails):
    trades = list(get_participant_trades_details(sender))
    trades.append({"action": trade.action, "direction": trade.direction, "amount": trade.amount, "index_price": trade.index_price,
                "index_name": trade.index_name,"date": trade.date, "time": trade.time})
    return trades

def get_participant(sender):
    return participants.find({"username": sender})[0]


def get_participant_index_position_info(sender):

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


def get_all_participants_names():
    all_participants= list(participants.find())
    all_participants_names = []

    for participant in all_participants:
        name = participant['username']
        all_participants_names.append(name)
    return all_participants_names

def get_participant_all_positions_names(sender):
    positions_index_names = list(get_participant(sender)['positions'])
    return positions_index_names

def get_participant_all_positions(sender):
    positions_index_names = list(get_participant(sender)['positions'])
    positions = []
    for index_name in positions_index_names:
        index = get_latest_index(index_name)
        position = get_participant_position_info(sender, index_name)
        positions.append(position)

    return positions

def get_participant_position_info(sender, index_name):

    long_amount_spent = get_participant_long_amount_spent(sender, index_name)
    short_amount_spent = get_participant_short_amount_spent(sender, index_name)
    long_purchased = get_participant_long_purchased(sender, index_name)
    short_purchased = get_participant_short_purchased(sender, index_name)
    long_shares = get_participant_long_shares(sender, index_name)
    short_shares = get_participant_short_shares(sender, index_name)

    participant_position_info = Position(
        long_amount_spent, short_amount_spent, long_purchased, short_purchased, long_shares, short_shares)

    return participant_position_info

def get_participant_long_amount_spent(sender, index_name):
    return get_participant(sender)['positions'][index_name]['Long']['buyIn']['amount_spent']

def get_participant_short_amount_spent(sender, index_name):
    return get_participant(sender)['positions'][index_name]['Short']['buyIn']['amount_spent']

def get_participant_long_purchased(sender, index_name):
    return get_participant(sender)['positions'][index_name]['Long']['buyIn']['purchased']

def get_participant_short_purchased(sender,index_name):
    return get_participant(sender)['positions'][index_name]['Short']['buyIn']['purchased']

def get_participant_long_shares(sender, index_name):
    return get_participant(sender)['positions'][index_name]['Long']['shares']

def get_participant_short_shares(sender, index_name):
    return get_participant(sender)['positions'][index_name]['Short']['shares']

def get_participant_funds(sender):
    return get_participant(sender)['funds']

def get_participants_trades_total(sender):
    return get_participant(sender)['trades']['total']

def get_participant_trades_details(sender):
    return get_participant(sender)['trades']['tradeDetails']

def get_participant_positions(sender):
    return get_participant(sender)['positions']

def get_participant_username(sender):
    return get_participant(sender)['username']

#Composition

def get_index_composition(index_name):
    index_composition = list(composition.find({"name": index_name})[0]['composition'])
    print(str(index_composition[0]))
    return index_composition

def does_index_composition_exist(index_name):
    index = list(composition.find({"name": index_name}).clone())
    print(index)
    if (len(index) > 0):
        return True
    else:
        return False


#schema update
def update_index_time_format():
    all_indexes_stats = list(stats.find())

    for index in all_indexes_stats:
        id = index["_id"]
        date = index["date"]

        parsed_date = date.split("/")
        month = parsed_date[0]
        day = parsed_date[1]
        year = parsed_date[2]

        print (parsed_date)

        formatted_date = year + "-" + month + "-" + day

        print(formatted_date)

        stats.update_one({"_id": id}, {"$set": {"date": formatted_date}})
