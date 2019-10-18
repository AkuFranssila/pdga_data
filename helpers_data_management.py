# coding=utf-8
import json
import logging
import sys
from datetime import date

#Class
#Contains function to open files
    #if **kwargs are list then loop through all lists


#Open & loop file(s) - DONE
#Send data to mongo
#Save file
#Find file - find_file.py

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


#Save file function
#Choose if player or tournament
#Choose if parse or crawl, and file to save
#Check that file is list of dicts
#with open('crawled_players/player_data_' + str(date.today()) + '.json', 'w') as file:
#    json.dump(player_data, file)
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
