import unittest
from service import *

class TestPortfolio(unittest.TestCase):

    def test_calculate_portfolio(self):
        funds = 9900
        number_of_trades = 10
        current_index_price = 150
        position = Position(long_amount_spent=100, short_amount_spent=0, long_purchased=1,short_purchased=0, long_shares=1, short_shares=0)
        portfolio = calculate_portfolio(position,funds, number_of_trades, current_index_price )
        expected = Portfolio(funds=9900, short_shares=0, long_shares=0,long=50, short = 0, avg_buy_price_long= 100, avg_buy_price_short=0, pnl=50, number_of_trades=10 )

if __name__ == '__main__':
    unittest.main()