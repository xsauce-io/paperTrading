import controller
from tabulate import tabulate
from processes.portfolio import determine_global_portfolio, determine_portfolio_by_index
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import dataframe_image as dfi
import textwrap

def leaderboard(sender, message):

    try:
        global_pnl_leaderboard = []
        all_participants_names = controller.get_all_participants_names()

        for participant_name in all_participants_names:

            global_portfolio = calculate_global_portfolio(participant_name)

            participant_leaderboard_item = {"username": participant_name ,"pnl": global_portfolio.pnl }

            if len(global_pnl_leaderboard) < 3:
                global_pnl_leaderboard.append(participant_leaderboard_item)

                print (global_pnl_leaderboard)
                global_pnl_leaderboard = sorted(global_pnl_leaderboard, key=lambda d: d['pnl'])
                print (global_pnl_leaderboard)
            else:
                last_ranked_leaderboard_item = global_pnl_leaderboard[0]
                if participant_leaderboard_item["pnl"] > last_ranked_leaderboard_item['pnl']:
                    global_pnl_leaderboard.pop(0)
                    global_pnl_leaderboard.append(participant_leaderboard_item)
                    global_pnl_leaderboard = sorted(global_pnl_leaderboard, key=lambda d: d['pnl'])

                print (global_pnl_leaderboard)

        global_pnl_leaderboard_descending = sorted(global_pnl_leaderboard, key=lambda d: d['pnl'], reverse=True)

        headers, data = format_leaderboard_table(global_pnl_leaderboard_descending, ["rank", "username", "pnl"])

        # df = pd.DataFrame(data, columns=headers)

        # df.set_index('rank', inplace=True)
        # df.style.set_table_styles(styles)
        # dfi.export(df, 'df_image.png', fontsize=15, max_rows=-1)

    except Exception as error:
        print("leaderboard")
    return headers



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


def format_leaderboard_table(global_pnl_leaderboard: list, headers: list):
    try :
        data = []
        count= 1
        for item in global_pnl_leaderboard:
            rank = count
            name = item['username']
            value = round(item['pnl'], 2)
            leaderboard_item = [rank, name, value]
            data.append(leaderboard_item)
            count += 1

        table_to_string = tabulate(data, headers, tablefmt='orgtbl')

        font = ImageFont.load_default()
        image = Image.new("RGB", size=(250, 190) ,  color = (255, 255, 255))
        draw = ImageDraw.Draw(image)
        draw.text((7, 7), table_to_string, font=font, fill="black" , spacing=20)
        #lines = textwrap.wrap(table_to_string, width=50)
        #draw.multiline_text((15,15), '\n'.join(lines), font=font, fill ="black")
        image.save("my_table_image.png", 'PNG')

    except Exception as error:
         print (error)
         print("format_leaderboard")
    return headers, data
