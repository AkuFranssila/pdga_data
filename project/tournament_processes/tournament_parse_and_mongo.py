import argparse
import logging
import json
from project.utils.s3_tools import find_all_keys_from_s3_folder, download_file_from_s3_return_file_path, save_to_temp_file_and_upload_to_s3
from project.tournament_processes.tournament import ParseTournament
from project.tournament_processes.tournament_parse_raw_data import TournamentParseRawData

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

def handle_arguments() -> (str):
    parser = argparse.ArgumentParser()
    parser.add_argument('--s3_key',
        type=str,
        help="S3 folder name that is date in format YearMonthDay",
        required=False
    )
    parser.add_argument('--send',
        action="store_true",
        help="Send data, defaults to False",
    )
    parser.add_argument('--statistics',
        action="store_true",
        help="Argument if statistics should be created. By default statistics are not created.",
    )
    parser.add_argument('--clear_updated_fields',
        action="store_true",
        help="Argument if updated_fields should be cleaned. By default fields are not cleared.",
    )
    parser.add_argument('--file_date',
        type=str,
        help="S3 folder name that is date in format YearMonthDay",
        required=False
    )
    args = parser.parse_args()

    return args.s3_key, args.send, args.statistics, args.clear_updated_fields, args.file_date


def parse_raw_data_and_send_to_mongo(s3_key, send, statistics, clear_updated_fields, file_date):
    file_counter = s3_key.split('.json')[0].split('data_')[1]
    download_name = f"data_{file_counter}"
    if not file_date:
        file_date = s3_key.split('/')[1].split('/')[0]
    file_path = download_file_from_s3_return_file_path(s3_key, download_name)

    all_parsed_data = []
    with open(file_path, "r") as data:
        logging.info("Opening file %s" % file_path)
        all_data = json.load(data)
        for page in all_data:
            id = page["pdga_number"]
            raw_data = page["raw_data"]
            parsed_data = TournamentParseRawData(id, raw_data)
            ParseTournament(parsed_data, send, statistics, clear_updated_fields)
            all_parsed_data.append(parsed_data)

        save_to_temp_file_and_upload_to_s3("tournament-parsed-data", file_date, file_counter, all_parsed_data)


if __name__ == "__main__":
    s3_key, send, statistics, clear_updated_fields, file_date = handle_arguments()
    parse_raw_data_and_send_to_mongo(s3_key, send, statistics, clear_updated_fields, file_date)