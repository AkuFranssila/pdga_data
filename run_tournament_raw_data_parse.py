# coding=utf-8
import json
import logging
from helpers_data_management import DownloadFileFromS3, SaveFile
from tournament_parse_raw_data import TournamentParseRawData
from send_file_to_s3 import send_multipart_file_to_s3
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logging.info("Starting run_tournament_raw_data_parse.py")


file_location = DownloadFileFromS3("tournament-raw-data")

all_parsed_data = []

with open(file_location, "r") as data:
    logging.info("Opening file %s" % file_location)
    for line in data:
        json_data = json.loads(line)
        id = json_data["pdga_number"]
        raw_data = json_data["raw_data"]
        parsed_data = TournamentParseRawData(id, raw_data, '')
        all_parsed_data.append(parsed_data)

saved_file_location = SaveFile("tournament", "parse", all_parsed_data)

logging.info("Sending parsed tournament data to S3")
send_multipart_file_to_s3(saved_file_location, "tournament-parsed-data")
logging.info("Finished tournament raw data parsing. Parsed %s tournaments" % str(len(all_parsed_data)))
