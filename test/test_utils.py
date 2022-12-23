import unittest
from controller import *
import helpers.utils as utils
from models import *

class TestUtils(unittest.TestCase):

     def test_split_message(self):
        message = "/open long 100"
        expected = ['/open', 'long', '100']
        split_message = utils.split_message(message)

        self.assertEqual(expected, split_message)

if __name__ == '__main__':
    unittest.main()