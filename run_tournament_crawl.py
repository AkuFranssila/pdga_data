# coding=utf-8
import json
import logging
import sys
from datetime import date
from crawl_tournament import CrawlTournament
from helpers_data_management import SaveFile
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

tournament_data = CrawlTournament("all")

SaveFile('tournament', 'crawl',  tournament_data)
