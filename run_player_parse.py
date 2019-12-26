# coding=utf-8
import json
import logging
import sys
from datetime import date
from player import ParsePlayer
from connect_mongodb import ConnectMongo
from helpers_data_management import SaveFile, OpenFileReturnData
from find_file import FindFiles
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


latest_file = FindFiles('crawled_players').find_latest_file()
data_from_file = OpenFileReturnData(latest_file)

ConnectMongo()
for data in data_from_file:
    ParsePlayer(data)

logging.info('Finished parse - parsed ' + str(len(data_from_file)) + ' players')
