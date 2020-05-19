# coding=utf-8
import json
import logging
import datetime
import argparse
from project.tournament_processes.tournament_parse_raw_data import TournamentParseRawData
from project.utils.s3_tools import find_all_keys_from_s3_folder, download_file_from_s3_return_file_path, save_to_temp_file_and_upload_to_s3
from project.utils.slack_message_sender import SendSlackMessageToChannel
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logging.info("Starting run_tournament_raw_data_parse.py")

def handle_arguments() -> (str):
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_date',
        type=str,
        help="S3 folder name that is date in format YearMonthDay",
        required=False
    )
    args = parser.parse_args()

    return args.file_date


def RunTournamentRawDataParse(file_date):
    SendSlackMessageToChannel("%s Starting run_tournament_raw_data_parse.py" % str(datetime.datetime.today()), "#data-reports")

    all_file_keys = find_all_keys_from_s3_folder(f"tournament-raw-data/{file_date}")

    logging.info("Found %s keys" % str(len(all_file_keys)))

    for file_key in all_file_keys:
        file_counter = file_key.split('.json')[0].split('data_')[1]
        download_name = f"data_{file_counter}"

        file_path = download_file_from_s3_return_file_path(file_key, download_name)

        all_parsed_data = []
        with open(file_path, "r") as data:
            logging.info("Opening file %s" % file_path)
            all_data = json.load(data)
            for page in all_data:
                id = page["pdga_number"]
                raw_data = page["raw_data"]
                parsed_data = TournamentParseRawData(id, raw_data)
                all_parsed_data.append(parsed_data)


        save_to_temp_file_and_upload_to_s3("tournament-parsed-data", file_date, file_counter, all_parsed_data)


if __name__ == "__main__":
    file_date = handle_arguments()
    RunTournamentRawDataParse(file_date)
