import requests
import os
from dotenv import load_dotenv

load_dotenv()

API = os.environ['api']


def calculateJordanIndex():
    try:
        skus = ["555088-117",
                "136064-123",
                "378037-003",
                "308497-100",
                "845035-003",
                "CD4487-100",
                "378037-061",
                "AV9175-001",
                "378037-117",
                "AA3834-101"]

        resData = []

        for sku in skus:
            sneak_url = API + sku
            response = requests.get(sneak_url)

            resData.append(response.json()[
                'results'][0]['estimatedMarketValue'])

        culture = 0
        culture += resData[0] * .02
        culture += resData[1] * .02
        culture += resData[2] * .02
        culture += resData[3] * .02
        culture += resData[4] * .02
        culture += resData[5] * .02
        culture += resData[6] * .02
        culture += resData[7] * .02
        culture += resData[8] * .02
        culture += resData[9] * .02

        return culture

    except Exception as error:
        print(error)


def calculateNikeIndex():
    try:
        skus = ["315121-115/CW2290-111",
                "BQ6817-006",
                "AA3830-002",
                "318429-660",
                "314996-001",
                "AH8050-100",
                "884421-001",
                "616750-001",
                "CU3244-100",
                "DD1391-100"]

        resData = []

        for sku in skus:
            sneak_url = API + sku
            response = requests.get(sneak_url)

            resData.append(response.json()[
                'results'][0]['estimatedMarketValue'])

        culture = 0
        culture += resData[0] * .02
        culture += resData[1] * .02
        culture += resData[2] * .02
        culture += resData[3] * .02
        culture += resData[4] * .02
        culture += resData[5] * .02
        culture += resData[6] * .02
        culture += resData[7] * .02
        culture += resData[8] * .02
        culture += resData[9] * .02

        return culture

    except Exception as error:
        print(error)


def calculateYeezyIndex():
    try:
        skus = ["CP9654",
                "GW1934",
                "B75571",
                "HP8739",
                "EG6462",
                "FW5191",
                "DB2908",
                "AH8050-100",
                "GX6144",
                "H03665"]

        resData = []

        for sku in skus:
            sneak_url = API + sku
            response = requests.get(sneak_url)

            resData.append(response.json()[
                'results'][0]['estimatedMarketValue'])

        culture = 0
        culture += resData[0] * .02
        culture += resData[1] * .02
        culture += resData[2] * .02
        culture += resData[3] * .02
        culture += resData[4] * .02
        culture += resData[5] * .02
        culture += resData[6] * .02
        culture += resData[7] * .02
        culture += resData[8] * .02
        culture += resData[9] * .02

        return culture

    except Exception as error:
        print(error)


def calculateAdidasIndex():
    try:
        skus = ["GZ9256",
                "BB7802",
                "GY9693",
                "GZ9177",
                "H01877",
                "M20324",
                "EE7582",
                "FX3239",
                "HP6772",
                "FY9120"]

        resData = []

        for sku in skus:
            sneak_url = API + sku
            response = requests.get(sneak_url)

            resData.append(response.json()[
                'results'][0]['estimatedMarketValue'])

        culture = 0
        culture += resData[0] * .02
        culture += resData[1] * .02
        culture += resData[2] * .02
        culture += resData[3] * .02
        culture += resData[4] * .02
        culture += resData[5] * .02
        culture += resData[6] * .02
        culture += resData[7] * .02
        culture += resData[8] * .02
        culture += resData[9] * .02

        return culture

    except Exception as error:
        print(error)


def calculateNewBalanceIndex():
    try:
        skus = ["BB550PB/BB550PB1",
                "ML574EGG",
                "M990JD3",
                "MR993ALD",
                "CM997HZH",
                "U9060JF1",
                "MR993GL",
                "M990SB2",
                "M990GL5",
                "MS997JBG"]

        resData = []

        for sku in skus:
            sneak_url = API + sku
            response = requests.get(sneak_url)
            resData.append(response.json()[
                'results'][0]['estimatedMarketValue'])

        culture = 0
        culture += resData[0] * .02
        culture += resData[1] * .02
        culture += resData[2] * .02
        culture += resData[3] * .02
        culture += resData[4] * .02
        culture += resData[5] * .02
        culture += resData[6] * .02
        culture += resData[7] * .02
        culture += resData[8] * .02
        culture += resData[9] * .02

        return culture

    except Exception as error:
        print(error)

def calculateSP50Index():
    try:
        jordanIndex = calculateJordanIndex()
        NikeIndex = calculateNikeIndex()
        YeezyIndex = calculateYeezyIndex()
        AdidasIndex =calculateAdidasIndex()
        NewBalanceIndex = calculateNewBalanceIndex()

        culture = 0
        culture += jordanIndex * .2
        culture += NikeIndex * .2
        culture += YeezyIndex * .2
        culture += AdidasIndex * .2
        culture += NewBalanceIndex * .2

        print("S&P 50 Price :" + " "+ str(culture))
        return culture

    except Exception as error:
        print(error)


def main():
    calculateSP50Index()

if __name__ == '__main__':
    main()
