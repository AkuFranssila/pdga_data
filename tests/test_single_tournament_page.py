# coding=utf-8
from bs4 import BeautifulSoup
import requests
import json
import logging
import argparse
from datetime import date
from project.tournament_processes.tournament_parse_raw_data import TournamentParseRawData


def handle_arguments() -> (str):
    parser = argparse.ArgumentParser()
    parser.add_argument('--link',
        type=str,
        help="Link to a tournament page to test individual pages.",
        required=True
    )
    args = parser.parse_args()

    return args.link


def test_tournament_parsers_on_single_link(link):
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


if __name__ == "__main__":
    link = handle_arguments()
    test_tournament_parsers_on_single_link(link)