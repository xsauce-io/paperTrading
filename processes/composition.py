import controller
from models import *
from helpers.utils import *


def get_index_composition(message):
    parsed_message = split_message(message)

    if is_composition_message_format_valid(parsed_message) == False:
        raise UserInputException('Please enter valid command.\neg: /comp xci')
    if is_composition_message_input_valid(parsed_message) == False:
        raise UserInputException('Please enter valid command.\neg: /comp xci')

    index_name = extract_composition_message(parsed_message)

    if controller.index_statistics.does_index_exist(index_name) == False:
       raise UserInputException("Index Not Found")
    if index_name == "xj1" or index_name == "xj3" or index_name =="xj4":
       raise UserInputException("Oops index is not available yet. Stay tuned.")
    if controller.index_composition.does_index_composition_exist(index_name) == False:
       raise UserInputException("Composition Not Found")

    composition_items = controller.index_composition.get_index_composition(index_name)
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
