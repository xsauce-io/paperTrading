import controller
from models import *
from datetime import datetime
from helpers.utils import *

def get_index_latest_info(message):
    parsed_message = split_message(message)

    if len(parsed_message) <= 1:
        raise ValueError('Please enter valid command. eg: /info xci')

    index_name = parsed_message[1]

    if controller.find_index(index_name) == False:
       raise ValueError("Index Not Found")

    index = controller.get_latest_index(index_name)
    index = format_index_price(index)
    return index


def format_index_price(index: Index) -> Index:
    price = round(index.price, 2)
    return Index(index.name, index.full_name, price, index.date,index.price)

def extract_info_message(message):
    parsed_message = split_message(message)

    if parsed_message[2] == "max":
        direction = parsed_message[1]
        wager = "max"
    else:
        if float(parsed_message[2]) < 0:
            raise UserInputException('Please enter a positive number')
        direction = parsed_message[1]
        wager = float(parsed_message[2])

    return wager, direction

def is_info_message_valid(parsed_message: list):
    if len(parsed_message) == 2:
       if type(parsed_message[1]) == str:
           return True
    return False
