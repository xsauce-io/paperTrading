import unittest
from controller import *
import processes.open as open
from models import *

class TestOpen(unittest.TestCase):



    def test_determine_opened_position_update(self):
        position = Position(0, 0, 0, 0, 0, 0)
        participant = Participant("Tim", 10000, 0)
        index = Index("xci", "Xsauce Culture Index", 100, "12/12/2022", "12:02:02")

        expected_position = Position(100, 0, 1.0, 0, 1.0,0)
        expected_participant = Participant("Tim", 9900, 1)
        expected_trade_detail = TradeDetails("long", 100.0, "buy", 100.0, None, None, None)

        updated_position, updated_participant, new_trade = open.determine_opened_position_update(100, "long", position, participant, index)

        self.assertEqual(repr(expected_position), repr(updated_position))
        self.assertEqual(repr(expected_participant), repr(updated_participant))
        self.assertEqual({expected_trade_detail.amount, expected_trade_detail.action, expected_trade_detail.direction}, {new_trade.amount, new_trade.action, new_trade.direction})


    def test_extract_open_message(self):
        parsed_message = ['/open' ,"xci",'long', 'max']
        expected = {"xci", "max", "long"}
        index_name , wager, direction = open.extract_open_message(parsed_message)

        self.assertEqual(expected, {index_name,wager, direction})

    def test_is_open_valid(self):
        parsed_message = ['/open' ," long",'table', '100']
        expected = False
        is_message_valid = open.is_open_message_input_valid(parsed_message)

        self.assertEqual(expected, is_message_valid)

if __name__ == '__main__':
    unittest.main()