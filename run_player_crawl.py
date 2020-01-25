# coding=utf-8
import json
import logging
import sys
from datetime import date
from player_crawl_raw_data import PlayerCrawlRawData
from helpers_data_management import ReturnFileLocation
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

#player_data = CrawlPlayer(1,100,True)
#SaveFile('player', 'crawl',  player_data)
file_loc = ReturnFileLocation("player", "crawl")
PlayerCrawlRawData(1,1000, False, file_loc)
