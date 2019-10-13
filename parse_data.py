# coding=utf-8
import json
import logging
import os
from datetime import datetime
#Open crawled_players
#loop through the files
#Check which one is the newest file
    #get current date
    #get time delta for each file
    #parse the file with smallest time delta
class LatestJsonFile:
    def __init__(self, folder_name):
        self.folder_name = folder_name
        if self.folder_name == "crawled_players":
            self.file_text = "player_data_"
        elif self.folder_name == "parsed_players":
            self.file_text = "parsed_player_data_"
        elif self.folder_name == "crawled_tournaments":
            self.file_text = "tournament_data_"
        elif self.folder_name == "parsed_tournaments":
            self.file_text = "parsed_tournament_data_"
        else:
            sys.exit('Unable to find folder with the name mentioned')

    def days_since_today(date):
        today = str(datetime.today()).split(' ')[0]
        d1 = datetime.strptime(today, "%Y-%m-%d")
        d2 = datetime.strptime(date, "%Y-%m-%d")
        return abs((d2 - d1).days)

    def find_latest_file(self):
        for file in os.listdir("./" + self.folder_name):
            latest_file = ""
            crawled_since = 1000
            if file.endswith(".json"):
                file_date = file.replace(self.file_text, '').replace('.json', '')
                time_difference = days_since_today(self, file_date)
                if time_difference < crawled_since:
                    crawled_since = time_difference
                    latest_file = os.path.join(".\\crawled_players", file)

        if latest_file == "":
            sys.exit('Failed to find latest file')
        else:
            return (latest_file)
a = LatestJsonFile('crawled_players')
print (a.folder_name)

import pdb; pdb.set_trace()
print ('lol')
