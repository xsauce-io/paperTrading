from models import *
from .database import *
import controller

#Participant
def does_participant_exist(sender) -> bool:
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


def update_participant_position(sender, index_name, position:Position, participant:Participant):

    participants.update_one({"username": sender}, {"$set": {
                f"positions.{index_name}": {"Short": {"shares": position.short_shares, "buyIn": {"purchased": position.short_shares, "amount_spent": position.short_amount_spent}}, "Long": {"shares": position.long_shares, "buyIn": {"purchased": position.long_shares, "amount_spent": position.long_amount_spent}}}, "funds": participant.funds, "trades": participant.number_of_trades}})
    return

def add_index_to_participant_positions(sender, index_name):
    participants.update_one({"username": sender}, {"$set": {
                f"positions.{index_name}": {"Short": {"shares": 0, "buyIn": {"purchased": 0, "amount_spent": 0}}, "Long": {"shares": 0, "buyIn": {"purchased": 0, "amount_spent": 0}}}}})

    return

# def add_trade_to_participant_trades(sender, trade: TradeDetails):
#     trades = list(get_participant_trades_details(sender))
#     trades.append({"action": trade.action, "direction": trade.direction, "amount": trade.amount, "index_price": trade.index_price,
#                 "index_name": trade.index_name,"date": trade.date, "time": trade.time})
#     return trades

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
        index = controller.index_statistics.get_latest_index(index_name)
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
    return get_participant(sender)['number_of_trades']

# def get_participant_trades_details(sender):
#     return get_participant(sender)['trades']['tradeDetails']

def get_participant_positions(sender):
    return get_participant(sender)['positions']

def get_participant_username(sender):
    return get_participant(sender)['username']
