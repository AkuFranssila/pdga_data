# coding=utf-8
import json
import logging
import os
import sys
from datetime import datetime

class FindFiles:
    def __init__(self, folder_name):
        self.folder_name = folder_name
        folders = {
            "crawled_players" : "player_data_",
            "parsed_players" : "parsed_player_data_",
            "crawled_tournaments" : "tournament_data_",
            "parsed_tournaments" : "parsed_tournament_data_"
        }
        try:
            self.file_text = folders[self.folder_name]
        except:
            sys.exit('Unable to find folder with the name mentioned')

    def days_since_today(self, file_date):
        today = str(datetime.today()).split(' ')[0]
        d1 = datetime.strptime(today, "%Y-%m-%d")
        d2 = datetime.strptime(file_date, "%Y-%m-%d")
        return abs((d2 - d1).days)

    def find_latest_file(self):
        for file in os.listdir("./" + self.folder_name):
            latest_file = ""
            crawled_since = 1000
            if file.endswith(".json"):
                file_date = file.replace(self.file_text, '').replace('.json', '')
                time_difference = self.days_since_today(file_date)
                if time_difference < crawled_since:
                    crawled_since = time_difference
                    latest_file = os.path.join(".\\" + self.folder_name, file)

        if latest_file == "":
            sys.exit('Failed to find latest file')
        else:
            return (latest_file)

    def find_all_files(self):
        all_files_in_folder = []
        for file in os.listdir("./" + self.folder_name):
            if file.endswith(".json"):
                file = os.path.join(".\\" + self.folder_name, file)
                all_files_in_folder.append(file)

        return (all_files_in_folder)

    def find_one_file(self, specific_file):
        for file in os.listdir("./" + self.folder_name):
            if file.endswith(".json") and file == specific_file:
                file = os.path.join(".\\" + self.folder_name, file)
                return (file)


#print (FindFiles('crawled_players').find_one_file("player_data_2019-09-13.json"))
