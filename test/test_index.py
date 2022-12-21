import unittest
from service import *

class TestIndex(unittest.TestCase):

    def test_format_index_price(self):

        index = Index(100.99999, "12/10/2000", "11:43:34")
        index_formatted = format_index_price(index)
        expected = {101.00, "12/10/2000", "11:43:34"}
        self.assertEqual(expected, {index_formatted.price, index.date, index.time})

if __name__ == '__main__':
    unittest.main()