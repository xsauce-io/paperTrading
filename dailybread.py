import math
from telegram import *
from telegram.ext import *
import requests
import re
import os
from dotenv import load_dotenv
import requests
from datetime import datetime
import pymongo
from pymongo import MongoClient
from models import *
import processes.play
import processes.info
import processes.portfolio
import processes.open
import processes.close
import processes.manage_index
import processes.composition
from indexMaker.index_maker import *
from indexMaker.constituents_store import *

load_dotenv()

PASSWORD = os.environ['password']
USERNAME = os.environ['username']
BOT_TOKEN = os.environ['bot_token']
API = os.environ['api']
CHAT = os.environ['chat']
DATABASE_NAME = os.environ['db_name']
COLLECTION_NAME1 = os.environ['collection_name1']
COLLECTION_NAME2 = os.environ['collection_name2']
URL = os.environ['db_url']
cluster = MongoClient(URL)


def price_update(context):
    try:
        culture = calculate_index_price(CULTURE_INDEX_CONSTITUENTS)
        context.bot.send_message(CHAT,
                                 text="Xsauce Culture Index is ${}".format(round(culture, 2)))

        processes.manage_index.add_index_statistics("xci" , "Xsauce Culture Index" ,culture)
    except Exception as error:
        print('Cause {}'.format(error))

def price_update2(context):
    try:
        hype6_index_price = calculate_index_price(HYPE6_INDEX_CONSTITUENTS)
        context.bot.send_message(CHAT,
                                 text="HYPE6 is ${}".format(round(hype6_index_price, 2)))

        processes.manage_index.add_index_statistics("hype6" , "HYPE6", hype6_index_price)
    except Exception as error:
        print('Cause {}'.format(error))

def price_update3(context):
    try:
        sp50_index_price = calculate_composite_index_price(SNEAKER_SP50_INDEX_CONSTITUENTS)
        context.bot.send_message(CHAT,
                                 text="Sneaker Benchmark S&P50 is ${}".format(round(sp50_index_price, 2)))

        processes.manage_index.add_index_statistics("sp50" , "Sneaker S&P50", sp50_index_price)
    except Exception as error:
        print('Cause {}'.format(error))


def index_price(update, context):
    message = update.message.text
    try:
        index_info = processes.info.get_index_latest_info(message)
        update.message.reply_text("{} is ${}. Updated on {} at {} UTC".format(
            index_info.full_name, index_info.price, index_info.date, index_info.time))
    except UserInputException as error:
        print('Cause {}'.format(error))
        update.message.reply_text('{}'.format(error))
    except Exception as error:
        print('Cause {}'.format(error))

def index_composition(update, context):
    message = update.message.text
    try:
        composition_string = processes.composition.get_index_composition(message)
        update.message.reply_text(composition_string, parse_mode='Markdown')
    except UserInputException as error:
        print('Cause {}'.format(error))
        update.message.reply_text('{}'.format(error))
    except Exception as error:
        print('Cause {}'.format(error))


def play(update, context):
    sender = update.message.from_user.username
    try:
        reply = processes.play.play(sender)
        update.message.reply_text(reply)
    except UserInputException as error:
        print('Cause {}'.format(error))
        update.message.reply_text('{}'.format(error))
    except Exception as error:
        print('Cause {}'.format(error))


def welcome(update, context):
    new_members = update.effective_message.new_chat_members

    context.bot.send_message(CHAT,
                             text="Welcome to the Xchange {}!\n\nUse the /help command to see all options".format(new_members[-1].username))


def portfolio(update, context):
    sender = update.message.from_user.username
    message = update.message.text
    try:
        portfolio = processes.portfolio.portfolio(sender, message)
        if type(portfolio) == Portfolio:
            formatted_message = format_portfolio_string(portfolio)

        elif type(portfolio) == GlobalPortfolio:
            formatted_message = format_total_string(portfolio)
        update.message.reply_text(
                formatted_message,
                parse_mode='Markdown'
            )
    except UserInputException as error:
        print('Cause {}'.format(error))
        update.message.reply_text('{}'.format(error))
    except Exception as error:
        print('Cause {}'.format(error))


