# coding=utf-8
import json
import logging
from datetime import date
from schemas import Player
from helpers_data_parsing import *
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


def GeneratePlayerStatistics(player):

    womens_divisions = ['FPO', 'FP40', 'FP50', 'FP55', 'FP60', 'FP65', 'FP70', 'FA1', 'FA2', 'FA3', 'FA4', 'FA40', 'FA50', 'FA55', 'FA60', 'FA65', 'FA70', 'FJ18', 'FJ15', 'FJ12', 'FJ10', 'FJ08', 'FJ06']
    junior_divisions = ['MJ18', 'MJ15', 'MJ12', 'MJ10', 'MJ08', 'MJ06']
    played_tournament_ids = []
    played_tournament_countries = []
    tournaments_as_td = []
    tournaments_as_assistant_td = []
    #Find all tournament Ids that the player has played in
    all_tournaments = Tournament.objects.filter(players=player.pdga_number)

    logging.info('Player %s, with pdga number %s has played in %s tournaments' % (player.full_name, str(player.pdga_number), str(all_tournaments.count())))
    for tournament in all_tournaments:
        logging.info(json.dumps(json.loads(tournament.to_json()), indent=4))
        import pdb; pdb.set_trace()
    #player.gender = ''
    #player.date_of_birth = ''
    #player.year_of_birth = ''
    #player.age_estimate = ''
    #player.yearly_statistics = ''
    #player.events_as_td = ''
    #player.events_as_assistant_td = ''
    #player.played_event_ids = ''
    #player.played_countries = ''
    #player.singles_played = ''
    #player.doubles_played = ''
    #player.teams_played = ''
    #player.dns_count = ''
    #player.dnf_count = ''
    #player.players_played_with_in_same_tournament = '' #list of unique player ids that the player has played with in same tournaments
    #player.players_played_with_in_same_divisions = '' #list of unique player ids that the player has played with in same tournaments and same divisions
    #player.total_throws = ''
    #player.top_five_placements = ''
    #player.top_ten_placements = ''
    #player.total_rounds_played = ''
    #player.avg_position = ''
    #player.avg_par = ''
    #player.avg_throw_length_feet = ''
    #player.avg_throw_length_meters = ''
    #player.avg_earnings_per_tournament = ''
    #player.tournaments_played_per_division = '' #dynamicfield division name, number events played
    #player.tournaments_played_per_tier = '' #dynamicfield tier code, number events played
    #player.highest_paid_event = '' #dynamicfield which includes course name, total_players, division name, round number, number of throws, event id, event name, final event position, round par, round rating over event rating, money won
    #player.best_round_rating = '' #dynamicfield which includes course name, total_players, division name, round number, number of throws, event id, event name, final event position, round par, round rating over event rating, money won
    #player.best_round_rating_over_rating = '' #dynamicfield which includes course name, round number, number of throws, event id, event name, final event position, round par, round rating over event rating, money won
    logging.info(player.to_json())
    #player.save()

#ParsePlayer(data)
