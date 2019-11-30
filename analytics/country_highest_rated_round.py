# coding=utf-8
import sys
import json
import logging
import datetime
sys.path.append('/pdga_ratings/pdga_data')
from connect_mongodb import ConnectMongo
from schemas import Player, Tournament
from mongoengine import *
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

#collect all fi player ids to a list X
#check each tournament X
#check if tournament individual player is on the finnish player list
#check what were the round ratings for the players
#if found ratings where higher than previous highest save the info



logging.info('Starting country highest rated analytics script')
ConnectMongo()
all_pdga_numbers = []
all_country_players = Player.objects.filter(country="Finland").only("pdga_number")
for country_player = all_country_players:
    all_pdga_ids.append(country_player.pdga_number)

all_tournaments = Tournament.objects.filter().only("players", "tournament_id")

highest_round_rating = 0
player_name = ""
tournament_id = 0

logging.info(f'Highest round rating for Finland: {} for player {} in tournament with ID: {}'.format(highest_round_rating, player_name, tournament_id))

for tournament in all_tournaments:
    found_country_players = []
    for tour_player in tournament.players:
        if tour_player in all_pdga_numbers:
            found_country_players.append(tour_player)
