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

    def test_ParseFullName(self):
        logging.info('Testing ParseFullName')
        self.assertEqual(ParseFullName("Clark Kent"), ('Clark', 'Kent'))
        self.assertEqual(ParseFullName("Clark Superman Kent"), ('Clark Superman', 'Kent'))

    def test_ParseFullLocation(self):
        logging.info('Testing ParseFullLocation')
        #Returns city, state, country
        self.assertEqual(ParseFullLocation('Helsinki, Finland'), ('Helsinki', None, 'Finland'))
        self.assertEqual(ParseFullLocation('Helsinki'), ('Helsinki', None, 'Finland'))
        self.assertEqual(ParseFullLocation('New York'), ('New York', 'New York', 'United States'))
        self.assertEqual(ParseFullLocation('New York, NY, United States'), ('New York', 'New York', 'United States'))
        self.assertEqual(ParseFullLocation('Finland'), (None, None, 'Finland'))
        self.assertEqual(ParseFullLocation('IL'), (None, 'Illinois', 'United States'))
        self.assertEqual(ParseFullLocation('Gotham, IL, United States'), ('Gotham', 'Illinois', 'United States'))
        self.assertEqual(ParseFullLocation('United States'), (None, None, 'United States'))
        self.assertEqual(ParseFullLocation('Gotham'), (None, None, None))

if __name__ == '__main__':
    unittest.main()
