import unittest
from service import calculate_long_position

class Testing(unittest.TestCase):

    def test_calculate_long_position(self):
        shares = 10
        avg_buy_price = 100
        index_price = 150
        expected = 1500
        long_position = calculate_long_position(shares, avg_buy_price, index_price)

        self.assertEqual(expected,long_position)

if __name__ == '__main__':
    unittest.main()