def format_portfolio_string(portfolio: Portfolio):
    message = "*Index:* {}\n" \
        "*Balance:* ${}\n" \
        "*Holdings(of XCI)*: {} Short / {} Long\n" \
        "*Total(Unsettled)*: ${}\n" \
        "*Avg Buy Price*:{} Short / {} Long\n" \
        "*PNL*: ${}\n" \
        "*Total Trades*: {}"
    formatted_message = message.format(portfolio.index_name,
                            round(portfolio.funds, 3),
                           round(portfolio.short_shares, 3),
                           round(portfolio.long_shares, 3),
                           round(portfolio.long + portfolio.short, 2),
                           round(portfolio.avg_buy_price_short, 3),
                           round(portfolio.avg_buy_price_long, 3),
                           portfolio.pnl,
                           portfolio.number_of_trades)
    return formatted_message

def format_total_string(portfolio: Portfolio):
    message = "*Balance:* ${}\n" \
        "*Total(Unsettled)*: ${}\n" \
        "*PNL*: ${}\n" \
        "*Total Trades*: {}"
    formatted_message = message.format(
                           round(portfolio.funds, 3),
                           round(portfolio.long + portfolio.short, 2),
                           portfolio.pnl,
                           portfolio.number_of_trades)
    return formatted_message

def instructions(update, context):
    update.message.reply_text(
        "https://docs.xsauce.io/applications/how-it-works")


def open(update, context):
    sender = update.message.from_user.username
    message = update.message.text

    try:
        result = processes.open.open(sender, message)
        update.message.reply_text(result)
    except UserInputException as error:
        print('Cause {}'.format(error))
        update.message.reply_text('{}'.format(error))
    except Exception as error:
        print('Cause {}'.format(error))


def close(update, context):
    sender = update.message.from_user.username
    message = update.message.text
    try:
        reply = processes.close.close(sender, message)
        update.message.reply_text(reply)
    except UserInputException as error:
        print('Cause {}'.format(error))
        update.message.reply_text('{}'.format(error))
    except Exception as error:
        print('Cause {}'.format(error))

def list_index(update, context):
    ##warning the list is hard coded for now
    try:
        update.message.reply_text( "*Xsauce Culture Index:* xci\n" \
        "*HYPE6:* hype6\n" \
        "*Sneaker Benchmark S&P50*: sp50\n", parse_mode='Markdown')
    except Exception and ValueError as error:
        print('Cause {}'.format(error))
        update.message.reply_text('{}'.format(error))


def help(update, context):
    update.message.reply_text(
        "/instructions -> Learn how to use the Xchange\n"
        "/play -> Use this command to get $10,000 dollars to start up!\n"
        "/list -> Show the list of index names\n"
        "/open -> Open a position\n"
        "/close -> Close a position\n"
        "/info index_name -> Show the current price of an index\n"
        "/comp index_name -> Show the index composition\n"
        "/portfolio -> Show your current portfolio holdings\n"
        "/portfolio index_name-> Show your current portfolio holdings for given index\n"
        "/help -> Shows this message\n"
        "/website -> Learn about Xsauce and cultural assets"
    )

def website(update, context):
    update.message.reply_text(
        "Check out our website to see what Xsauce is all about: https://xsauce.io/ ")


def main():
    updater = Updater(
        BOT_TOKEN, use_context=True)
    job_queue = updater.job_queue
    job_seconds = job_queue.run_repeating(
        price_update, interval=86400, first=1)
    job_seconds_2 = job_queue.run_repeating(
        price_update2, interval=86400, first=1)
    job_seconds_3 = job_queue.run_repeating(
        price_update3, interval=86400, first=1)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CommandHandler('close', close))
    dispatcher.add_handler(CommandHandler('portfolio', portfolio))
    dispatcher.add_handler(CommandHandler('play', play))
    dispatcher.add_handler(CommandHandler('list', list_index))
    dispatcher.add_handler(CommandHandler('website', website))
    dispatcher.add_handler(CommandHandler('open', open))
    dispatcher.add_handler(CommandHandler('info', index_price))
    dispatcher.add_handler(CommandHandler('comp', index_composition))
    dispatcher.add_handler(CommandHandler('instructions', instructions))
    dispatcher.add_handler(MessageHandler(
        Filters.status_update.new_chat_members, welcome))

    updater.start_polling(allowed_updates=Update.ALL_TYPES)
    updater.idle()


main()
