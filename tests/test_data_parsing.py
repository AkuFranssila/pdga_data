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
        #self.assertEqual(ParseFullLocation('Helsinki', recheck=True), ('helsinki', None, 'finland'))
        #self.assertEqual(ParseFullLocation('New York', recheck=True), ('new york', 'new york', 'united states'))
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

        test_data = {"player_membership_status": None}
        self.assertEqual(CheckAndNormalizeMembershipStatus(test_data), None)

        test_data = {"player_membership_status": 'Ace Club'}
        self.assertEqual(CheckAndNormalizeMembershipStatus(test_data), 'ace club')

        test_data = {"player_membership_status": 'EAGLE CLUB'}
        self.assertEqual(CheckAndNormalizeMembershipStatus(test_data), 'eagle club')

        test_data = {"player_membership_status": "Current"}
        self.assertEqual(CheckAndNormalizeMembershipStatus(test_data), 'current')

        test_data = {"player_membership_status": 1234}
        self.assertEqual(CheckAndNormalizeMembershipStatus(test_data), '1234',)

    def test_ParseClassification(self):

        test_data = {'player_classification': 1234}
        self.assertEqual(ParseClassification(test_data), '1234')

        test_data = {'player_classification': 'Something here'}
        self.assertEqual(ParseClassification(test_data), 'something here')

        test_data = {'player_classification': 'Professional'}
        self.assertEqual(ParseClassification(test_data), 'professional')

    def test_ParseMemberSince(self):
        test_data = {'player_member_since': 'Unknown'}
        self.assertEqual(ParseMemberSince(test_data), None)

        test_data = {'player_member_since': 1234}
        self.assertEqual(ParseMemberSince(test_data), 1234)

        test_data = {'player_member_since': None}
        self.assertEqual(ParseMemberSince(test_data), None)

if __name__ == '__main__':
    unittest.main()
