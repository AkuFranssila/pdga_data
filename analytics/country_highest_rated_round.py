# coding=utf-8
import sys
import json
import logging
import datetime
sys.path.append('/pdga_ratings/pdga_data')
from utils.connect_mongodb import ConnectMongo
from models.schemas import Player, Tournament
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
all_country_players = Player.objects.filter(country="united states").only("pdga_number")
for country_player in all_country_players:
    all_pdga_numbers.append(country_player.pdga_number)

all_tournaments = Tournament.objects.filter().only("players", "tournament_id")

highest_round_rating = 0
player_id = 0
tournament_id = 0

dict = {}

same_round_rating = []

logging.info(f'Highest round rating for Finland: {str(highest_round_rating)} for player {str(player_id)} in tournament with ID: {str(tournament_id)}')

for count, tournament in enumerate(all_tournaments):
    logging.info(f'Checking tournament number {str(count)}')
    logging.info(f'Tournament ID is {str(tournament.tournament_id)}')
    found_country_players = []
    for tour_player in tournament.players:
        if tour_player in all_pdga_numbers:
            found_country_players.append(tour_player)

    if len(found_country_players) > 0:
        t = Tournament.objects.filter(tournament_id=tournament.tournament_id).first()

        logging.info(f'Found {str(len(found_country_players))} Finnish players in this tournament')
        for div in t.divisions:
            for p in div.players:
                if p.pdga_number_1 in found_country_players:
                    for r in p.rounds:
                        if r.round_rating is not None:
                            if len(dict.keys()) < 11:
                                dict[r.round_rating] = {"tournament": t.tournament_name, "player_name": p.full_name_1, "pdga_number": p.pdga_number_1, "year": str(t.tournament_start).split('-')[0], "round_number": str(r.round_number)}
                            elif r.round_rating < 1500:
                                dict[r.round_rating] = {"tournament": t.tournament_name, "player_name": p.full_name_1, "pdga_number": p.pdga_number_1, "year": str(t.tournament_start).split('-')[0], "round_number": str(r.round_number)}
                                lowest_key = sorted(dict)[0]
                                highest_key = sorted(dict)[-1]
                                dict.pop(lowest_key)
                                print(json.dumps(dict[highest_key], indent=4))


                            # if r.round_rating == highest_round_rating:
                            #     same_round_rating.append(p.pdga_number_1)
                            #     logging.info('New same highest round rating found.')
                            # elif r.round_rating > highest_round_rating and r.round_rating < 1400:
                            #     tournament_id = t.tournament_id
                            #     player_id = p.pdga_number_1
                            #     highest_round_rating = r.round_rating
                            #     same_round_rating = []
                            #     logging.info(f'Highest round rating for Finland: {str(highest_round_rating)} for player {str(player_id)} in tournament with ID: {str(tournament_id)}')


print(json.dumps(dict, indent=4))
