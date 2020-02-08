# coding=utf-8
import logging
import unittest
import sys
import os
#cwd = os.getcwd()
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
from helpers.helpers_crawler import FindNewestMemberId, TournamentDate, TournamentLastPage

import pdb; pdb.set_trace()

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

class TestHelpersCrawler(unittest.TestCase):
    logging.info('Starting PDGA crawler tests')

    def test_FindNewestMemberId(self):
        latest_member_id = FindNewestMemberId()
        if latest_member_id > 100000:
            logging.info('Latest member id seems to be correct, the latest id was %s' % str(latest_member_id))

    def test_TournamentDate(self):
        logging.info('Running TournamentDate test')
        self.assertEqual(TournamentDate('all'), "https://www.pdga.com/tour/search?date_filter[min][date]=1979-01-01&date_filter[max][date]=2020-12-31")

    def test_TournamentLastPage(self):
        logging.info('Running TournamentLastPage test')

        self.assertTrue(TournamentLastPage("https://www.pdga.com/tour/search?date_filter[min][date]=2020-01-01&date_filter[max][date]=2020-12-31"))

if __name__ == '__main__':
    unittest.main()
