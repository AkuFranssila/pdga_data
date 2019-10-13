# coding=utf-8
import json
import logging
import urllib
import sqlite3, logging, requests
from datetime import date
from pdga_find_latest_id import FindNewestMemberId
from pdga_player_crawler import CrawlPlayers
import pymongo

#database_url = urllib.parse.quote("mongodb://aku_db:Mountain1@ds333768.mlab.com:333768/pdga?retryWrites=true&w=majority")
database_url = "mongodb://aku_db:Mountain1@ds333768.mlab.com:33768/pdga?retryWrites=false&w=majority"
client = pymongo.MongoClient(database_url)
db = client.pdga
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
#test_data = {"test" : "data"}
#import pdb; pdb.set_trace()
player_data = CrawlPlayers(1,20,False)

logging.info('Number of players crawled ' + str(len(player_data)))
db.Players.insert_many(player_data)
logging.info('Player data uploaded to MongoDB')
