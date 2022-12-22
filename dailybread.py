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
import controller
import processes.play
import processes.index_price
import processes.portfolio
import processes.open
import processes.close
import service

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
        skus = ["555088-063",
                "DO9392-700",
                "DD1391-400",
                "GW3355",
                "DC9533-800",
                "BB550WT1",
                "GX2487",
                "GW1229",
                "DH9792-100",
                "DH7863-100"]

        resData = []

        for sku in skus:
            sneak_url = API + sku
            response = requests.get(sneak_url)
            print(response.json()[
                'results'][0]['estimatedMarketValue'])
            resData.append(response.json()[
                'results'][0]['estimatedMarketValue'])
        culture = 0
        culture += resData[0] * .125
        culture += resData[1] * .14
        culture += resData[2] * .150
        culture += resData[3] * .075
        culture += resData[4] * .011
        culture += resData[5] * .18
        culture += resData[6] * .08
        culture += resData[7] * .185
        culture += resData[8] * .017
        culture += resData[9] * .037
        context.bot.send_message(CHAT,
                                 text="Xsauce Culture Index is ${}".format(round(culture, 2)))

        db = cluster[DATABASE_NAME]
        stats = db[COLLECTION_NAME2]
        strip = datetime.now()
        date = strip.strftime('%m/%d/%Y')
        time = strip.strftime("%H:%M:%S")

        stats.insert_one(
            {"price": culture, "date": date, "time": time})
    except Exception as error:
        print('Cause {}'.format(error))


def xci_price(update, context):
    try:
        xci_info = processes.index_price.get_latest_xci_info()
        update.message.reply_text("Xsauce Culture Index is ${}. Updated on {} at {} UTC".format(
            xci_info.price, xci_info.date, xci_info.time))
    except Exception as error:
        print('Cause {}'.format(error))
        update.message.reply_text(error)


def play(update, context):
    sender = update.message.from_user.username
    try:
        if processes.play.find_participant(sender):
            update.message.reply_text("Nice try! No such thing as free")
        else:
            processes.play.create_participant(sender)
            update.message.reply_text(
                "Welcome {},\nThis is v0 of Daily Bread. Your account has been funded with $10,000".format(sender))
    except Exception as error:
        print('Cause{}'.format(error))


def welcome(update, context):
    new_members = update.effective_message.new_chat_members

    context.bot.send_message(CHAT,
                             text="Welcome to the Xchange {}!\n\nUse the /help command to see all options".format(new_members[-1].username))


def portfolio(update, context):
    sender = update.message.from_user.username
    try:
        portfolio = processes.portfolio.get_portfolio(sender)
        funds = portfolio.funds
        short_shares = portfolio.short_shares
        long_shares = portfolio.long_shares
        Long  = portfolio.long
        Short = portfolio.short
        avg_buy_price_long = portfolio.avg_buy_price_long
        avg_buy_price_short = portfolio.avg_buy_price_short
        pnl = portfolio.pnl
        number_of_trades = portfolio.number_of_trades

        message = "*Balance:* ${}\n" \
            "*Holdings(of XCI)*: {} Short / {} Long\n" \
            "*Total(Unsettled)*: ${}\n" \
            "*Avg Buy Price*:{} Short / {} Long\n" \
            "*PNL*: ${}\n" \
            "*Total Trades*: {}"

        update.message.reply_text(
            message.format(round(funds, 3),
                           round(short_shares, 3),
                           round(long_shares, 3),
                           round(Long + Short, 2),
                           round(avg_buy_price_short, 3),
                           round(avg_buy_price_long, 3),
                           pnl,
                           number_of_trades),
            parse_mode='Markdown'
        )

    except Exception as error:
        update.message.reply_text("You hold no positions/ Error")
        print('Cause {}'.format(error))


def calculate_average_buy_price(amount_spent, purchased):
    avg_buy_price = amount_spent / purchased
    return avg_buy_price


def calculate_long_position(shares, avg_buy_price, index_price):
    long = (shares * avg_buy_price) + ((index_price - avg_buy_price) * shares)
    return long


def calculate_short_position(shares, avg_buy_price, index_price):
    short = (shares * avg_buy_price) + ((avg_buy_price - index_price) * shares)
    return short



def instructions(update, context):
    update.message.reply_text(
        "https://docs.xsauce.io/applications/how-it-works")


def open(update, context):
    sender = update.message.from_user.username
    message = update.message.text

    try:
        result = processes.open.open(sender, message)
        update.message.reply_text(result)
    except Exception and ValueError as error:
        print('Cause {}'.format(error))
        update.message.reply_text('{}'.format(error))


def close(update, context):
    sender = update.message.from_user.username
    message = update.message.text
    try:
        reply = processes.close.close(sender,message)
        update.message.reply_text(reply)
    except Exception and ValueError as error:
        print('Cause {}'.format(error))
        update.message.reply_text('{}'.format(error))


def help(update, context):
    update.message.reply_text(
        "/instructions -> Learn how to use the Xchange\n"
        "/play -> Use this command to get $10,000 dollars to start up!\n"
        "/open -> Open a position\n"
        "/close -> Close a position\n"
        "/xci -> Show the current price of the Xsauce Culture Index\n"
        "/portfolio -> Show your current index holdings\n"
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
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CommandHandler('close', close))
    dispatcher.add_handler(CommandHandler('portfolio', portfolio))
    dispatcher.add_handler(CommandHandler('play', play))
    dispatcher.add_handler(CommandHandler('website', website))
    dispatcher.add_handler(CommandHandler('xci', xci_price))
    dispatcher.add_handler(CommandHandler('open', open))
    dispatcher.add_handler(CommandHandler('instructions', instructions))
    dispatcher.add_handler(MessageHandler(
        Filters.status_update.new_chat_members, welcome))

    updater.start_polling(allowed_updates=Update.ALL_TYPES)
    updater.idle()


main()
