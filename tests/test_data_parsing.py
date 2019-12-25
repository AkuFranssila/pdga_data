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
        self.assertEqual(ParseFullName("Clark Kent"), ('Clark', 'Kent'))
        self.assertEqual(ParseFullName("Clark Superman Kent"), ('Clark Superman', 'Kent'))

    def test_ParseFullLocation(self):
        self.assertEqual(ParseFullLocation('Helsinki, Finland'), ('helsinki', None, 'finland'))
        self.assertEqual(ParseFullLocation('Helsinki'), ('helsinki', None, 'finland'))
        self.assertEqual(ParseFullLocation('New York'), ('new york', 'new york', 'united states'))
        self.assertEqual(ParseFullLocation('New York, NY, United States'), ('new york', 'new york', 'united states'))
        self.assertEqual(ParseFullLocation('Finland'), (None, None, 'finland'))
        self.assertEqual(ParseFullLocation('IL'), (None, 'illinois', 'united states'))
        self.assertEqual(ParseFullLocation('Gotham, IL, United States'), ('gotham', 'illinois', 'united states'))
        self.assertEqual(ParseFullLocation('United States'), (None, None, 'united states'))
        self.assertEqual(ParseFullLocation('Gotham'), (None, None, None))

    def test_ParseDate(self):
        self.assertEqual(ParseDate(None), None)
        self.assertEqual(ParseDate('01-Jan-1993'), '1993-01-01')

    def test_CheckMembershipStatus(self):
        self.assertEqual(CheckMembershipStatus(None), (None, False))
        self.assertEqual(CheckMembershipStatus('Ace Club'), ('ace club', True))
        self.assertEqual(CheckMembershipStatus('EAGLE CLUB'), ('eagle club', True))
        self.assertEqual(CheckMembershipStatus('Current'), ('current', True))
        self.assertEqual(CheckMembershipStatus(1234), ('1234', False))

    def test_ParseClassification(self):
        self.assertEqual(ParseClassification(1234), '1234')
        self.assertEqual(ParseClassification('Something here'), 'something here')
        self.assertEqual(ParseClassification('Professional'), 'professional')

    def test_ParseMemberSince(self):
        self.assertEqual(ParseMemberSince('Unknown'), 0)
        self.assertEqual(ParseMemberSince(1234), 1234)
        self.assertEqual(ParseMemberSince(None), None)

if __name__ == '__main__':
    unittest.main()
