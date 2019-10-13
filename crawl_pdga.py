# coding=utf-8
import json
import logging
from datetime import date
from pdga_find_latest_id import FindNewestMemberId
from pdga_player_crawler import CrawlPlayers
from send_data_to_mongo import SendData
import pymongo

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
player_data = CrawlPlayers(1,20,False)

logging.info('Number of players crawled ' + str(len(player_data)))
SendData.MultiSendPlayerData(player_data)
logging.info('Player data uploaded to MongoDB')
