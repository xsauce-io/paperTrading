import controller
from models import *
import math
import re
from datetime import datetime
from helpers.market_math import *
from helpers.utils import *


def close(sender, message):
    parsed_message = split_message(message)
    index_name = parsed_message[1]

    try:
        if is_close_message_valid(parsed_message) == False:
            raise UserInputException('Please enter valid command. eg: /close xci long 500')
        if controller.find_index(index_name) == False:
            raise "Index {} Not Found".format(index_name)
        if controller.find_participant_position(sender, index_name) == False:
            raise ValueError('You have no positions open')
    except UserInputException as error:
        return str(error)

    current_index=controller.get_latest_index(index_name)
    current_position_info = controller.get_participant_position_info(sender, index_name)
    print(repr(current_position_info))
    current_participant_info = controller.get_participant_info(sender)
    try:
        updated_position, updated_participant, new_trade = close_position(message, current_position_info, current_participant_info, current_index)
        updated_trades = controller.append_trade_to_participant_trades(sender, new_trade)
        controller.update_participant_position(sender, index_name, updated_position, updated_participant, updated_trades)
    except UserInputException as error:
        return str(error)
    #except ZeroDivisionError as error:

    return '{} position has been closed!'.format(new_trade.direction)

def close_position(message, position:Position, participant:Participant, index: Index):
    updated_position = None
    updated_participant = None
    reset_position = False

    try:
        reduction, direction = extract_close_message(message)
    except Exception as error:
        raise error

    try:
        if direction == "long":
            if reduction == "max":
                reduction = position.long_shares - 1e-09
                reset_position = True
            print({position.long_shares, reduction})

            has_required_shares(position.long_shares, reduction)
            has_required_shares(position.long_purchased, reduction)

            avg_buy_price_long = position.long_amount_spent / position.long_purchased
            wager = avg_buy_price_long * reduction
            long_value_by_share = calculate_long_position(position.long_shares, avg_buy_price_long, index.price) / position.long_shares
            cash_out = reduction * long_value_by_share

            funds = rounder(participant.funds + cash_out)
            number_of_trades = participant.number_of_trades + 1

            date, time = get_current_date_time()

            if (reset_position):
                updated_position = Position(0, position.short_amount_spent, 0, position.short_purchased, 0, position.short_shares)
            else:
                updated_position = Position(rounder(position.long_amount_spent - wager), rounder(position.short_amount_spent), rounder(position.long_purchased - reduction), position.short_purchased, rounder(position.long_shares-reduction), position.short_shares)

            updated_participant = Participant(participant.name, funds, number_of_trades)
            new_trade = TradeDetails(direction, amount=reduction, action="sell", index_price=index.price, index_name=None, date=date, time=time)

        if direction == "short":
            if reduction == "max":
                reduction = rounder(position.short_shares)
                reset_position = True

            has_required_shares(position.short_shares, reduction)
            has_required_shares(position.short_purchased, reduction)

            avg_buy_price_short = calculate_average_buy_price(
                position.short_amount_spent, position.short_purchased)
            wager = avg_buy_price_short * reduction
            short_value_by_share = calculate_short_position(
                position.short_shares, avg_buy_price_short, index.price) / position.short_shares
            cash_out = reduction * short_value_by_share

            funds = rounder(participant.funds + cash_out)
            number_of_trades = participant.number_of_trades + 1

            date, time = get_current_date_time()

            if (reset_position):
                updated_position = Position(position.long_amount_spent,0, position.long_purchased, 0, position.long_shares, 0)
            else:
                updated_position = Position(position.long_amount_spent, rounder(position.short_amount_spent - wager), position.long_purchased , rounder(position.short_purchased - reduction), position.long_shares, rounder(position.short_shares - reduction))

            updated_participant = Participant(participant.name, funds, number_of_trades)
            new_trade = TradeDetails(direction, amount=reduction, action="sell", index_price=index.price, index_name=None, date=date, time=time)

    except Exception as error:
        raise error

    return updated_position, updated_participant, new_trade

def extract_close_message(close):
    parsed_message = split_message(close)

    if is_close_message_valid(parsed_message) == False:
        raise UserInputException('Please enter valid command. eg: /open long 500')

    if  parsed_message[3] == "max":
        direction =  parsed_message[2]
        reduction = "max"
    else:
        if float(parsed_message[3]) < 0:
            raise ValueError('Please enter a positive number')
        direction =  parsed_message[2]
        reduction = float( parsed_message[3])

    return reduction, direction


def is_close_message_valid(parsed_message: list):
    if len(parsed_message) == 4:
       if parsed_message[2] == "short" or parsed_message[2] == "long":
            if is_float(parsed_message[3]):
                return True
            else:
                if parsed_message[3] == "max":
                    return True
    return False

def has_required_shares(shares, reduction):
    if shares == 0:
        raise ValueError('You have no positions')

    if math.isclose(shares, reduction) == False and reduction > shares:
        raise ValueError('More than you have in your account')
