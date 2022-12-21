import math
from telegram import *
from telegram.ext import *
import requests
import re
import os
from dotenv import load_dotenv
import configparser
import requests
from datetime import datetime
import pymongo
from pymongo import MongoClient

load_dotenv()

config = configparser.ConfigParser()
config.read('config.ini')
PASSWORD = os.environ['password']
USERNAME = os.environ['username']
BOT_TOKEN = os.environ['bot_token']
API = os.environ['api']
CHAT = os.environ['chat']
DATABASE_NAME = os.environ['db_name']
COLLECTION_NAME1 = os.environ['collection_name1']
COLLECTION_NAME2 = os.environ['collection_name2']
URL = os.environ['db_url']
# url = "mongodb+srv://" + USERNAME + ":" + PASSWORD + \
#     "@xsauce-telegram.7zeqjol.mongodb.net/?retryWrites=true&w=majority"
cluster = MongoClient(URL)


def priceUpdate(context):
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
        db = cluster[DATABASE_NAME]
        stats = db[COLLECTION_NAME2]
        info = stats.find().sort("_id", -1)[0]
        culture = info['price']
        culture_date = info['date']
        culture_time = info['time']
        update.message.reply_text("Xsauce Culture Index is ${}. Updated on {} at {} UTC".format(
            round(culture, 2), culture_date, culture_time))
    except Exception as error:
        print('Cause {}'.format(error))
        update.message.reply_text(error)


def play(update, context):
    sender = update.message.from_user.username
    try:
        db = cluster[DATABASE_NAME]
        participants = db[COLLECTION_NAME1]
        res = participants.find({"username": sender})
        if len(list(res.clone())) > 0:
            update.message.reply_text("Nice try! No such thing as free")
        else:
            participants.insert_one(
                {"username": sender, "funds": 10000, "position": {"Long": {"shares": 0, "buyIn": {"purchased": 0, "amount_spent": 0}}, "Short": {"shares": 0, "buyIn": {"purchased": 0, "amount_spent": 0}}}, "trades": {"total": 0, "tradeDetails": []}})
            update.message.reply_text(
                "Welcome {},\n This is v0 of Daily Bread. Your account has been funded with $10,000".format(sender))
    except Exception as error:
        print('Cause{}'.format(error))


def welcome(update, context):
    new_members = update.effective_message.new_chat_members

    context.bot.send_message(CHAT,
                             text="Welcome to the Xchange {}!\n\nUse the /help command to see all options".format(new_members[-1].username))


def portfolio(update, context):
    username = update.message.from_user.username
    try:
        db = cluster[DATABASE_NAME]
        participants = db[COLLECTION_NAME1]
        stats = db[COLLECTION_NAME2]
        res2 = stats.find().sort("_id", pymongo.DESCENDING)[0]
        currIndexPrice = res2['price'] + 50
        print(currIndexPrice)
        res = participants.find({"username": username})[0]
        avg_buy_price_long = 0
        avg_buy_price_short = 0
        if res['position']['Long']['buyIn']['amount_spent'] > 0:
            avg_buy_price_long = res['position']['Long']['buyIn']['amount_spent'] / \
                res['position']['Long']['buyIn']['purchased']
        if res['position']['Short']['buyIn']['amount_spent'] > 0:
            avg_buy_price_short = res['position']['Short']['buyIn']['amount_spent'] / \
                res['position']['Short']['buyIn']['purchased']
        Long = res['position']["Long"]['shares'] * avg_buy_price_long + \
            (currIndexPrice - avg_buy_price_long) * \
            res['position']['Long']['shares']
        Short = res['position']["Short"]['shares'] * avg_buy_price_short + \
            (avg_buy_price_short - currIndexPrice) * \
            res['position']["Short"]['shares']
        pnl = round((res['funds'] + (Long + Short)) - 10000, 3)
        if math.isclose(pnl, 0.00):
            pnl = 0
        message = "*Balance:* ${}\n" \
            "*Holdings(of XCI)*: {} Short / {} Long\n" \
            "*Total(Unsettled)*: ${}\n" \
            "*Avg Buy Price*:{} Short / {} Long\n" \
            "*PNL*: ${}\n" \
            "*Total Trades*: {}"

        update.message.reply_text(
            message.format(round(res['funds'], 3),
                           round(res['position']['Short']['shares'], 3),
                           round(res['position']['Long']['shares'], 3),
                           round(Long + Short, 2),
                           round(avg_buy_price_short, 3),
                           round(avg_buy_price_long, 3),
                           pnl,
                           res['trades']['total']),
            parse_mode='Markdown'
        )

    except Exception as error:
        update.message.reply_text("You hold no positions/ Error")
        print('Cause {}'.format(error))


