import unittest
from controller.controller import *
import processes.close as close
from models import *


class TestClose(unittest.TestCase):

    def test_update_position(self):
        position = Position(100.0, 0, 1.0, 0, 1.0,0)
        participant = Participant("Tim", 9900, 0)
        index = Index("xci", "Xsauce Culture Index", 100, "12/12/2022", "12:02:02")

        expected_position = Position(0.0, 0, 0.0, 0, 0.0,0)
        expected_participant = Participant("Tim", 10000.0, 1)
        expected_trade_detail = TradeDetails("long", 1, "sell", 100.0, None, None, None)

        updated_position, updated_participant, new_trade = close.determine_closed_position_update(1, "long", position, participant, index)

        self.assertEqual(repr(expected_position), repr(updated_position))
        self.assertEqual(repr(expected_participant), repr(updated_participant))
        #Note the time is not being tested
        self.assertEqual({expected_trade_detail.amount, expected_trade_detail.action, expected_trade_detail.direction}, {new_trade.amount, new_trade.action, new_trade.direction})

    def test_update_position_more_than_in_account(self):
        position = Position(100.0, 0, 1.0, 0, 1.0,0)
        participant = Participant("Tim", 99000, 0)
        index = Index("xci", "Xsauce Culture Index", 100, "12/12/2022", "12:02:02")

        with self.assertRaises(UserInputException) as context:
            close.determine_closed_position_update(100, "long", position, participant, index)
        self.assertEqual('More than you have in your account', str(context.exception))

    def test_extract_close_message(self):
        parsed_message = ['/close' ,'table','short', 'max']
        expected = {"table", "max", "short"}
        reduction, wager, direction = close.extract_close_message(parsed_message)

        self.assertEqual(expected, {reduction, wager, direction})

    def test_is_close_input_valid(self):
        parsed_message = ['/close' ,'xci','short', '100']
        expected = True
        is_message_valid = close.is_close_message_input_valid(parsed_message)

        self.assertEqual(expected, is_message_valid)

    def test_is_close_format_valid(self):
        parsed_message = ['/close' ,'xci','short', '100']
        expected = True
        is_message_valid = close.is_close_message_format_valid(parsed_message)

        self.assertEqual(expected, is_message_valid)

if __name__ == '__main__':
    unittest.main()