import controller
from models import *
from datetime import datetime
from helpers.utils import *

def get_index_latest_info(message):
    parsed_message = split_message(message)

    if is_info_message_format_valid(parsed_message) == False:
        raise UserInputException('Please enter valid command.\neg: /info xci')
    if is_info_message_input_valid(parsed_message) == False:
        raise UserInputException('Please enter valid command.\neg: /info xci')

    index_name = extract_info_message(parsed_message)

    if controller.does_index_exist(index_name) == False:
       raise UserInputException("Index Not Found")

    index = controller.get_latest_index(index_name)
    index = format_index_price(index)
    return index


def format_index_price(index: Index) -> Index:
    price = round(index.price, 2)
    return Index(index.name, index.full_name, price, index.date, index.time)

def extract_info_message(parsed_message):
    index_name = parsed_message[1]
    return index_name

def is_info_message_input_valid(parsed_message: list):
    if (type(parsed_message[1]) == str):
        return True
    return False

def is_info_message_format_valid(parsed_message: list):
    if len(parsed_message) == 2:
       if type(parsed_message[1]) == str:
           return True
    return False
