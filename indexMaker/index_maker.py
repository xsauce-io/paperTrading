import requests
import os
from dotenv import load_dotenv
from constituents_store import *

load_dotenv()

API = os.environ['api']


def calculate_index_price(constituents: list) -> float:
    index_price = 0
    try:
        for constituent in constituents:
            sku = constituent['sku']
            weight_in_decimal = constituent['weight_in_decimal']
            sneak_url = API + sku
            response = requests.get(sneak_url)

            print(response.json()['results'][0]['name'])
            estimates_market_value = float(response.json()[
                'results'][0]['estimatedMarketValue'])
            print(estimates_market_value)
            index_price += estimates_market_value * weight_in_decimal
            print(index_price)

        print()

        return index_price
    except Exception as error:
        print(error)


def calculate_composite_index_price(composite_of_constituents: list) -> float:
    index_price = 0

    try:
        for composite in composite_of_constituents:
            constituents = composite['constituent']
            weight_in_decimal = composite['weight_in_decimal']
            name = composite['name']

            sub_index_price = calculate_index_price(constituents)

            index_price += sub_index_price * weight_in_decimal
            print(index_price)

    except Exception as error:
        print(error)



    except Exception as error:
        print(error)


def main():
    # calculate_index_price(CULTURE_INDEX_CONSTITUENTS)
    calculate_composite_index_price(SNEAKER_SP50_INDEX_CONSTITUENTS)



if __name__ == '__main__':
    main()
