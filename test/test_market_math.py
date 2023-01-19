import unittest
from controller.controller import *
from helpers import *
from models import *

class TestMarketMath(unittest.TestCase):

    def test_calculate_short_position(self):
        shares = 10
        avg_buy_price = 100
        index_price = 150
        expected = 500
        short_shares_value = calculate_short_position(shares, avg_buy_price, index_price)
        self.assertEqual(expected, short_shares_value)

    def test_calculate_long_position(self):
        shares = 10
        avg_buy_price = 100
        index_price = 150
        expected = 1500
        long_shares_value = calculate_long_position(shares, avg_buy_price, index_price)

        self.assertEqual(expected,long_shares_value)

    def test_calculate_average_buy_price(self):
        amount_spent = 200
        shares_purchased = 2
        expected = 100
        avg_buy_price = calculate_average_buy_price(amount_spent, shares_purchased)

        self.assertEqual(expected, avg_buy_price)

if __name__ == '__main__':
    unittest.main()