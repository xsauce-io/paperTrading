import unittest
from controller import *
import processes.open as open
from models import *

class TestOpen(unittest.TestCase):


    def test_update_position(self):
        message = "/open long 100"
        position = Position(0, 0, 0, 0, 0, 0)
        participant = Participant("Tim", 10000, 0)
        index = Index(100, "12/12/2022", "12:02:02")

        expected_position = Position(100.0, 0, 1.0, 0, 1.0,0)
        expected_participant = Participant("Tim", 9900.0, 1)
        expected_trade_detail = TradeDetails("long", 100.0, "buy", 100.0, None, None, None)

        updated_position, updated_participant, new_trade = open.update_position(message, position, participant, index)

        self.assertEqual(repr(expected_position), repr(updated_position))
        self.assertEqual(repr(expected_participant), repr(updated_participant))
        self.assertEqual({expected_trade_detail.amount, expected_trade_detail.action, expected_trade_detail.direction}, {new_trade.amount, new_trade.action, new_trade.direction})


    def test_extract_open_message(self):
        message = "/open long max"
        expected = {"max", "long"}
        wager, direction = open.extract_open_message(message)

        self.assertEqual(expected, {wager, direction})

    def test_is_open_message_valid(self):
        parsed_message = ['/open' ,'table', '100']
        expected = False
        is_message_valid = open.is_open_message_valid(parsed_message)

        self.assertEqual(expected, is_message_valid)

    def test_split_message(self):
        message = "/open long 100"
        expected = ['/open', 'long', '100']
        split_message = open.split_message(message)

        self.assertEqual(expected, split_message)



    def test_calculate_portfolio(self):
        funds = 9900
    #     number_of_trades = 10
    #     current_index_price = 150
    #     position = Position(long_amount_spent=100, short_amount_spent=0, long_purchased=1,short_purchased=0, long_shares=1, short_shares=0)
    #     #portfolio = calculate_portfolio(position,funds, number_of_trades, current_index_price )
    #     #expected = Portfolio(funds=9900, short_shares=0, long_shares=0,long=50, short = 0, avg_buy_price_long= 100, avg_buy_price_short=0, pnl=50, number_of_trades=10 )

if __name__ == '__main__':
    unittest.main()