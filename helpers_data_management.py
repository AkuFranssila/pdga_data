# coding=utf-8
import json
import logging
import sys
import os
from datetime import date
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

def OpenFileReturnData(file):
    if isinstance(file, str):
        with open(file, 'r') as opened_file:
            data = json.load(opened_file)
        if isinstance(data[0], dict):
            return data
        else:
            sys.exit('Something went wrong when opening the file. File not list full of dicts')
    elif isinstance(file, list):
        data_from_files = []
        for i in file:
            with open(i, 'r') as opened_file:
                data = json.load(opened_file)
                data_from_files.append(data)

        combined_data = []
        for i in data_from_files:
            combined_data += i

        if isinstance(combined_data[0], dict):
            return combined_data
        else:
            sys.exit('Something went wrong when opening the file. File not list full of dicts')
    else:
        sys.exit('File format was not string or list')

def SaveFile(type, target, data):
    if not isinstance(data, list) and isintance(data[0], dict):
        sys.exit('Data in wrong format')
    today = str(date.today())
    file_location = ''
    file_name = ''
    if type == 'player' and target == 'crawl':
        file_location = 'crawled_players'
        file_name = 'player_data_'
    elif type == 'player' and target == 'parse':
        file_location = 'parsed_players'
        file_name = 'parsed_player_data_'
    elif type == 'tournament' and target == 'crawl':
        file_location = 'crawled_tournaments'
        file_name = 'tournament_data_'
    elif type == 'tournament' and target == 'parse':
        file_location = 'parsed_tournaments'
        file_name = 'parsed_tournament_data_'
    else:
        sys.exit('Wrong type or target set')

    with open(file_location + '/' + file_name + today + '.json', 'w') as file:
        json.dump(data, file)

#file = '.\\crawled_players\\player_data_2019-09-13.json'

def DeleteFile(file_location):
    if os.path.exists(file_location):
        logging.info("File at %s has been removed" % file_location)
        os.remove(file_location)
    else:
      logging.critical("The file at %s does not exist" % str(file_location))

def AppendToFile(type, target, data):
    today = str(date.today())
    file_location = ''
    file_name = ''
    if type == 'player' and target == 'crawl':
        file_location = 'crawled_players'
        file_name = 'player_raw_data_'
    elif type == 'player' and target == 'parse':
        file_location = 'parsed_players'
        file_name = 'player_parsed_data_'
    elif type == 'tournament' and target == 'crawl':
        file_location = 'crawled_tournaments'
        file_name = 'tournament_raw_data_'
    elif type == 'tournament' and target == 'parse':
        file_location = 'parsed_tournaments'
        file_name = 'tournament_parsed_data_'
    else:
        sys.exit('Wrong type or target set')

    with open(file_location + '/' + file_name + today + '.json', 'a') as file:
        json.dump(data, file)
        file.write("\n")
