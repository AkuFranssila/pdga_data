# coding=utf-8
import json
import logging
from datetime import date
from project.models.schemas import Player
from project.helpers.helpers_data_parsing import *
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


def GeneratePlayerStatistics(player):

    womens_divisions = ['FPO', 'FP40', 'FP50', 'FP55', 'FP60', 'FP65', 'FP70', 'FA1', 'FA2', 'FA3', 'FA4', 'FA40', 'FA50', 'FA55', 'FA60', 'FA65', 'FA70', 'FJ18', 'FJ15', 'FJ12', 'FJ10', 'FJ08', 'FJ06']
    junior_divisions = ['MJ18', 'MJ15', 'MJ12', 'MJ10', 'MJ08', 'MJ06']
    players_same_tournament = {}
    players_same_division = {}
    played_tournament_ids = []
    played_tournament_countries = []
    played_tournament_states = []
    played_tournament_cities = []
    tournaments_as_td = []
    tournaments_as_assistant_td = []
    singles = 0
    doubles = 0
    teams = 0
    dnf = 0
    dns = 0
    #Find all tournament Ids that the player has played in
    all_tournaments = Tournament.objects(players=player.pdga_number)

    logging.info('Player %s, with pdga number %s has played in %s tournaments' % (player.full_name, str(player.pdga_number), str(all_tournaments.count())))
    for tournament in all_tournaments:
        logging.info(json.dumps(json.loads(tournament.to_json()), indent=4))
        #import pdb; pdb.set_trace()
        if "tournament_director_id" in tournament:
            if tournament.tournament_director_id == player.pdga_number and tournament.tournament_id not in tournaments_as_td:
                tournaments_as_td.append(tournament.tournament_id)

        if "assistant_director_id" in tournament:
            if tournament.assistant_director_id == player.pdga_number and tournament.tournament_id not in tournaments_as_assistant_td:
                tournaments_as_assistant_td.append(tournament.tournament_id)

        if tournament.tournament_id not in played_tournament_ids:
            played_tournament_ids.append(tournament.tournament_id)

        if "location_country" in tournament:
            if tournament.location_country not in played_tournament_countries:
                played_tournament_countries.append(tournament.location_country)

        if "location_state" in tournament:
            if tournament.location_state not in played_tournament_states:
                played_tournament_states.append(tournament.location_state)

        if "location_city" in tournament:
            if tournament.location_city not in played_tournament_cities:
                played_tournament_cities.append(tournament.location_city)

        if "tournament_type" in tournament:
            if tournament.tournament_type == "singles":
                singles += 1
            elif tournament.tournament_type == "doubles":
                doubles += 1
            elif tournament.tournament_type == "team":
                teams += 1

        for player_id in tournament.players:
            try:
                players_same_tournament[player_id] += 1
            except KeyError:
                players_same_tournament[player_id] = 1

        """
        Data points that need to be collected from the division and rounds the player has played in the tournament
        player.dns_count
        player.dnf_count
        player.players_played_with_in_same_divisions
        player.total_throws
        player.total_points
        player.top_five_placements
        player.top_ten_placements
        player.total_rounds_played
        player.tournaments_played_per_division
        player.tournaments_played_per_tier
        """

        for division in tournament.divisions:
            import pdb; pdb.set_trace()
            if player.full_name in division.to_json():
                import pdb; pdb.set_trace()




    ###############################
    #Fields that can be updated only after checking every tournament
    #player.current_rating = '' #if player is inactive we can get the current rating from the last tournament the player played
    #player.gender = ''
    #player.date_of_birth = ''
    #player.year_of_birth = ''
    #player.age_estimate = ''
    #player.yearly_statistics = ''
    #player.avg_position = ''
    #player.avg_par = ''
    #player.avg_throw_length_feet = ''
    #player.avg_throw_length_meters = ''
    #player.avg_earnings_per_tournament = ''
    #player.highest_paid_event = '' #dynamicfield which includes course name, total_players, division name, round number, number of throws, event id, event name, final event position, round par, round rating over event rating, money won
    #player.best_round_rating = '' #dynamicfield which includes course name, total_players, division name, round number, number of throws, event id, event name, final event position, round par, round rating over event rating, money won
    #player.best_round_rating_over_rating = '' #dynamicfield which includes course name, round number, number of throws, event id, event name, final event position, round par, round rating over event rating, money won

    ###############################
    #Fields that need to be updated when checking each tournament
    #DONE #player.events_as_td = ''
    #DONE #player.events_as_assistant_td = ''
    #DONE #player.played_event_ids = ''
    #DONE #player.played_countries = ''
    #DONE #player.played_states = ''
    #DONE #player.played_cities = ''
    #DONE #player.singles_played = ''
    #DONE #player.doubles_played = ''
    #DONE #player.teams_played = ''
    #player.dns_count = ''
    #player.dnf_count = ''
    #DONE #player.players_played_with_in_same_tournament = '' #list of unique player ids that the player has played with in same tournaments
    #player.players_played_with_in_same_divisions = '' #list of unique player ids that the player has played with in same tournaments and same divisions
    #player.total_throws = ''
    #player.total_points = ''
    #player.top_five_placements = ''
    #player.top_ten_placements = ''
    #player.total_rounds_played = ''
    #player.tournaments_played_per_division = '' #dynamicfield division name, number events played
    #player.tournaments_played_per_tier = '' #dynamicfield tier code, number events played
    logging.info(player.to_json())
    #player.save()

#ParsePlayer(data)
