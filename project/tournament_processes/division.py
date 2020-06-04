# coding=utf-8
import json
import logging
from datetime import date
from project.models.schemas import *
from mongoengine import *
from project.utils.connect_mongodb import ConnectMongo
from project.helpers.helpers_data_parsing import *
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


def ParseDivisions(data):
    #ConnectMongo()
    all_divisions = []
    all_pdga_numbers = []
    for div in data['event_divisions']:
        division = Division()
        division.name = ParseDivisionFullName(div['division_name'])
        division.short_name = div['division_short_name']
        division.type = data["event_type"][0]
        division.team_size = CheckTeamSize(div['division_players'])
        division.total_players = ParseDivisionTotalPlayers(div["division_total_players"])
        division.rounds = []
        all_players = div['division_players']

        for count, round in enumerate(div['division_course_details']):
            divisionround = DivisionRound()
            divisionround.round_number = count + 1
            divisionround.course_name, divisionround.course_layout, divisionround.course_holes, divisionround.course_par, divisionround.course_pdga_page, divisionround.course_length_meters, divisionround.course_length_feet = ParseCourseDetails(round['round_' + str(count + 1)]['course_details'], round['round_' + str(count + 1)]['course_pdga_link'])

            divisionround.course_avg_hole_par = CalculateAverageFromTwoFields(divisionround.course_par, divisionround.course_holes)
            divisionround.course_avg_hole_length_meters = CalculateAverageFromTwoFields(divisionround.course_length_meters, divisionround.course_holes)
            divisionround.course_avg_hole_length_feet = CalculateAverageFromTwoFields(divisionround.course_length_feet, divisionround.course_holes)
            division.rounds.append(divisionround)

        parsed_players = []
        for player in all_players:
            divisionplayer = DivisionPlayer()

            divisionplayer.full_name = player.get("player_full_names")
            divisionplayer.pdga_number = player.get("player_pdga_number")
            divisionplayer.pdga_page = player.get("player_pdga_link")
            divisionplayer.propagator = player.get("player_propagator")
            divisionplayer.rating_during_tournament = player.get("player_rating_during_tournament")
            divisionplayer.rounds_with_results = ParseTournamentRoundsWithResults(player)

            divisionplayer.final_placement = ParseTournamentPlacement(player['player_final_placement'])
            divisionplayer.money_won = ParseTournamentWinnings(player['player_money_won'])
            divisionplayer.total_throws, dnf_found, dns_found = ParseTournamentTotalThrows(player['player_total_throws'])
            divisionplayer.total_par, dnf_found, dns_found = ParseTournamentPar(player["player_total_par"], dnf_found, dns_found) #funk player_total_par
            divisionplayer.event_points = ParseTournamentPoints(player["player_event_points"])
            divisionplayer.dns = dns_found
            divisionplayer.dnf = dnf_found
            divisionplayer.rounds = []
            for round in player['player_rounds']:
                r = PlayerRound()
                r.round_number = round['round_number']
                r.round_throws, r.dnf = ParsePlayerRoundThrows(round['round_throws'], r.dnf)
                r.round_rating = ParsePlayerRoundRating(round['round_rating'])
                r.dns = False
                r.avg_throw_length_meters = PlayerRoundAvgThrowLength(division.rounds, r.round_throws, r.round_number, type="meters")
                r.avg_throw_length_feet = PlayerRoundAvgThrowLength(division.rounds, r.round_throws, r.round_number, type="feet")
                r.round_par = PlayerRoundPar(division.rounds, r.round_throws, r.round_number)
                r.avg_throws_per_hole = PlayerRoundAvgThrowsPerHole(division.rounds, r.round_throws, r.round_number)
                divisionplayer.rounds.append(r)

            divisionplayer.total_throws = FillTotalThrowsIfEmpty(divisionplayer.total_throws, divisionplayer.rounds)

            divisionplayer.avg_throws_per_round = CalculateAvgFromRounds(divisionplayer.total_throws, divisionplayer.rounds_with_results)
            divisionplayer.avg_par_per_round = CalculateAvgFromRounds(divisionplayer.total_par, divisionplayer.rounds_with_results)
            divisionplayer.avg_round_rating = CalculateAvgRoundRating(divisionplayer.rounds)
            divisionplayer.avg_throw_length_meters = CalculatePlayerTournamentAvgThrowLenght(divisionplayer.rounds, type="meters")
            divisionplayer.avg_throw_length_feet = CalculatePlayerTournamentAvgThrowLenght(divisionplayer.rounds, type="feet")
            divisionplayer.total_holes_played = CalculateTotalHolesPlayed(divisionplayer.rounds, division.rounds)
            divisionplayer.avg_throws_per_hole = CalculateAverageFromTwoFields(divisionplayer.total_throws, divisionplayer.total_holes_played)
            divisionplayer.players_avg_round_rating_difference_to_rating_during_tournament = CalculateDifferenceFromTwoFields(divisionplayer.avg_round_rating, divisionplayer.rating_during_tournament[0])
            
            if divisionplayer.pdga_number:
                for number in divisionplayer.pdga_number:
                    all_pdga_numbers.append(number)

            parsed_players.append(divisionplayer)

        division.players = parsed_players

        UpdateDivisionRoundDetails(division.rounds, division.players)
        CheckPlayerRoundDetails(division)
        UpdateDivisionDetails(division)

        #Statistics left to be calculated
        #player round tournament_placement
        all_divisions.append(division)
        
    return all_divisions, all_pdga_numbers
