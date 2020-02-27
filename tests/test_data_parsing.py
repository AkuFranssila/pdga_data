# coding=utf-8
import logging
import unittest
import sys
import os
cwd = os.getcwd()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
from project.helpers.helpers_data_parsing import *
from project.models.schemas import Player, Tournament

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

class TestDataParsers(unittest.TestCase):

    def test_ParseFullName(self):

        test_data1 = {"player_name": "Clark Kent"}
        test_data2 = {"player_name": "Clark Superman Kent"}
        self.assertEqual(ParsePlayerFullName(test_data1), ('Clark', None, 'Kent'))
        self.assertEqual(ParsePlayerFullName(test_data2), ('Clark Superman', None, 'Kent'))

    def test_ParseFullLocation(self):
        self.assertEqual(ParseFullLocation('Helsinki, Finland', recheck=True), ('helsinki', None, 'finland'))
        self.assertEqual(ParseFullLocation('Helsinki', recheck=True), ('helsinki', None, 'finland'))
        self.assertEqual(ParseFullLocation('New York', recheck=True), ('new york', 'new york', 'united states'))
        self.assertEqual(ParseFullLocation('New York, NY, United States', recheck=True), ('new york', 'new york', 'united states'))
        self.assertEqual(ParseFullLocation('Finland', recheck=True), (None, None, 'finland'))
        self.assertEqual(ParseFullLocation('IL', recheck=True), (None, 'illinois', 'united states'))
        self.assertEqual(ParseFullLocation('Gotham, IL, United States', recheck=True), ('gotham', 'illinois', 'united states'))
        self.assertEqual(ParseFullLocation('United States', recheck=True), (None, None, 'united states'))
        self.assertEqual(ParseFullLocation('Gotham', recheck=True), (None, None, None))

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
