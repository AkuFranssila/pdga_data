# coding=utf-8
import json
import logging
from helpers_data_management import DownloadFileFromS3
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logging.info("Starting run_player_raw_data_parse.py")

file_location = DownloadFileFromS3("player-raw-data")

with open(file_location, "r") as data:
    logging.info("Opening file %s" % file_location)
    json_data = json.load(data)
    for player in json_data:
        print(player["pdga_number"])
        print(len(player["raw_data"]))

#logging.info('Finished parse - parsed ' + str(len(data_from_file)) + ' players')
