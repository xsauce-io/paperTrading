import controller
from models import *
from helpers.utils import *

def leaderboard(sender, message):
    parsed_message = split_message(message)

    if is_leaderboard_message_format_valid(parsed_message) == False:
        raise UserInputException('Please enter valid command.\neg: /leaderboard xci')
    if is_leaderboard_message_input_valid(parsed_message) == False:
        raise UserInputException('Please enter valid command.\neg: /leaderboard xci')


    leaderboard_name = extract_leaderboard_message(parsed_message)

    if controller.index_statistics.does_index_exist(leaderboard_name) == False and leaderboard_name != "pnl" and leaderboard_name != "comp": #TODO: Currently checking the index collection not a leaderboard collection
       raise UserInputException("Leaderboard Not Found")
    if leaderboard_name == "xj1" or leaderboard_name == "xj3" or leaderboard_name =="xj4":
       raise UserInputException("Oops index is not available yet. Stay tuned.")

    try:
        if leaderboard_name == "pnl":
            table_image_name = "images/global_pnl_leaderboard.png"

        elif leaderboard_name == "comp":
            table_image_name = "images/competition_pnl_leaderboard.png"
        else:
            table_image_name = "images/{}_pnl_leaderboard.png".format(leaderboard_name)

    except Exception as error:
        print(f"Cause: leaderboard {error}")
    return table_image_name

def extract_leaderboard_message(parsed_message):
    leaderboard_name = parsed_message[1]
    return leaderboard_name

def is_leaderboard_message_input_valid(parsed_message: list):
    if (type(parsed_message[1]) == str):
        return True
    return False

def is_leaderboard_message_format_valid(parsed_message: list):
    if len(parsed_message) == 2:
       if type(parsed_message[1]) == str:
           return True
    return False
