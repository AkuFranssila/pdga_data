# coding=utf-8
import json
import logging
import sys
from datetime import date
from tournament.tournament_crawl_raw_data import TournamentCrawlRawData
from helpers.helpers_data_management import SaveFile, ReturnFileLocation
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

file_loc = ReturnFileLocation("tournament", "crawl")
tournament_data = TournamentCrawlRawData("all", file_loc)
