# coding=utf-8
import json
import logging
import sys
import datetime
from player.player_crawl_raw_data import PlayerCrawlRawData
from helpers.helpers_data_management import ReturnFileLocation
from utils.slack_message_sender import SendSlackMessageToChannel
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

SendSlackMessageToChannel("%s Starting run_player_crawl.py" % str(datetime.datetime.today()), "#data-reports")

#player_data = CrawlPlayer(1,100,True)
#SaveFile('player', 'crawl',  player_data)
file_loc = ReturnFileLocation("player", "crawl")
PlayerCrawlRawData(1,100, False, file_loc)
SendSlackMessageToChannel("%s Finished run_player_crawl.py. Saved crawled players to %s" % (str(datetime.datetime.today()), file_loc), "#data-reports")
