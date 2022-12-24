import controller
from models import *
from datetime import datetime
from helpers.utils import *

def get_index_composition(message):
    parsed_message = split_message(message)

    if len(parsed_message) <= 1:
        raise ValueError('Please enter valid command. eg: /comp xci')

    index_name = parsed_message[1]

    if controller.find_index(index_name) == False:
       raise ValueError("Index Not Found")

    composition_items = controller.get_index_composition(index_name)

    composition_string = ""
    for item in composition_items:
        composition_string += (f"*{item['name']}:* {item['weight']}%\n")
    return composition_string
