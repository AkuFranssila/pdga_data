# coding=utf-8
import json
import logging
import sys
from datetime import date
from tournament import ParseTournament
from helpers_data_management import SaveFile, OpenFileReturnData
from find_file import FindFiles
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


latest_file = FindFiles('crawled_tournaments').find_latest_file()
data_from_file = OpenFileReturnData(latest_file)

for data in data_from_file:
    ParseTournament(data)

logging.info('Finished parse - parsed ' + str(len(data_from_file)) + ' tournaments')
