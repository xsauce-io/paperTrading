import controller
from models import *
from datetime import datetime

from helpers.utils import *

def open(sender, message):

    parsed_message = split_message(message)

    if is_open_message_format_valid(parsed_message) == False:
        raise UserInputException('Please enter valid command. eg: /open xci long 500')
    if is_open_message_input_valid(parsed_message) == False:
        raise UserInputException('Please enter valid command. eg: /open xci long 500')

    index_name, wager, direction = extract_open_message(parsed_message)

    if controller.does_index_exist(index_name) == False:
       raise UserInputException("Index {} Not Found".format(index_name))

    if controller.does_participant_have_position_for_index(sender, index_name) == False:
        controller.add_index_to_participant_positions(sender, index_name)


    current_index= controller.get_latest_index(index_name)
    current_position_info = controller.get_participant_position_info(sender, index_name)
    current_participant_info = controller.get_participant_info(sender)

    updated_position, updated_participant, new_trade = determine_opened_position_update(wager, direction, current_position_info, current_participant_info, current_index)
    updated_trades = controller.add_trade_to_participant_trades(sender, new_trade)
    controller.update_participant_position(sender, index_name ,updated_position, updated_participant, updated_trades)

    return '{} position has been opened!'.format(new_trade.direction)


def determine_opened_position_update(wager, direction, position: Position, participant: Participant, index: Index):
    updated_position = None
    updated_participant = None
    new_trade = None

    if wager == "max":
        wager = participant.funds
    if wager == 0:
        raise UserInputException("You can't get something for nothing")
    if participant.funds == 0:
        raise UserInputException("You're broke. Sell some shares to feed your funds")
    if wager > participant.funds:
        raise UserInputException('That cost more than you got in your bag')


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
            updated_position = Position(position.long_amount_spent, position.short_amount_spent + wager , position.long_purchased, position.short_purchased + purchased, position.long_shares,position.short_shares + purchased)
        updated_participant = Participant(participant.name, funds, number_of_trades)
        new_trade = TradeDetails(direction, amount=wager, action="buy", index_price=index.price, index_name=index.name, date=date, time=time)
    except Exception as error:
        raise error

    return updated_position, updated_participant, new_trade


def extract_open_message(parsed_message):
    index_name = parsed_message[1]
    direction = parsed_message[2]
    wager = parsed_message[3]

    if wager == "max":
        wager = "max"
    else:
        wager = float(parsed_message[3])

    return index_name, wager, direction

def is_open_message_input_valid(parsed_message: list):
    index_name = parsed_message[1]
    direction = parsed_message[2]
    wager = parsed_message[3]
    if direction == "short" or direction == "long":
            if is_float(wager):
                 if float(parsed_message[3]) > 0:
                    return True

            else:
                if wager == "max":
                    return True
    return False

def is_open_message_format_valid(parsed_message: list):
    if len(parsed_message) == 4:
       return True
    return False