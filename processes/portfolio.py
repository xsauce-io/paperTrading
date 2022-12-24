import controller
from models import *
import math
from helpers.utils import *
from helpers.market_math import *




def portfolio(sender, message):

    parsed_message = split_message(message)

    if len(parsed_message) == 1:
        all_positions_names = controller.get_participant_all_positions_info(sender)
        all_portfolio =[]
        current_participant_info = 0
        current_participant_info = controller.get_participant_info(sender)
        for index_name in all_positions_names:
            current_index = controller.get_latest_index(index_name)
            current_position_info = controller.get_participant_position_info(sender, index_name)
            portfolio_info = create_portfolio(current_position_info, current_participant_info, current_index)

            all_portfolio.append(portfolio_info)

        long = 0
        short = 0
        for portfolio in all_portfolio:
            long += portfolio.long
            short += portfolio.short

        pnl = calculate_total_profit_and_loss(current_participant_info.funds, long, short)

        return TotalPortfolio(current_participant_info.funds, long, short,  pnl, current_participant_info.number_of_trades)


    if len(parsed_message) > 1:
        index_name = parsed_message[1]

        if controller.does_index_exist(index_name) == False:
            raise ValueError("Index Not Found")

        if controller.does_participant_have_position_for_index(sender, index_name) == False:
            raise ValueError('You have no positions open')

        current_index = controller.get_latest_index(index_name)
        current_position_info = controller.get_participant_position_info(sender, index_name)
        current_participant_info = controller.get_participant_info(sender)

        portfolio_info = create_portfolio(current_position_info, current_participant_info, current_index)

    return portfolio_info




def create_portfolio(position: Position, participant: Participant, index: Index):
    long_amount_spent = position.long_amount_spent
    short_amount_spent = position.short_amount_spent
    long_purchased = position.long_purchased
    short_purchased = position.short_purchased
    long_shares = position.long_shares
    short_shares = position.short_shares
    avg_buy_price_long = 0
    avg_buy_price_short = 0

    if long_amount_spent > 0:
        avg_buy_price_long = calculate_average_buy_price(
            long_amount_spent, long_purchased)
    if short_amount_spent > 0:
        avg_buy_price_short = calculate_average_buy_price(
            short_amount_spent, short_purchased)

    Long = calculate_long_position(
        long_shares, avg_buy_price_long, index.price)
    Short = calculate_short_position(
        short_shares, avg_buy_price_short, index.price)

    initial_long = long_shares * avg_buy_price_long
    initial_short = short_shares * avg_buy_price_short
    pnl = round(calculate_profit_and_loss(initial_long, initial_short, Long, Short), 3)

    return Portfolio(participant.funds, short_shares, long_shares, Long, Short, avg_buy_price_long, avg_buy_price_short, pnl, participant.number_of_trades, index.name)



def calculate_profit_and_loss(initial_long, initial_short, long, short):
    pnl_short = long - initial_long
    pnl_long = short - initial_short
    pnl = round(pnl_short+ pnl_long, 3)
    if math.isclose(pnl, 0.00):
        pnl = 0

    return pnl

def calculate_total_profit_and_loss(funds, long, short):
    initial_funds = 10000
    pnl = round((funds + short + long) - initial_funds, 3)
    if math.isclose(pnl, 0.00):
        pnl = 0
    return pnl
