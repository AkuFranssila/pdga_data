# coding=utf-8
import json
import logging
import datetime
from player_processes.player import ParsePlayer
from utils.connect_mongodb import ConnectMongo
from utils.slack_message_sender import SendSlackMessageToChannel
from models.schemas import Player
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logging.info("Starting run_player_to_mongo.py")

SendSlackMessageToChannel("%s Starting run_player_to_mongo.py" % str(datetime.datetime.today()), "#data-reports")

file_location = DownloadFileFromS3("player-parsed-data")
#file_location = '.\\parsed_players\\player-parsed-data-2020-01-25.json'

ConnectMongo()
with open(file_location, "r") as data:
    all_players = json.load(data)
    for player in all_players:
        ParsePlayer(player)


total_players = Player.objects().count()
logging.info("Finished run_player_to_mongo.py")
SendSlackMessageToChannel("%s Finished run_player_to_mongo.py. Currently %s players in MongoDB." % (str(datetime.datetime.today()), str(total_players)), "#data-reports")
