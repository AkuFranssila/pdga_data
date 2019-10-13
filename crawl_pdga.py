# coding=utf-8
import json
import logging
import sys
from datetime import date
from pdga_player_crawler import CrawlPlayers
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

player_data = CrawlPlayers(1,20,False)
with open('crawled_players/player_data_' + str(date.today()) + '.json', 'w') as file:
    json.dump(player_data, file)
