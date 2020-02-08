# coding=utf-8
import logging
import unittest
import sys
import os
cwd = os.getcwd()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
from helpers.helpers_data_parsing import *
from player.player import ParsePlayer
from mongoengine import connect, disconnect
from models.schemas import Player, Tournament

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

class TestPlayer(unittest.TestCase):
    logging.info('Starting mongodb player schema tests')
    @classmethod
    def setUpClass(cls):
        connect('mongoenginetest', host='mongomock://localhost')

    @classmethod
    def tearDownClass(cls):
       disconnect()

    def test_create_and_update_player(self):
        player1_data = {"player_name": "Test Player", "player_pdga_number": 1, "player_id": True, "player_location_raw": "Watsonville, California, United States", "player_classification": "Professional", "player_member_since": 1976, "player_membership_status": "Eagle Club", "player_membership_expiration_date": "31-Dec-2200", "player_current_rating": 736, "player_rating_difference": None, "player_rating_updated": "15-Sep-2004", "player_events_played": 41, "player_career_wins": 8, "player_certified_status": None, "player_certified_status_expiration": None, "player_career_earnings": 602.0, "player_individual_tournament_years": [2001, 2000, 1999, 1998, 1997, 1996, 1995, 1994, 1993, 1992, 1991, 1990, 1989, 1988, 1987, 1986, 1985, 1984, 1983, 1981], "player_crawl_date": "2019-10-21"}

        ParsePlayer(player1_data)

        player1 = Player.objects(pdga_number=1).first()
        logging.info(player1.to_json())
        logging.info(player1.latest_rating_update)
        logging.info(player1.first_crawl_date)
        logging.info(player1.latest_update)
        first_crawl = player1.first_crawl_date
        updated_date = str(player1.latest_update).split(' ')[0]
        self.assertEqual(player1.full_name, 'Test Player')
        self.assertEqual(player1.first_name, 'Test')
        self.assertEqual(player1.last_name, 'Player')
        self.assertEqual(player1.pdga_id_status, True)
        self.assertEqual(player1.location_full, "Watsonville, California, United States")
        self.assertEqual(player1.city, 'watsonville')
        self.assertEqual(player1.state, 'california')
        self.assertEqual(player1.country, 'united states')
        self.assertEqual(player1.classification, 'professional')
        self.assertEqual(player1.gender, None)
        self.assertEqual(player1.date_of_birth, None)
        self.assertEqual(player1.member_since, 1976)
        self.assertEqual(player1.membership_status, True)
        self.assertEqual(player1.membership_status_expiration_date, datetime.datetime(2200, 12, 31, 0, 0))
        self.assertEqual(player1.membership, 'eagle club')
        self.assertEqual(player1.rating_difference, None)
        self.assertEqual(player1.current_rating, 736)
        self.assertEqual(player1.lowest_rating, 736)
        self.assertEqual(player1.highest_rating, 736)
        self.assertEqual(player1.latest_rating_update, datetime.datetime(2004, 9, 15, 0, 0))
        self.assertEqual(player1.total_events, 41)
        self.assertEqual(player1.total_wins, 8)
        self.assertEqual(player1.certified_status, False)
        self.assertEqual(player1.career_earnings, 602.0)
        self.assertEqual(player1.yearly_statistics, [])
        self.assertEqual(player1.individual_tournament_years, [2001, 2000, 1999, 1998, 1997, 1996, 1995, 1994, 1993, 1992, 1991, 1990, 1989, 1988, 1987, 1986, 1985, 1984, 1983, 1981])
        self.assertEqual(player1.pdga_page_link, 'https://www.pdga.com/player/1')
        self.assertEqual(player1.played_event_ids, [])
        self.assertEqual(player1.played_countries, [])
        #self.assertEqual(player1.first_crawl_date, '')
        #self.assertEqual(player1.latest_update, '')
        #self.assertEqual(player1.fields_updated, [{"new_data": ["full_name", "first_name", "last_name", "pdga_number", "pdga_id_status", "location_full", "city", "state", "country", "classification", "member_since", "membership_status", "membership_status_expiration_date", "membership", "current_rating", "highest_rating", "lowest_rating", "latest_rating_update", "total_events", "total_wins", "certified_status", "career_earnings", "individual_tournament_years", "pdga_page_link", "played_event_ids", "played_countries", "players_played_with_in_same_tournament", "players_played_with_in_same_divisions", "yearly_statistics", "first_crawl_date", "latest_update", "fields_updated"], "modified_data": {}, "removed_data": [], "updated_date": updated_date}])

        player1_updated_data = {"player_name": "Test Player", "player_pdga_number": 1, "player_id": True, "player_location_raw": "Gotham, Batville, Imagination", "player_classification": "Amateur", "player_member_since": 1976, "player_membership_status": "Current", "player_membership_expiration_date": "31-Dec-2200", "player_current_rating": 836, "player_rating_difference": 100, "player_rating_updated": "16-Sep-2004", "player_events_played": 99, "player_career_wins": 10, "player_certified_status": 'Certified', "player_certified_status_expiration": "31-Dec-2200", "player_career_earnings": 802.0, "player_individual_tournament_years": [2001, 2000, 1999, 1998, 1997, 1996, 1995, 1994, 1993, 1992, 1991, 1990, 1989, 1988, 1987, 1986, 1985, 1984, 1983, 1981], "player_crawl_date": "2019-10-21"}

        ParsePlayer(player1_updated_data)

        player1 = Player.objects(pdga_number=1).first()
        logging.info(player1.to_json())
        logging.info(player1.latest_rating_update)
        logging.info(player1.first_crawl_date)
        logging.info(player1.latest_update)
        logging.info(player1.fields_updated)
        updated_date = str(player1.latest_update).split(' ')[0]
        self.assertEqual(player1.full_name, 'Test Player')
        self.assertEqual(player1.first_name, 'Test')
        self.assertEqual(player1.last_name, 'Player')
        self.assertEqual(player1.pdga_id_status, True)
        self.assertEqual(player1.location_full, "Gotham, Batville, Imagination")
        self.assertEqual(player1.city, 'gotham')
        self.assertEqual(player1.state, 'batville')
        self.assertEqual(player1.country, 'imagination')
        self.assertEqual(player1.gender, None)
        self.assertEqual(player1.date_of_birth, None)
        self.assertEqual(player1.classification, 'amateur')
        self.assertEqual(player1.member_since, 1976)
        self.assertEqual(player1.membership_status, True)
        self.assertEqual(player1.membership_status_expiration_date, datetime.datetime(2200, 12, 31, 0, 0))
        self.assertEqual(player1.membership, 'current')
        self.assertEqual(player1.rating_difference, 100)
        self.assertEqual(player1.current_rating, 836)
        self.assertEqual(player1.lowest_rating, 736)
        self.assertEqual(player1.highest_rating, 836)
        self.assertEqual(player1.latest_rating_update, datetime.datetime(2004, 9, 16, 0, 0))
        self.assertEqual(player1.total_events, 99)
        self.assertEqual(player1.total_wins, 10)
        self.assertEqual(player1.certified_status, True)
        self.assertEqual(player1.career_earnings, 802.0)
        self.assertEqual(player1.yearly_statistics, [])
        self.assertEqual(player1.individual_tournament_years, [2001, 2000, 1999, 1998, 1997, 1996, 1995, 1994, 1993, 1992, 1991, 1990, 1989, 1988, 1987, 1986, 1985, 1984, 1983, 1981])
        self.assertEqual(player1.pdga_page_link, 'https://www.pdga.com/player/1')
        self.assertEqual(player1.played_event_ids, [])
        self.assertEqual(player1.played_countries, [])
        self.assertEqual(player1.first_crawl_date, first_crawl)
        #self.assertEqual(player1.latest_update, '')
        #self.assertEqual(player1.fields_updated, [{'new_data': ['full_name', 'first_name', 'last_name', 'pdga_number', 'pdga_id_status', 'location_full', 'city', 'state', 'country', 'classification', 'member_since', 'membership_status', 'membership_status_expiration_date', 'membership', 'current_rating', 'highest_rating', 'lowest_rating', 'latest_rating_update', 'total_events', 'total_wins', 'certified_status', 'career_earnings', 'yearly_statistics', 'individual_tournament_years', 'pdga_page_link', 'played_event_ids', 'played_countries', 'first_crawl_date', 'latest_update', 'fields_updated'], 'modified_data': {}, 'removed_data': [], 'updated_date': updated_date}, {'new_data': [], 'modified_data': {}, 'removed_data': [], 'updated_date': updated_date}])

if __name__ == '__main__':
    unittest.main()
