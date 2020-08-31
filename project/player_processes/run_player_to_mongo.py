# coding=utf-8
import json
import logging
import datetime
import argparse
import subprocess
from project.player_processes.player import ParsePlayer
from project.utils.connect_mongodb import ConnectMongo
from project.utils.slack_message_sender import SendSlackMessageToChannel
from project.utils.s3_tools import find_all_keys_from_s3_folder, download_file_from_s3_return_file_path
from project.models.schemas import Player
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logging.info("Starting run_player_to_mongo.py")


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
    args = parser.parse_args()

    return args.file_date, args.send, args.statistics, args.clear_updated_fields


def run_player_to_mongo(file_date, send, statistics, clear_updated_fields, starting_index=0):

    SendSlackMessageToChannel("%s Starting run_player_to_mongo.py" % str(datetime.datetime.today()), "#data-reports")

    all_file_keys = find_all_keys_from_s3_folder(f"player-parsed-data/{file_date}")

    for file_key in all_file_keys[starting_index:]:
        SendSlackMessageToChannel(("Starting to parse file %s" % (file_key)), "#data-reports")
        try:
            subprocess.check_output(['python', '-m', 'project.player_processes.player', '--s3_key', file_key, '--send', '--statistics', '--clear_updated_fields'])
        except subprocess.CalledProcessError as e:
            SendSlackMessageToChannel("File %s failed with error %s" % (file_key, str(e.output)), "#data-reports")

    ConnectMongo()
    total = Player.objects().count()
    logging.info("Finished run_player_to_mongo.py")
    SendSlackMessageToChannel("%s Finished run_player_to_mongo.py. Currently %s players in MongoDB." % (str(datetime.datetime.today()), str(total)), "#data-reports")


if __name__ == "__main__":
    file_date, send, statistics, clear_updated_fields = handle_arguments()
    run_player_to_mongo(file_date, send, statistics, clear_updated_fields)