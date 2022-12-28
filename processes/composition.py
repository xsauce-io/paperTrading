import controller
from models import *
from datetime import datetime
from helpers.utils import *
from prettytable import PrettyTable


def get_index_composition(message):
    parsed_message = split_message(message)

    if is_composition_message_format_valid(parsed_message) == False:
        raise UserInputException('Please enter valid command.\neg: /comp xci')
    if is_composition_message_input_valid(parsed_message) == False:
        raise UserInputException('Please enter valid command.\neg: /comp xci')

    index_name = extract_composition_message(parsed_message)

    if controller.does_index_exist(index_name) == False:
       raise UserInputException("Index Not Found")
    if controller.does_index_composition_exist(index_name) == False:
       raise UserInputException("Composition Not Found")

    composition_items = controller.get_index_composition(index_name)
    composition_string = format_composition_to_string(composition_items)

    return composition_string

def format_composition_to_string(composition) -> str:
    composition_string = ""
    for item in composition:
        composition_string += (f"*{item['name']}:* {item['weight_in_percentage']}%\n")
    return composition_string

def extract_composition_message(parsed_message):
    index_name = parsed_message[1]
    return index_name

def is_composition_message_input_valid(parsed_message: list):
    if (type(parsed_message[1]) == str):
        return True
    return False

def is_composition_message_format_valid(parsed_message: list):
    if len(parsed_message) == 2:
       if type(parsed_message[1]) == str:
           return True
    return False
