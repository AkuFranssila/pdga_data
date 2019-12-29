# coding=utf-8
import json
import logging
from datetime import date
from schemas import Player
from helpers_data_parsing import *
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


def GeneratePlayerStatistics(player):

    #player.gender = ''
    #player.date_of_birth = ''
    #player.year_of_birth = ''
    #player.age_estimate = ''
    #player.yearly_statistics = ''
    #player.played_event_ids = ''
    #player.played_countries = ''
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
    #player.highest_paid_event = '' #dynamicfield which includes course name, total_players, division name, round number, number of throws, event id, event name, final event position, round par, round rating over event rating, money won
    #player.best_round_rating = '' #dynamicfield which includes course name, total_players, division name, round number, number of throws, event id, event name, final event position, round par, round rating over event rating, money won
    #player.best_round_rating_over_rating = '' #dynamicfield which includes course name, round number, number of throws, event id, event name, final event position, round par, round rating over event rating, money won
    logging.info(player.to_json())
    #player.save()

#ParsePlayer(data)
