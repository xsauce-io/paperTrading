import controller
from models import *
from helpers.utils import *

def get_index_latest_info(message):
    parsed_message = split_message(message)

    if is_info_message_format_valid(parsed_message) == False:
        raise UserInputException('Please enter valid command.\neg: /info')
    if is_info_message_input_valid(parsed_message) == False:
        raise UserInputException('Please enter valid command.\neg: /info')

    index_name = extract_info_message(parsed_message)

    if controller.index_statistics.does_index_exist(index_name) == False:
       raise UserInputException("Index Not Found")

    index = controller.index_statistics.get_latest_index(index_name)
    index = format_index_price(index)
    return index

def get_all_latest_index_price(index_names: list):

    indexes = controller.index_statistics.get_all_latest_index(index_names)
    formatted_indexes = []

    for index in indexes:
        formatted_index = format_index_price(index)
        formatted_indexes.append(formatted_index)

    return formatted_indexes


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
    if len(parsed_message) == 2 :
       if type(parsed_message[1]) == str:
           return True
    return False
