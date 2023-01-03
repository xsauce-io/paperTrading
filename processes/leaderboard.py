import controller
from tabulate import tabulate
from processes.portfolio import determine_global_portfolio, determine_portfolio_by_index
from PIL import Image, ImageDraw, ImageFont
from models import *
from helpers.utils import *

def leaderboard(sender, message):
    parsed_message = split_message(message)

    if is_leaderboard_message_format_valid(parsed_message) == False:
        raise UserInputException('Please enter valid command.\neg: /leaderboard xci')
    if is_leaderboard_message_input_valid(parsed_message) == False:
        raise UserInputException('Please enter valid command.\neg: /leaderboard xci')

    leaderboard_name = extract_leaderboard_message(parsed_message)

    if controller.does_index_exist(leaderboard_name) == False: #TODO: Currently checking the index collection not a leaderboard collection
       raise UserInputException("Leaderboard Not Found")

    try:

        #if leaderboard_name == "pnl":
            #create_pnl_leaderboard
        participants_leaderboard_items = []
        table_image_name = "global_pnl_leaderboard.png"
        all_participants_names = controller.get_all_participants_names()


        for participant_name in all_participants_names:

            global_portfolio = calculate_global_portfolio(participant_name)
            participant_leaderboard_item_pnl = {"username": participant_name ,"value": global_portfolio.pnl }
            participants_leaderboard_items.append(participant_leaderboard_item_pnl)

        global_pnl_leaderboard_descending = calculate_top3_leaderboard(participants_leaderboard_items)


        table_as_string = create_table_as_string(global_pnl_leaderboard_descending, ["rank", "username", "pnl"])
        table_image = create_image_from_table(table_as_string, (250, 170))
        table_image.save("global_pnl_leaderboard.png", "PNG")


    except Exception as error:
        print(f"Cause: leaderboard {error}")
    return table_image_name

def calculate_top3_leaderboard(leaderboard_items: list):
    leaderboard = []

    for item in leaderboard_items:
        if len(leaderboard) < 3:
            leaderboard.append(item)
            leaderboard = sorted(leaderboard, key=lambda d: d['value'])
            print (leaderboard)
        else:
            last_ranked_leaderboard_item = leaderboard[0]
            if item["value"] > last_ranked_leaderboard_item['value']:
                leaderboard.pop(0)
                leaderboard.append(item)
                leaderboard = sorted(leaderboard, key=lambda d: d['value'])

    leaderboard_sorted_top3 = sorted(leaderboard, key=lambda d: d['value'], reverse=True)

    return leaderboard_sorted_top3


def calculate_global_portfolio(participant_name):
    all_positions_index_names = controller.get_participant_all_positions_names(participant_name)
    current_participant_info = controller.get_participant_info(participant_name)

    all_portfolio =[]

    for index_name in all_positions_index_names:
        current_index = controller.get_latest_index(index_name)
        current_position_info = controller.get_participant_position_info(participant_name, index_name)
        portfolio_info = determine_portfolio_by_index(current_position_info, current_participant_info, current_index)

        all_portfolio.append(portfolio_info)

    global_portfolio = determine_global_portfolio(all_portfolio, current_participant_info)

    return global_portfolio



def create_table_as_string(leaderboard: list, headers: list) -> str:
    try :
        data = []
        count= 1
        for item in leaderboard:
            rank = count
            name = item['username']
            value = round(item['value'], 2)
            leaderboard_item = [rank, name, value]
            data.append(leaderboard_item)
            count += 1

        table_to_string = tabulate(data, headers, tablefmt='orgtbl')

    except Exception as error:
         print (error)
         print("format_leaderboard")
    return table_to_string

def create_image_from_table(table_as_string: str, size):
    image = ""
    try:
        W, H = size
        font = ImageFont.load_default()
        image = Image.new("RGB", size=size, color = (255, 255, 255))
        draw = ImageDraw.Draw(image)
        _, _, w, h = draw.textbbox((0, 0), table_as_string, font=font)
        draw.text(((W-w)/2, (H-h)/2), table_as_string, font=font, fill="black", spacing=5)

    except Exception as error:
        print (f"Cause create image error: {error}")
    return image


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
