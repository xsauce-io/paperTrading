import controller
from models import *
import math



def calculate_long_position(shares, avg_buy_price, index_price):
    long = (shares * avg_buy_price) + ((index_price - avg_buy_price) * shares)
    return long

def get_latest_xci_info():
    latest_xci = controller.get_latest_xci()
    latest_xci = format_index_info(latest_xci)
    return latest_xci

def format_index_info(index: Index) -> Index:
    price = round(index.price, 2)
    date = index.date
    time = index.price
    return Index(price, date, time)


def find_participant(sender):
    participant = tuple(controller.find_participant(sender).clone())
    if (len(participant) > 0):
        return True
    else:
        return False
