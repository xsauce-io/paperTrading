import controller
from processes.portfolio import determine_global_portfolio, determine_portfolio_by_index


def leaderboard(sender, message):

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


    return



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
