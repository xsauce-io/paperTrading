import unittest
from controller import *
import processes.open as open
from models import *

class TestOpenClose(unittest.TestCase):

    def test_close_short_position_at_index_price_(self):
        message = "/open long 100"
        position = Position(0, 0, 0, 0, 0, 0)
        participant = Participant("Tim", 10000, 0)
        index = Index(100, "12/12/2022", "12:02:02")

        expected_position = Position(100.0, 0, 1.0, 0, 1.0,0)
        expected_participant = Participant("Tim", 9900.0, 1)
        expected_trade_detail = TradeDetails("long", 100.0, "buy", 100.0, None, None, None)

        updated_position, updated_participant, new_trade = open.open_position(message, position, participant, index)

        self.assertEqual(repr(expected_position), repr(updated_position))
        self.assertEqual(repr(expected_participant), repr(updated_participant))
        self.assertEqual({expected_trade_detail.amount, expected_trade_detail.action, expected_trade_detail.direction}, {new_trade.amount, new_trade.action, new_trade.direction})
