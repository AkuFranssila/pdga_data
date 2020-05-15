# coding=utf-8
import json
import logging
import datetime
from project.helpers.helpers_data_management import DownloadFileFromS3, SaveFile
from project.tournament_processes.tournament_parse_raw_data import TournamentParseRawData
from project.utils.send_file_to_s3 import send_multipart_file_to_s3
from project.utils.slack_message_sender import SendSlackMessageToChannel
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logging.info("Starting run_tournament_raw_data_parse.py")
SendSlackMessageToChannel("%s Starting run_tournament_raw_data_parse.py" % str(datetime.datetime.today()), "#data-reports")

#file_location = DownloadFileFromS3("tournament-raw-data")
file_location = '.\\project\\crawled_tournaments\\tournament-raw-data-2020-01-16.txt'

all_parsed_data = []

with open(file_location, "r") as data:
    logging.info("Opening file %s" % file_location)
    for line in data:
        json_data = json.loads(line)
        pdga_number = json_data["pdga_number"]
        raw_data = json_data["raw_data"]
        parsed_data = TournamentParseRawData(pdga_number, raw_data, '')
        all_parsed_data.append(parsed_data)

saved_file_location = SaveFile("tournament", "parse", all_parsed_data)
#saved_file_location = ""


logging.info("Sending parsed tournament data to S3")
send_multipart_file_to_s3(saved_file_location, "tournament-parsed-data")
SendSlackMessageToChannel("%s Tournament raw data parsed and send to S3.\n\nS3 file location: %s.\n\nNumber of tournaments parsed: %s" % (str(datetime.datetime.today()), saved_file_location, str(len(all_parsed_data))), "#data-reports")
logging.info("Finished tournament raw data parsing. Parsed %s tournaments" % str(len(all_parsed_data)))
