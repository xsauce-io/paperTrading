import controller
from models import *
from helpers.utils import *

def track(sender, message):

    parsed_message = split_message(message)

    if is_track_message_format_valid(parsed_message) == False:
        raise UserInputException('Please enter valid command. eg: /track xci lesser/greater 500')
    if is_track_message_input_valid(parsed_message) == False:
        raise UserInputException('Please enter valid command. eg: /track xci lesser/greater 500')

    index_name, operator, target_price = extract_track_message(parsed_message)

    if controller.does_index_exist(index_name) == False:
       raise UserInputException("Index {} Not Found".format(index_name))

    date, time = get_current_date_time()

    controller.add_index_tracker(index_name, operator, target_price, sender, date, time)
    tracker = Tracker(index_name, operator, target_price, sender, date, time)
    return tracker


def extract_track_message(parsed_message):
    index_name = parsed_message[1]
    operator = parsed_message[2]
    target_price = float(parsed_message[3])

    return index_name, operator, target_price


def is_track_message_input_valid(parsed_message: list):
    index_name = parsed_message[1]
    operator  = parsed_message[2]
    target_price = parsed_message[3]
    if  operator == "lesser" or  operator  == "greater":
            if is_float(target_price):
                return True

    return False

def is_track_message_format_valid(parsed_message: list):
    if len(parsed_message) == 4:
       return True
    return False