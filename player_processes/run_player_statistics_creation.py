# coding=utf-8
import json
import logging
import sys
from datetime import date
from player_processes.player import ParsePlayer
from utils.connect_mongodb import ConnectMongo
from models.schemas import Player
from player_processes.player_statistics import GeneratePlayerStatistics
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


ConnectMongo()
all_players = Player.objects.filter()
for player in all_players:
    GeneratePlayerStatistics(player)

logging.info('Finished creating statistics for %s players' % (str(all_players.count())))
