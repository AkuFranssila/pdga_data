# coding=utf-8
import json
import logging
import sys
from datetime import date
from crawl_player import CrawlPlayer
from helpers_data_management import SaveFile
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

player_data = CrawlPlayer(1,100,True)

SaveFile('player', 'crawl',  player_data)
