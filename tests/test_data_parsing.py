# coding=utf-8
import logging
import unittest
import sys
import os
cwd = os.getcwd()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
from helpers_data_parsing import *

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

class TestDataParsers(unittest.TestCase):

    def test_fullname_parser(self):
        self.assertEqual(ParseFullName("Clark Kent"), ('Clark', 'Kent'))


if __name__ == '__main__':
    unittest.main()
