# coding=utf-8
import json
import logging
import datetime
import argparse
import subprocess
from project.utils.connect_mongodb import ConnectMongo
from project.tournament_processes.tournament_parse_raw_data import TournamentParseRawData
from project.utils.s3_tools import find_all_keys_from_s3_folder, download_file_from_s3_return_file_path, save_to_temp_file_and_upload_to_s3
from project.utils.slack_message_sender import SendSlackMessageToChannel
from project.models.schemas import Tournament
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logging.info("Starting run_tournament_raw_data_parse.py")

def handle_arguments() -> (str):
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_date',
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
    parser.add_argument('--index',
        type=int,
        help="Index key if you want to start parsing from different key. Files in order the keys are downloaded from S3.",
    )
    args = parser.parse_args()

    return args.file_date, args.send, args.statistics, args.clear_updated_fields, args.index



def run_parse_raw_data_and_send_to_mongo(file_date, send, statistics, clear_updated_fields, starting_index=0):
    SendSlackMessageToChannel("%s Starting run_parse_raw_data_and_send_to_mongo.py" % str(datetime.datetime.today()), "#data-reports")
    all_file_keys = find_all_keys_from_s3_folder(f"tournament-raw-data/{file_date}")
    logging.info("Found %s keys" % str(len(all_file_keys)))


    for file_key in all_file_keys[starting_index:]:
        SendSlackMessageToChannel(("Starting to parse file %s" % (file_key)), "#data-reports")
        output_msg = ""
        try:
            output_msg = subprocess.check_output(['python', '-m', 'project.tournament_processes.tournament_parse_and_mongo', '--s3_key', file_key, '--send', '--statistics', '--clear_updated_fields', '--file_date', file_date])
        except subprocess.CalledProcessError:
            SendSlackMessageToChannel("File %s failed with error %s" % (file_key, str(output_msg)), "#data-reports")


    ConnectMongo()
    total = Tournament.objects().count()
    logging.info("Finished parse_raw_data_and_send_to_mongo.py")
    SendSlackMessageToChannel("%s Finished run_parse_raw_data_and_send_to_mongo.py Currently %s tournaments in MongoDB." % (str(datetime.datetime.today()), str(total)), "#data-reports")



if __name__ == "__main__":
    file_date, send, statistics, clear_updated_fields, starting_index = handle_arguments()
    run_parse_raw_data_and_send_to_mongo(file_date, send, statistics, clear_updated_fields, starting_index)