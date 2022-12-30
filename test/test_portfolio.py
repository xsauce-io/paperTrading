import unittest
from controller import *
import processes.portfolio as portfolio
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

if __name__ == '__main__':
    unittest.main()