# coding=utf-8
import json
import logging
import sys
from datetime import date
from pdga_player_crawler import CrawlPlayer
from helpers_data_management import SaveFile
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

player_data = CrawlPlayer(1,100,False)

SaveFile('player', 'crawl',  player_data)
