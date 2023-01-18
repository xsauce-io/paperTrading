import requests
import os
from dotenv import load_dotenv
import controller
from models import *
from helpers.utils import *

load_dotenv()

API = os.environ['api']


def calculate_index_price(constituents: list, index_name) -> float:
    index_price = 0
    try:
        for constituent in constituents:
            sku = constituent['sku']
            weight_in_decimal = constituent['weight_in_decimal']
            sneak_url = API + sku
            response = requests.get(sneak_url)

            name = response.json()['results'][0]['name']
            print(name)
            estimates_market_value = float(response.json()[
                'results'][0]['estimatedMarketValue'])
            print(estimates_market_value)
            index_price += estimates_market_value * weight_in_decimal
            print(index_price)

            date,time = get_current_date_time()

            asset = Sneaker(name, "skeaker", sku, estimates_market_value, date, time, index_name)
            controller.add_asset_statistic(asset)

        return index_price
    except Exception as error:
        print(error)


def calculate_composite_index_price(composite_of_constituents: list, index_name) -> float:
    index_price = 0

    try:
        for composite in composite_of_constituents:
            constituents = composite['constituent']
            weight_in_decimal = composite['weight_in_decimal']
            name = composite['name']

            sub_index_price = calculate_index_price(constituents, index_name)

            index_price += sub_index_price * weight_in_decimal

            print(index_price)
        return index_price

    except Exception as error:
        print(error)
