# coding=utf-8
import json
import logging
import sys
from datetime import date
from player import ParsePlayer
from connect_mongodb import ConnectMongo
from schemas import Player
from player_statistics import GeneratePlayerStatistics
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


ConnectMongo()
all_players = Player.objects.filter()
for player in all_players:
    GeneratePlayerStatistics(player)

logging.info('Finished creating statistics for %s players' % (str(all_players.count())))
