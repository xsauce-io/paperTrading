import controller
from models import *
import math
import re
from datetime import datetime


def open(sender, message):
    wager = 0
    position = ''
    try:
        wager, position = get_info_from_open_close_command(message)
    except ValueError as error:
        if str(error) == 'Please enter a positive number':
            return 'Please enter a positive number'
        else:
            return 'Please enter valid command. eg: /open long 500'

    current_index_price = controller.get_latest_xci().price
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


def get_current_date_time():
    now = datetime.now()
    date = now.strftime('%m/%d/%Y')
    time = now.strftime("%H:%M:%S")
    return date, time


def parse_open_close_command(message):
    parsed_message = re.split("\s", message)
    return parsed_message


def get_info_from_open_close_command(command):
    parsed_command = parse_open_close_command(command)

    if len(parsed_command) < 3:
        raise ValueError()
    elif parsed_command[2] == None or parsed_command[1] == None or len(parsed_command) > 3:
        raise ValueError()
    elif parsed_command[2] == "max":
        position = parsed_command[1]
        wager = "max"
    else:
        if float(parsed_command[2]) < 0:
            raise ValueError('Please enter a positive number')
        position = parsed_command[1]
        wager = float(parsed_command[2])

    return wager, position


def calculate_average_buy_price(amount_spent, purchased):
    avg_buy_price = amount_spent / purchased
    return avg_buy_price


def calculate_long_position(shares, avg_buy_price, index_price):
    long = (shares * avg_buy_price) + ((index_price - avg_buy_price) * shares)
    return long


def calculate_short_position(shares, avg_buy_price, index_price):
    short = (shares * avg_buy_price) + ((avg_buy_price - index_price) * shares)
    return short
