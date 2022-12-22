import controller
from models import *
import math
import re
from datetime import datetime


def open(sender, message):
    wager = 0
    position = ''



    try:
        wager, position = validate_extract_open_message(message)
    except ValueError as error:
        if str(error) == 'Please enter a positive number':
            return 'Please enter a positive number'
        else:
            return 'Please enter valid command. eg: /open long 500'



    current_index_price = controller.get_latest_xci().price

    #create_position(message, participant, current_index)
    funds = controller.get_participant_funds(sender)
    trades = controller.get_participant_trades_details(sender)
    if wager == "max":
        wager = funds - 1e-09
    if wager > funds:
        raise ValueError('More than you have in your account')

    purchased = wager / current_index_price

    date, time = get_current_date_time()
    print(date, time)
    if position == "short":
        trades = controller.append_trade_to_participant(sender, position, wager, date, time)
        controller.update_participant_cash_out_short(sender, purchased, wager, funds, trades)
        return 'Short position has been opened!'
    if position == "long":
        trades = controller.append_trade_to_participant(sender, position, wager, date, time)
        controller.update_participant_cash_out_long(
        sender, purchased, wager, funds, trades)
        return 'Long position has been opened!'


def create_position(message,participant:Participant, index: Index):

    try:
        wager, position = validate_extract_open_message(message)
    except ValueError as error:
        if str(error) == 'Please enter a positive number':
            return 'Please enter a positive number'
        else:
            return 'Please enter valid command. eg: /open long 500'



    return #updated participant


def validate_extract_open_message(message): #might need to split up in two functions validate / extract
    parsed_message = split_message(message)

    if len(parsed_message) < 3:
        raise ValueError()
    elif parsed_message[2] == None or parsed_message[1] == None or len(parsed_message) > 3:
        raise ValueError()
    elif parsed_message[2] == "max":
        position = parsed_message[1]
        wager = "max"
    else:
        if float(parsed_message[2]) < 0:
            raise ValueError('Please enter a positive number')
        position = parsed_message[1]
        wager = float(parsed_message[2])

    return wager, position

def split_message(message):
    parsed_message = re.split("\s", message)
    return parsed_message

def calculate_average_buy_price(amount_spent, purchased):
    avg_buy_price = amount_spent / purchased
    return avg_buy_price


def calculate_long_position(shares, avg_buy_price, index_price):
    long = (shares * avg_buy_price) + ((index_price - avg_buy_price) * shares)
    return long

def calculate_short_position(shares, avg_buy_price, index_price):
    short = (shares * avg_buy_price) + ((avg_buy_price - index_price) * shares)
    return short

def get_current_date_time():
    now = datetime.now()
    date = now.strftime('%m/%d/%Y')
    time = now.strftime("%H:%M:%S")
    return date, time