def instructions(update, context):
    update.message.reply_text(
        "https://docs.xsauce.io/applications/how-it-works")


def open(update, context):
    sender = update.message.from_user.username
    x = re.split("\s", update.message.text)
    wager = x[2]
    try:
        if x[2] == "max":
            wager = "max"
        elif x[2] == None or x[1] == None or len(x) > 3:
            raise ValueError()
        else:
            if float(x[2]) < 0:
                raise ValueError('Please enter a positive number')
            wager = float(x[2])
    except ValueError as error:
        if error == 'Please enter a positive number':
            return update.message.reply_text('Please enter a positive number')
        else:
            return update.message.reply_text(
                'Please enter valid command. eg: /open long 500')
    try:
        db = cluster[DATABASE_NAME]
        participants = db[COLLECTION_NAME1]
        stats = db[COLLECTION_NAME2]
        res = stats.find().sort("_id", pymongo.DESCENDING)[0]
        currIndexPrice = res['price']
        balance = participants.find({"username": sender})[0]
        funds = balance['funds']
        trades = balance['trades']['tradeDetails']
        if wager == "max":
            wager = balance['funds'] - 1e-09
        if wager > funds:
            raise ValueError('More than you have in your account')
        purchased = wager / currIndexPrice
        strip = datetime.now()
        date = strip.strftime('%m/%d/%Y')
        time = strip.strftime("%H:%M:%S")
        if x[1] == "short":
            trades.append(
                {"direction": x[1], "amount": wager, "date": date, "time": time})
            participants.update_one({"username": sender}, {"$set": {
                "position": {"Short": {"shares": balance['position']['Short']['shares'] + purchased, "buyIn": {"purchased": balance['position']['Short']
                                                                                                               ['buyIn']['purchased'] + purchased, "amount_spent": balance['position']['Short']
                                                                                                               ['buyIn']['amount_spent'] + wager}}, "Long": {"shares": balance['position']['Long']['shares'], "buyIn": {"purchased": balance['position']['Long']['buyIn']['purchased'], "amount_spent": balance['position']['Long']['buyIn']['amount_spent']}}}, "funds": funds - wager, "trades": {"total": balance['trades']['total'] + 1, "tradeDetails": trades}}})
            update.message.reply_text('Short position has been opened!')
        if x[1] == "long":
            trades.append(
                {"direction": x[1], "amount": wager, "date": date, "time": time})
            participants.update_one({"username": sender}, {"$set": {
                "position": {"Short": {"shares": balance['position']['Short']['shares'], "buyIn": {"purchased": balance['position']['Short']['buyIn']['purchased'], "amount_spent": balance['position']['Short']['buyIn']['amount_spent']}}, "Long": {"shares": balance['position']['Long']['shares'] + purchased, "buyIn": {"purchased": balance['position']['Long']
                                                                                                                                                                                                                                                                                                                             ['buyIn']['purchased'] + purchased, "amount_spent": balance['position']['Long']
                                                                                                                                                                                                                                                                                                                             ['buyIn']['amount_spent'] + wager}}}, "funds": funds - wager, "trades": {"total": balance['trades']['total'] + 1, "tradeDetails": trades}}})
            update.message.reply_text('Long position has been opened!')

    except Exception and ValueError as error:
        print('Cause {}'.format(error))
        update.message.reply_text('{}'.format(error))


