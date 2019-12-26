# coding=utf-8
import logging
import unittest
import sys
import os
cwd = os.getcwd()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
from helpers_data_parsing import *
from player import ParsePlayer
from mongoengine import *
from schemas import Player, Tournament

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

class TestMongoDB(unittest.TestCase):
    logging.info('Starting mongodb tests')
    @classmethod
    def setUpClass(cls):
        connect('mongoenginetest', host='mongomock://localhost')

    @classmethod
    def tearDownClass(cls):
       disconnect()

    def test_player_schema(self):
        pers = Player(full_name='John', pdga_number=1234569)
        pers.save()

        fresh_pers = Player.objects().first()
        assert fresh_pers.full_name ==  'John'


    def test_update_existing_player(self):
        player1_data = {"player_name": "Test Player", "player_pdga_number": 1, "player_id": True, "player_location_raw": "Watsonville, California, United States", "player_classification": "Professional", "player_member_since": 1976, "player_membership_status": "Eagle Club", "player_membership_expiration_date": "31-Dec-2200", "player_current_rating": 736, "player_rating_difference": None, "player_rating_updated": "15-Sep-2004", "player_events_played": 41, "player_career_wins": 8, "player_certified_status": None, "player_certified_status_expiration": None, "player_career_earnings": 602.0, "player_individual_tournament_years": [2001, 2000, 1999, 1998, 1997, 1996, 1995, 1994, 1993, 1992, 1991, 1990, 1989, 1988, 1987, 1986, 1985, 1984, 1983, 1981], "player_crawl_date": "2019-10-21"}

        ParsePlayer(player1_data)

        player1 = Player.objects(pdga_number=1).first()
        logging.info(player1.to_json())
        assert player1.full_name == 'Test Player'
        assert player1.first_name == 'Test'
        assert player1.last_name == 'Player'
        assert player1.pdga_id_status == True
        assert player1.location_full == "Watsonville, California, United States"
        assert player1.city == 'watsonville'
        assert player1.state == 'california'
        assert player1.country == 'united states'
        assert player1.classification == 'professional'
        self.assertEqual(player1.member_since, 1976)
        self.assertEqual(player1.membership_status, True)
        self.assertEqual(player1.membership_status_expiration_date, datetime.datetime(2200, 12, 31, 0, 0))

if __name__ == '__main__':
    unittest.main()
