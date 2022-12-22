import controller
from models import *
import re
from datetime import datetime

def open(sender, message):
    current_index= controller.get_latest_xci()
    current_position_info = controller.get_participant_position_info(sender)
    current_participant_info = controller.get_participant_info(sender)
    try:
        updated_position, updated_participant, new_trade = update_position(message, current_position_info, current_participant_info, current_index)
        update_trades = controller.append_trade_to_participant_trades(sender, new_trade)
        controller.update_participant_opened_position(sender, updated_position, updated_participant, update_trades)
    except UserInputException as error:
        return str(error)
    return '{} position has been opened!'.format(new_trade.direction)


def update_position(message, position: Position, participant: Participant, index: Index):
    updated_position = None
    updated_participant = None

    #extract in
    try:
        wager, direction = validate_extract_open_message(message)
    except Exception as error:
            raise error

    if wager == "max":
        wager = participant.funds - 1e-09
    if wager > participant.funds:
        raise UserInputException('More than you have in your account')


    purchased = wager / index.price
    funds = participant.funds - wager
    number_of_trades = participant.number_of_trades + 1
    date, time = get_current_date_time()

    try:
        if direction == "long":
            print("updating_long_position")
            updated_position = Position(position.long_amount_spent + wager, position.short_amount_spent , position.long_purchased + purchased, position.short_purchased, position.long_shares + purchased, position.short_shares )
        if direction == "short":
            print("updating__short_position")
            updated_position = Position(position.long_amount_spent, position.short_amount_spent + wager , position.long_purchased, position.short_purchased + purchased, position.long_shares, position.short_shares + purchased )
        updated_participant = Participant(participant.name, funds, number_of_trades)
        new_trade = TradeDetails(direction, amount=wager, action="buy", index_price=index.price, index_name=None, date=date, time=time)
    except Exception as error:
        raise error

    return updated_position, updated_participant, new_trade


def validate_extract_open_message(message): #might need to split up in two functions validate / extract
    parsed_message = split_message(message)

    if len(parsed_message) < 3:
        raise UserInputException('Please enter valid command. eg: /open long 500')
    elif parsed_message[2] == None or parsed_message[1] == None or len(parsed_message) > 3:
        raise UserInputException('Please enter valid command. eg: /open long 500')
    if parsed_message[1] != "short" and parsed_message[1] != "long":
        raise UserInputException('Please enter valid command. eg: /open long 500')
    elif parsed_message[2] == "max":
        direction = parsed_message[1]
        wager = "max"
    else:
        if float(parsed_message[2]) < 0:
            raise UserInputException('Please enter a positive number')
        direction = parsed_message[1]
        wager = float(parsed_message[2])

    return wager, direction

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