import unittest
from processes import *
from models import *

class TestPortfolio(unittest.TestCase):

    def test_create_portfolio(self):
        position = Position(100, 0, 1, 0, 1, 0)
        participant = Participant("Tim", 9900, 1)
        index = Index("xci", "Xsauce Culture Index", 150, "12/12/2022", "12:02:02")

        expected = "Funds: {}\n" \
        "Short Shares: {}  \n"\
        "Long Shares: {} \n" \
        "Short: {}  \n"\
        "Long: {} \n" \
        "Avg Buy Price Short: {}  \n"\
        "Avg Buy Price Long: {} \n" \
        "PNL: {}\n" \
        "Total Trades: {}".format(9900, 0, 1 ,0, 150.0, 0, 100.0, 50.0, 1)

        portfolio_info = portfolio.determine_portfolio_by_index(position, participant, index)

        self.assertEqual(expected, repr(portfolio_info))

    def test_calculate_index_pnl(self):
        long_shares = 5
        short_shares = 0
        avg_buy_price_long = 10
        avg_buy_price_short =  10
        index_price = 20

        initial_long = long_shares * avg_buy_price_long
        initial_short = short_shares * avg_buy_price_short

        Long = portfolio.calculate_long_position(
        long_shares, avg_buy_price_long, index_price)

        Short = portfolio.calculate_short_position(
        short_shares, avg_buy_price_short, index_price)

        expected = 50

        pnl = round(portfolio.calculate_profit_and_loss(initial_long, initial_short, Long, Short))

        self.assertEqual(expected,pnl)


if __name__ == '__main__':
    unittest.main()