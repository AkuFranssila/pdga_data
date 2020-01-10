# coding=utf-8
import json
import logging
import sys
import os
import re
from datetime import date, datetime
from aws_s3_client import AWS_S3CLIENT
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

def ReturnFileLocation(type, target):

    types = ["old_pdga_data", "player-parsed-data", "player-raw-data", "tournament-parsed-data", "tournament-raw-data"]
    today = str(date.today())
    if type == 'player' and target == 'crawl':
        file_location = 'crawled_players'
        file_name = 'player-raw-data-'
    elif type == 'player' and target == 'parse':
        file_location = 'parsed_players'
        file_name = 'player-parsed-data-'
    elif type == 'tournament' and target == 'crawl':
        file_location = 'crawled_tournaments'
        file_name = 'tournament-raw-data-'
    elif type == 'tournament' and target == 'parse':
        file_location = 'parsed_tournaments'
        file_name = 'tournament-parsed-data-'
    else:
        sys.exit('Wrong type or target set')

    return file_location + '/' + file_name + today + '.json'

def FindLatestFileFromS3(type):
    s3 = AWS_S3CLIENT()

    if type not in ["old_pdga_data", "player-parsed-data", "player-raw-data", "tournament-parsed-data", "tournament-raw-data"]:
        sys.exit('Type not in the predefined types')

    files = s3.list_objects_v2(Bucket="pdga-project-data", Prefix=type)["Contents"]

    newest_file_key = ""
    newest_file_date = ""
    for f in files:
        date_from_filename = re.findall(r'([0-9]{4}-[0-9]{2}-[0-9]{2})', str(f))

        if len(date_from_filename) > 0:
            logging.info("Current key: %s" % newest_file_key)
            logging.info("Current date: %s" % newest_file_date)
            if newest_file_date == "":
                newest_file_date = date_from_filename[0]
                newest_file_key = f["Key"]
            else:
                year, month, date = newest_file_date.split("-")
                newest_file_date_datetime = datetime(int(year), int(month), int(date))

                year, month, date = date_from_filename[0].split('-')
                current_file_datetime = datetime(int(year), int(month), int(date))
                if current_file_datetime > newest_file_date_datetime:
                    newest_file_date = date_from_filename[0]
                    newest_file_key = f["Key"]

    return newest_file_key


def DownloadFileFromS3(type):
    if type not in ["old_pdga_data", "player-parsed-data", "player-raw-data", "tournament-parsed-data", "tournament-raw-data"]:
        sys.exit('Type not in the predefined types')

    type_to_location = {"old_pdga_data" : "old_pdga_data",
                        "player-parsed-data" : "parsed_players",
                        "player-raw-data" : "crawled_players",
                        "tournament-parsed-data" : "parsed_tournaments",
                        "tournament-raw-data" : "crawled_tournaments"
                        }

    folder_name = type_to_location[type]
    key = FindLatestFileFromS3(type)
    file_name = key.split("/")[-1]
    save_location = '.\\' + folder_name + '\\' + file_name

    s3 = AWS_S3CLIENT()
    logging.info("Trying to find file %s from S3 and saving it to %s" % (key, save_location))
    s3.download_file('pdga-project-data', key, save_location)
