import unittest
from processes import *
from models import *

class TestOpenClose(unittest.TestCase):


    #TODO: refactor
    def test_close_short_position_at_index_price_(self):
        #Close
        message = "/open long 100"
        position = Position(0, 0, 0, 0, 0, 0)
        participant = Participant("Tim", 10000, 0)
        index = Index("xci", "Xsauce Culture Index",100, "12/12/2022", "12:02:02")

        expected_position = Position(100, 0, 1.0, 0, 1.0,0)
        expected_participant = Participant("Tim", 9900, 1)
        expected_trade_detail = TradeDetails("long", 100.0, "buy", 100.0, None, None, None)

        updated_position, updated_participant, new_trade = open.determine_opened_position_update(100, "long", position, participant, index)

        self.assertEqual(repr(expected_position), repr(updated_position))
        self.assertEqual(repr(expected_participant), repr(updated_participant))
        self.assertEqual({expected_trade_detail.amount, expected_trade_detail.action, expected_trade_detail.direction}, {new_trade.amount, new_trade.action, new_trade.direction})

        #portfolio
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

        #Close
        message = "/close long 1"
        position = Position(100.0, 0, 1.0, 0, 1.0,0)
        participant = Participant("Tim", 9900, 0)
        index = Index("xci", "Xsauce Culture Index", 150, "12/12/2022", "12:02:02")

        expected_position = Position(0.0, 0, 0.0, 0, 0.0,0)
        expected_participant = Participant("Tim", 10050.0, 1)
        expected_trade_detail = TradeDetails("long", 1, "sell", 150.0, None, None, None)

        updated_position, updated_participant, new_trade = close.determine_closed_position_update(1, "long", position, participant, index)

        self.assertEqual(repr(expected_position), repr(updated_position))
        self.assertEqual(repr(expected_participant), repr(updated_participant))
        #Note the time is not being tested
        self.assertEqual({expected_trade_detail.amount, expected_trade_detail.action, expected_trade_detail.direction}, {new_trade.amount, new_trade.action, new_trade.direction})
