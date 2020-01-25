# coding=utf-8
import json
import logging
from helpers_data_management import DownloadFileFromS3, SaveFile
from player_parse_raw_data import PlayerParseRawData
from send_file_to_s3 import send_multipart_file_to_s3
from slack_message_sender import SendSlackMessageToChannel
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logging.info("Starting run_player_raw_data_parse.py")

SendSlackMessageToChannel("%s Starting run_player_raw_data_parse.py" % str(datetime.datetime.today()), "#data-reports")

file_location = DownloadFileFromS3("player-raw-data")
#file_location = '.\\crawled_players\\player-raw-data-2020-01-12.txt'
#file_location = '.\\crawled_tournaments\\tournament-raw-data-2020-01-16.txt'

all_parsed_data = []

with open(file_location, "r") as data:
    logging.info("Opening file %s" % file_location)
    for line in data:
        json_data = json.loads(line)
        id = json_data["pdga_number"]
        raw_data = json_data["raw_data"]
        parsed_data = PlayerParseRawData(id, raw_data, '')
        all_parsed_data.append(parsed_data)

saved_file_location = SaveFile("player", "parse", all_parsed_data)

send_multipart_file_to_s3(saved_file_location, "player-parsed-data")
SendSlackMessageToChannel("%s Player raw data parsed and send to S3.\n\nS3 file location: %s.\n\nNumber of tournaments parsed: %s" % (str(datetime.datetime.today(), saved_file_location, str(len(all_parsed_data)))), "#data-reports")
