import controller
from models import *
import math


def portfolio(sender):
    current_index_price = controller.get_latest_xci().price
    position = controller.get_participant_position_info(sender)
    number_of_trades = controller.get_participants_trades_total(sender)
    funds = controller.get_participant_funds(sender)
    portfolio_info = create_portfolio(position, funds, number_of_trades, current_index_price)

    return portfolio_info


def create_portfolio(position: Position, funds, number_of_trades, current_index_price):
    long_amount_spent = position.long_amount_spent
    short_amount_spent = position.short_amount_spent
    long_purchased = position.long_purchased
    short_purchased = position.short_purchased
    long_shares = position.long_shares
    short_shares = position.short_shares
    avg_buy_price_long = 0
    avg_buy_price_short = 0

    if long_amount_spent > 0:
        avg_buy_price_long = calculate_average_buy_price(long_amount_spent, long_purchased)
    if short_amount_spent > 0:
        avg_buy_price_short = calculate_average_buy_price(short_amount_spent, short_purchased)

    Long = calculate_long_position(long_shares, avg_buy_price_long, current_index_price)
    Short = calculate_short_position(short_shares, avg_buy_price_short, current_index_price)
    pnl = round(calculate_profit_and_loss(funds, Long, Short), 3)

    return Portfolio(funds, short_shares, long_shares, Long, Short, avg_buy_price_long, avg_buy_price_short, pnl, number_of_trades)

def calculate_average_buy_price(amount_spent, purchased):
    avg_buy_price = amount_spent / purchased
    return avg_buy_price


def calculate_long_position(shares, avg_buy_price, index_price):
    long = (shares * avg_buy_price) + ((index_price - avg_buy_price) * shares)
    return long


def calculate_short_position(shares, avg_buy_price, index_price):
    short = (shares * avg_buy_price) + ((avg_buy_price - index_price) * shares)
    return short


def calculate_profit_and_loss(funds, long, short):
    initial_funds = 10000
    pnl = (funds + short + long) - initial_funds
    if math.isclose(pnl, 0.00):
        pnl = 0
    return pnl