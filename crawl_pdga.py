# coding=utf-8
import json
import logging
import sys
from datetime import date
from pdga_player_crawler import CrawlPlayers
from helpers_data_management import SaveFile
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

player_data = CrawlPlayers(21,40,False)

SaveFile('player', 'crawl',  player_data)