def close(update, context):
    sender = update.message.from_user.username
    x = re.split("\s", update.message.text)
    reduction = (x[2])
    try:
        if x[2] == "max":
            reduction = "max"
        elif x[2] == None or x[1] == None or len(x) > 3:
            raise ValueError()
        else:
            if float(x[2]) < 0:
                raise ValueError('Please enter a positive number')
            reduction = float(x[2])
    except ValueError as error:
        if error == 'Please enter a positive number':
            return update.message.reply_text('Please enter a positive number')
        else:
            return update.message.reply_text(
                'Please enter valid command. eg: /close short 300')
    try:
        db = cluster[DATABASE_NAME]
        participants = db[COLLECTION_NAME1]
        stats = db[COLLECTION_NAME2]
        res = stats.find().sort("_id", pymongo.DESCENDING)[0]
        currIndexPrice = res['price'] + 50
        print(currIndexPrice)
        balance = participants.find({"username": sender})[0]
        funds = balance['funds']
        trades = balance['trades']['tradeDetails']
        strip = datetime.now()
        date = strip.strftime('%m/%d/%Y')
        time = strip.strftime("%H:%M:%S")

        if x[1] == "short":
            try:
                if balance['position']['Short']['shares'] == 0:
                    raise ValueError('You have no positions')
                avg_buy_price = balance['position']['Short']['buyIn']['amount_spent'] / \
                    balance['position']['Short']['buyIn']['purchased']
                if reduction == "max":
                    reduction = balance['position']['Short']['shares'] - 1e-09
                wager = avg_buy_price * reduction

                short_value_by_share = ((balance['position']["Short"]['shares']) * avg_buy_price +
                                (avg_buy_price - currIndexPrice) *
                                balance['position']["Short"]['shares']) / balance['position']["Short"]['shares']

                cash_out = reduction * short_value_by_share


                if math.isclose(balance['position']['Short']['shares'], reduction) == False and reduction > balance['position']['Short']['shares']:
                    raise ValueError('More than you have in your account')
                trades.append(
                    {"direction": x[1], "amount": reduction, "date": date, "time": time})
                if (reduction != balance['position']['Short']['shares'] - 1e-09):
                    participants.update_one({"username": sender}, {"$set": {
                        "position": {"Short": {"shares": balance['position']['Short']['shares'] - reduction, "buyIn": {"purchased": balance['position']['Short']['buyIn']['purchased'] - reduction, "amount_spent": balance['position']['Short']['buyIn']['amount_spent'] - wager}}, "Long": {"shares": balance['position']['Long']['shares'], "buyIn": {"purchased": balance['position']['Long']['buyIn']['purchased'], "amount_spent": balance['position']['Long']['buyIn']['amount_spent']}}}, "funds": funds + cash_out, "trades": {"total": balance['trades']['total'] + 1, "tradeDetails": trades}}})
                if (reduction == balance['position']['Short']['shares'] - 1e-09):
                    participants.update_one({"username": sender}, {"$set": {
                        "position": {"Short": {"shares": 0, "buyIn": {"purchased": 0, "amount_spent": 0}}, "Long": {"shares": balance['position']['Long']['shares'], "buyIn": {"purchased": balance['position']['Long']['buyIn']['purchased'], "amount_spent": balance['position']['Long']['buyIn']['amount_spent']}}}, "funds": funds + cash_out, "trades": {"total": balance['trades']['total'] + 1, "tradeDetails": trades}}})
                update.message.reply_text('Short position has been closed!')
            except Exception and ValueError as error:
                print('Cause {}'.format(error))
                update.message.reply_text('{}'.format(error))
        if x[1] == "long":
            try:
                if balance['position']['Long']['shares'] == 0:
                    raise ValueError('You have no positions')
                avg_buy_price = balance['position']['Long']['buyIn']['amount_spent'] / \
                    balance['position']['Long']['buyIn']['purchased']
                if reduction == "max":
                    reduction = balance['position']['Long']['shares'] - 1e-09
                wager = avg_buy_price * reduction

                long_value_by_share = (balance['position']["Long"]['shares'] * avg_buy_price +
                                (currIndexPrice - avg_buy_price) *
                                balance['position']['Long']['shares']) / balance['position']["Long"]['shares']

                cash_out = reduction * long_value_by_share

                if math.isclose(balance['position']['Long']['shares'], reduction) == False and reduction > balance['position']['Long']['shares']:
                    raise ValueError('More than you have in your account')
                trades.append(
                    {"direction": x[1], "amount": reduction, "date": date, "time": time})
                if (reduction != balance['position']['Long']['shares'] - 1e-09):
                    participants.update_one({"username": sender}, {"$set": {
                        "position": {"Short": {"shares": balance['position']['Short']['shares'], "buyIn": {"purchased": balance['position']['Short']['buyIn']['purchased'], "amount_spent": balance['position']['Short']['buyIn']['amount_spent']}}, "Long": {"shares": balance['position']['Long']['shares'] - reduction, "buyIn": {"purchased": balance['position']['Long']['buyIn']['purchased'] - reduction, "amount_spent": balance['position']['Long']['buyIn']['amount_spent'] - wager}}}, "funds": funds + cash_out, "trades": {"total": balance['trades']['total'] + 1, "tradeDetails": trades}}})
                if (reduction == balance['position']['Long']['shares'] - 1e-09):
                    participants.update_one({"username": sender}, {"$set": {
                        "position": {"Short": {"shares": balance['position']['Short']['shares'], "buyIn": {"purchased": balance['position']['Short']['buyIn']['purchased'], "amount_spent": balance['position']['Short']['buyIn']['amount_spent']}}, "Long": {"shares": 0, "buyIn": {"purchased": 0, "amount_spent": 0}}}, "funds": funds + cash_out, "trades": {"total": balance['trades']['total'] + 1, "tradeDetails": trades}}})
                update.message.reply_text('Long position has been closed!')
            except Exception and ValueError as error:
                print('Cause {}'.format(error))
                update.message.reply_text('{}'.format(error))
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
        priceUpdate, interval=86400, first=1)
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
