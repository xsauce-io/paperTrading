import controller
from models import *
import math

def get_latest_xci_info():
    latest_xci = controller.get_latest_xci()
    latest_xci = format_index_price(latest_xci)
    return latest_xci


def format_index_price(index: Index) -> Index:
    price = round(index.price, 2)
    date = index.date
    time = index.price
    return Index(price, date, time)
