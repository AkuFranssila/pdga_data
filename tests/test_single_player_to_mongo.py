# coding=utf-8
from bs4 import BeautifulSoup
import requests
import json
import logging
import argparse
from datetime import date
from project.utils.connect_mongodb import ConnectMongo
from project.player_processes.player_parse_raw_data import PlayerParseRawData
from project.player_processes.player import ParsePlayer


def handle_arguments() -> (str):
    parser = argparse.ArgumentParser()
    parser.add_argument('--link',
        type=str,
        help="Link to player PDGA profile.",
        required=True
    )
    parser.add_argument('--send',
        action="store_true",
        help="Send data, defaults to False",
    )
    parser.add_argument('--statistics',
        action="store_true",
        help="Send data, defaults to False",
    )
    args = parser.parse_args()

    return args.link, args.send, args.statistics


def test_player_to_mongo_on_single_link(link, send, statistics):
    all_data = []
    all_parsed_data = []
    response = requests.get(link)
    data = response.content.decode('utf8').replace("'", '"')
    json_data = {"pdga_number" : int(link.rsplit("/", 1)[1]), "raw_data" : data}
    all_data.append(json_data)
    for page in all_data:
        id = page["pdga_number"]
        raw_data = page["raw_data"]
        parsed_data = PlayerParseRawData(id, raw_data)
        all_parsed_data.append(parsed_data)

    print(json.dumps(all_parsed_data, indent=4))

    ConnectMongo()
    for player in all_parsed_data:
        ParsePlayer(player, send_data=send, generate_statistics=statistics)



if __name__ == "__main__":
    link, send, statistics = handle_arguments()
    test_player_to_mongo_on_single_link(link, send, statistics)