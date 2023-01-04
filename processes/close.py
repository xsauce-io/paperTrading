import controller
from models import *
import math
import re
from datetime import datetime
from helpers.market_math import *
from helpers.utils import *


def close(sender, message):
    parsed_message = split_message(message)

    if is_close_message_format_valid(parsed_message) == False:
        raise UserInputException('Please enter valid command. eg: /close xci long 10')
    if is_close_message_input_valid(parsed_message) == False:
        raise UserInputException('Please enter valid command. eg: /close xci long 10')

    index_name, reduction, direction = extract_close_message(parsed_message)

    if controller.does_index_exist(index_name) == False:
       raise UserInputException("Index {} Not Found".format(index_name))
    if controller.does_participant_have_position_for_index(sender, index_name) == False:
        raise UserInputException('You have no positions open')

    current_index=controller.get_latest_index(index_name)
    current_position_info = controller.get_participant_position_info(sender, index_name)
    current_participant_info = controller.get_participant_info(sender)

    updated_position, updated_participant, new_trade = determine_closed_position_update(reduction, direction, current_position_info, current_participant_info, current_index)
    updated_trades = controller.append_trade_to_participant_trades(sender, new_trade)
    controller.update_participant_position(sender, index_name, updated_position, updated_participant, updated_trades)

    return '{} position has been closed!'.format(new_trade.direction)

def determine_closed_position_update(reduction, direction, position:Position, participant:Participant, index: Index):
    updated_position = None
    updated_participant = None
    reset_position = False
    new_trade = None


    if direction == "long":
            if reduction == "max":
                reduction = position.long_shares - 1e-09
                reset_position = True

            has_required_shares(position.long_shares, reduction)
            has_required_shares(position.long_purchased, reduction)

            avg_buy_price_long = position.long_amount_spent / position.long_purchased
            wager = avg_buy_price_long * reduction
            long_value_by_share = calculate_long_position(position.long_shares, avg_buy_price_long, index.price) / position.long_shares
            cash_out = reduction * long_value_by_share

            funds = participant.funds + cash_out
            number_of_trades = participant.number_of_trades + 1

            date, time = get_current_date_time()

            if (reset_position):
                updated_position = Position(0, position.short_amount_spent, 0, position.short_purchased, 0, position.short_shares)
            else:
                updated_position = Position(position.long_amount_spent - wager, position.short_amount_spent, position.long_purchased - reduction, position.short_purchased, position.long_shares-reduction, position.short_shares)

            updated_participant = Participant(participant.name, funds, number_of_trades)
            new_trade = TradeDetails(direction, amount=reduction, action="sell", index_price=index.price, index_name=index.name, date=date, time=time)

    if direction == "short":
            if reduction == "max":
                reduction = position.short_shares - 1e-09
                reset_position = True

            has_required_shares(position.short_shares, reduction)
            has_required_shares(position.short_purchased, reduction)

            avg_buy_price_short = calculate_average_buy_price(
                position.short_amount_spent, position.short_purchased)
            wager = avg_buy_price_short * reduction
            short_value_by_share = calculate_short_position(
                position.short_shares, avg_buy_price_short, index.price) / position.short_shares
            cash_out = reduction * short_value_by_share

            funds = participant.funds + cash_out
            number_of_trades = participant.number_of_trades + 1

            date, time = get_current_date_time()

            if (reset_position):
                updated_position = Position(position.long_amount_spent,0, position.long_purchased, 0, position.long_shares, 0)
            else:
                updated_position = Position(position.long_amount_spent, position.short_amount_spent - wager, position.long_purchased , position.short_purchased - reduction, position.long_shares, position.short_shares - reduction)

            updated_participant = Participant(participant.name, funds, number_of_trades)
            new_trade = TradeDetails(direction, amount=reduction, action="sell", index_price=index.price, index_name=None, date=date, time=time)


    return updated_position, updated_participant, new_trade

def extract_close_message(parsed_message):
    index_name = parsed_message[1]
    direction = parsed_message[2]
    reduction = parsed_message[3]

    if reduction == "max":
        reduction = "max"
    else:
        reduction = float(parsed_message[3])

    return index_name, reduction, direction


def is_close_message_input_valid(parsed_message: list):
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

def is_close_message_format_valid(parsed_message: list):
    if len(parsed_message) == 4:
       return True
    return False

def has_required_shares(shares, reduction):
    if shares == 0:
        raise UserInputException('You have no positions')

    if math.isclose(shares, reduction) == False and reduction > shares:
        raise UserInputException('More than you have in your account')
