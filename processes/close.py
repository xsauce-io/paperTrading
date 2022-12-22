import controller
from models import *
import math
import re
from datetime import datetime


def close(sender, message):
    reduction = 0
    position = ''
    try:
        reduction, position = get_info_from_open_close_command(message)
    except ValueError as error:
        if str(error) == 'Please enter a positive number':
            return 'Please enter a positive number'
        else:
            return 'Please enter valid command. eg: /close long 10'

    current_index_price = controller.get_latest_xci().price
    funds = controller.get_participant_funds(sender)
    trades = controller.get_participant_trades_details(sender)
    position_info = controller.get_participant_position_info(sender)
    long_amount_spent = position_info.long_amount_spent
    short_amount_spent = position_info.short_amount_spent
    long_purchased = position_info.long_purchased
    short_purchased = position_info.short_purchased
    long_shares = position_info.long_shares
    short_shares = position_info.short_shares

    date, time = get_current_date_time()

    if position == "short":

        if reduction == "max":
            reduction = set_reduction_max(short_shares)

        check_close_requirements(short_shares, reduction)

        avg_buy_price_short = calculate_average_buy_price(
            short_amount_spent, short_purchased)
        wager = avg_buy_price_short * reduction
        short_value_by_share = calculate_short_position(
            short_shares, avg_buy_price_short, current_index_price) / short_shares
        cash_out = reduction * short_value_by_share

        if (reduction != short_shares - 1e-09):
            trades.append(
                {"direction": position, "amount": reduction, "date": date, "time": time})
            controller.update_participant_close_short(
                sender, wager, reduction, funds, trades, cash_out)
        if (reduction == short_shares - 1e-09):
            trades.append(
                {"direction": position, "amount": reduction, "date": date, "time": time})
            controller.update_participant_close_short_max(
                sender, funds, trades, cash_out)

        return 'Short position has been closed!'

    if position == "long":
        if reduction == "max":
            reduction = long_shares - 1e-09

        check_close_requirements(long_shares, reduction)

        avg_buy_price_long = long_amount_spent / long_purchased
        wager = avg_buy_price_long * reduction
        long_value_by_share = calculate_long_position(
            long_shares, avg_buy_price_long, current_index_price) / long_shares
        cash_out = reduction * long_value_by_share

        if (reduction != long_shares - 1e-09):
            trades.append(
                {"direction": position, "amount": reduction, "date": date, "time": time})
            controller.update_participant_close_long(
                sender, wager, funds, reduction, trades, cash_out)
        if (reduction == long_shares - 1e-09):
            trades.append(
                {"direction": position, "amount": reduction, "date": date, "time": time})
            controller.update_participant_close_long_max(
                sender, funds, trades, cash_out)
        return ('Long position has been closed!')


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


def check_close_requirements(shares, reduction):
    if shares == 0:
        raise ValueError('You have no positions')

    if math.isclose(shares, reduction) == False and reduction > shares:
        raise ValueError('More than you have in your account')


def set_reduction_max(shares):
    reduction = shares - 1e-09
    return reduction


def calculate_average_buy_price(amount_spent, purchased):
    avg_buy_price = amount_spent / purchased
    return avg_buy_price


def calculate_long_position(shares, avg_buy_price, index_price):
    long = (shares * avg_buy_price) + ((index_price - avg_buy_price) * shares)
    return long


def calculate_short_position(shares, avg_buy_price, index_price):
    short = (shares * avg_buy_price) + ((avg_buy_price - index_price) * shares)
    return short
