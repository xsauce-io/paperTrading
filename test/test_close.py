import unittest
from controller import *
import processes.close as close
from models import *


class TestClose(unittest.TestCase):

    def test_update_position(self):
        message = "/close long 1"
        position = Position(100.0, 0, 1.0, 0, 1.0,0)
        participant = Participant("Tim", 9900, 0)
        index = Index(100, "12/12/2022", "12:02:02")

        expected_position = Position(0.0, 0, 0.0, 0, 0.0,0)
        expected_participant = Participant("Tim", 10000.0, 1)
        expected_trade_detail = TradeDetails("long", 1, "sell", 100.0, None, None, None)

        updated_position, updated_participant, new_trade = close.close_position(message, position, participant, index)

        self.assertEqual(repr(expected_position), repr(updated_position))
        self.assertEqual(repr(expected_participant), repr(updated_participant))
        #Note the time is not being tested
        self.assertEqual({expected_trade_detail.amount, expected_trade_detail.action, expected_trade_detail.direction}, {new_trade.amount, new_trade.action, new_trade.direction})

    def test_update_position_more_than_in_account(self):
        message = "/close long 100"
        position = Position(100.0, 0, 1.0, 0, 1.0,0)
        participant = Participant("Tim", 99000, 0)
        index = Index(100, "12/12/2022", "12:02:02")

        with self.assertRaises(ValueError) as context:
            close.close_position(message, position, participant, index)
        self.assertEqual('More than you have in your account', str(context.exception))

    def test_extract_close_message(self):
        message = "/open long max"
        expected = {"max", "long"}
        wager, direction = close.extract_close_message(message)

        self.assertEqual(expected, {wager, direction})

    def test_is_close_message_valid(self):
        parsed_message = ['/open' ,'table', '100']
        expected = False
        is_message_valid = close.is_close_message_valid(parsed_message)

        self.assertEqual(expected, is_message_valid)

if __name__ == '__main__':
    unittest.main()