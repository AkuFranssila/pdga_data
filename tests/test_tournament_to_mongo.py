# coding=utf-8
from bs4 import BeautifulSoup
import requests
import json
import logging
import argparse
from datetime import date
from project.tournament_processes.tournament import ParseTournament
from project.utils.connect_mongodb import ConnectMongo
from project.tournament_processes.tournament_parse_raw_data import TournamentParseRawData


def handle_arguments() -> (str):
    parser = argparse.ArgumentParser()
    parser.add_argument('--link',
        type=str,
        help="Link to a tournament page to test individual pages.",
        required=True
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

    return args.link, args.send, args.statistics, args.clear_updated_fields



def test_tournament_to_mongo_on_single_link(link, send, statistics, clear_updated_fields):
    all_data = []
    all_parsed_data = []
    response = requests.get(link)
    data = response.content.decode('utf8').replace("'", '"')
    json_data = {"pdga_number" : int(link.rsplit("/", 1)[1]), "raw_data" : data}
    all_data.append(json_data)
    for page in all_data:
        id = page["pdga_number"]
        raw_data = page["raw_data"]
        parsed_data = TournamentParseRawData(id, raw_data)
        all_parsed_data.append(parsed_data)


    print(json.dumps(all_parsed_data, indent=4))
    ConnectMongo()
    for tournament in all_parsed_data:
        ParseTournament(tournament, send, statistics, clear_updated_fields)


if __name__ == "__main__":
    link, send, statistics, clear_updated_fields = handle_arguments()
    test_tournament_to_mongo_on_single_link(link, send, statistics, clear_updated_fields)