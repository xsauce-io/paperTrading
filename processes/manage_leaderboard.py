import controller.controller as controller
from tabulate import tabulate
from processes.portfolio import determine_global_portfolio, determine_portfolio_by_index
from PIL import Image, ImageDraw, ImageFont
from models import *
from helpers.utils import *

def update_leaderboard(leaderboard_name):

    if controller.does_index_exist(leaderboard_name) == False and leaderboard_name != "pnl": #TODO: Currently checking the index collection not a leaderboard collection
       raise UserInputException("Leaderboard Not Found")

    try:

        participants_leaderboard_items = []
        table_image_name = ""
        all_participants_names = controller.get_all_participants_names()

        if leaderboard_name == "pnl":
            for participant_name in all_participants_names:

                global_portfolio = calculate_global_portfolio(participant_name)
                participant_leaderboard_item_pnl = {"username": participant_name ,"value": global_portfolio.pnl }
                participants_leaderboard_items.append(participant_leaderboard_item_pnl)

            pnl_leaderboard = calculate_top5_leaderboard(participants_leaderboard_items)
            table = create_table_as_string(pnl_leaderboard , ["rank", "username", "pnl"])
            table_image_name = "images/global_pnl_leaderboard.png"

        else:
            #@TODO check participant has position
            all_participants_names_by_index = []
            for participant_name in all_participants_names:
                if controller.does_participant_have_position_for_index(participant_name, leaderboard_name) == True: #Warning leaderboard name is synonymous with index_name here
                    all_participants_names_by_index.append(participant_name)

            for participant_name in all_participants_names_by_index:

                current_index = controller.get_latest_index(leaderboard_name)

                current_position_info = controller.get_participant_position_info(participant_name, leaderboard_name)
                current_participant_info = controller.get_participant_info(participant_name)

                portfolio_info = determine_portfolio_by_index(current_position_info, current_participant_info, current_index)

                participant_leaderboard_item_index_pnl = {"username": participant_name ,"value": portfolio_info.pnl }
                participants_leaderboard_items.append(participant_leaderboard_item_index_pnl)

            pnl_by_index_leaderboard = calculate_top5_leaderboard(participants_leaderboard_items)
            table = create_table_as_string(pnl_by_index_leaderboard , ["rank", "username", f"{leaderboard_name} pnl"])
            table_image_name = "images/{}_pnl_leaderboard.png".format(leaderboard_name)


        table_image = create_image_from_table(table, (250, 160))
        table_image.save(table_image_name, format="PNG",  dpi=(300, 300),  quality=95)


    except Exception as error:
        print(f"Cause: leaderboard {error}")
    return table_image_name

def calculate_top5_leaderboard(leaderboard_items: list):
    leaderboard = []

    for item in leaderboard_items:
        if len(leaderboard) < 5:
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
        image = Image.new("RGB", size=size, color="#0C1615")
        draw = ImageDraw.Draw(image)
        _, _, w, h = draw.textbbox((0, 0), table_as_string, font=font)
        draw.text(((W-w)/2, (H-h)/2), table_as_string, font=font, fill="#ACFF00", spacing=5)

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
