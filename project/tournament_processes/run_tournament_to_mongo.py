# coding=utf-8
import json
import logging
import datetime
import argparse
from project.tournament_processes.tournament import ParseTournament
from project.utils.connect_mongodb import ConnectMongo
from project.utils.s3_tools import find_all_keys_from_s3_folder, download_file_from_s3_return_file_path
from project.utils.slack_message_sender import SendSlackMessageToChannel
from project.models.schemas import Tournament
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logging.info("Starting run_tournament_to_mongo.py")


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


def RunTournamentToMongo(file_date, send, statistics, clear_updated_fields, starting_index=0):

    SendSlackMessageToChannel("%s Starting run_tournament_to_mongo.py" % str(datetime.datetime.today()), "#data-reports")

    all_file_keys = find_all_keys_from_s3_folder(f"tournament-parsed-data/{file_date}")

    for file_key in all_file_keys[starting_index:]:
        file_counter = file_key.split('.json')[0].split('data_')[1]
        download_name = f"data_{file_counter}"

        file_path = download_file_from_s3_return_file_path(file_key, download_name)

        ConnectMongo()
        with open(file_path, "r") as data:
            all_tournaments = json.load(data)
            for tournament in all_tournaments:
                if tournament:
                    ParseTournament(tournament, send, statistics, clear_updated_fields)


    total = Tournament.objects().count()
    logging.info("Finished run_tournament_to_mongo.py")
    SendSlackMessageToChannel("%s Finished run_tournament_to_mongo.py. Currently %s players in MongoDB." % (str(datetime.datetime.today()), str(total)), "#data-reports")


if __name__ == "__main__":
    file_date, send, statistics, clear_updated_fields, start_index = handle_arguments()
    RunTournamentToMongo(file_date, send, statistics, clear_updated_fields, start_index)