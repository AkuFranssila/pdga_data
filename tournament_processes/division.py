# coding=utf-8
import json
import logging
from datetime import date
from schemas import *
from mongoengine import *
from utils.connect_mongodb import ConnectMongo
from helpers.helpers_data_parsing import *
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


def ParseDivisions(data):
    #ConnectMongo()
    all_divisions = []
    all_pdga_numbers = []
    for div in data['event_divisions']:
        #print (div)
        division = Division()
        division.name = ParseDivisionFullName(div['division_name'])
        division.short_name = div['division_short_name']
        division.type = data["event_type"][0]
        division.total_players = ParseDivisionTotalPlayers(div["division_total_players"])
        division.rounds = []
        try:
            all_players = div['division_players_singles']
        except:
            try:
                all_players = div['division_players_doubles']
            except:
                all_players = div['division_players_team']

        for count, round in enumerate(div['division_course_details']):
            divisionround = DivisionRound()
            divisionround.round_number = count + 1
            divisionround.course_name, divisionround.course_layout, divisionround.course_holes, divisionround.course_par, divisionround.course_pdga_page, divisionround.course_length_meters, divisionround.course_length_feet = ParseCourseDetails(round['round_' + str(count + 1)]['course_details'], round['round_' + str(count + 1)]['course_pdga_link'])
            division.rounds.append(divisionround)

        parsed_players = []
        for player in all_players:
            divisionplayer = DivisionPlayer()
            divisionplayer.full_name_1, divisionplayer.full_name_2 = ParseTournamentPlayerName(data["event_type"][0], player)
            divisionplayer.pdga_number_1, divisionplayer.pdga_number_2 = ParsePDGAnumber(data["event_type"][0], player)
            divisionplayer.pdga_page_1, divisionplayer.pdga_page_2 = ParseTournamentPDGApage(data["event_type"][0], player)
            divisionplayer.propagator_1, divisionplayer.propagator_2 = ParsePropagator(data["event_type"][0], player)
            divisionplayer.rating_during_tournament_1, divisionplayer.rating_during_tournament_2 = ParseRatingTournament(data["event_type"][0], player)
            #Use new fields here
            divisionplayer.full_name = []
            if divisionplayer.full_name_1:
                divisionplayer.full_name.append(divisionplayer.full_name_1)
            if divisionplayer.full_name_2:
                divisionplayer.full_name.append(divisionplayer.full_name_2)

            divisionplayer.pdga_number = []
            #if divisionplayer.pdga_number_1

            divisionplayer.pdga_page = []
            divisionplayer.rating_during_tournament = []
            divisionplayer.propagator = True


            divisionplayer.rounds_with_results = 0
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

                if r.round_throws > 0:
                    divisionplayer.rounds_with_results += 1
                #r.avg_throw_length_meters = PlayerRoundAvgThrowLenghtMeters(division.rounds, r.round_throws, r.round_number)
                #r.avg_throw_length_feet = PlayerRoundAvgThrowLenghtFeet(division.rounds, r.round_throws, r.round_number)
                divisionplayer.rounds.append(r)

            if divisionplayer.pdga_number_1 is not None:
                all_pdga_numbers.append(divisionplayer.pdga_number_1)
                logging.info('Division name: %s. Pdga number: %s.' % (division.name, str(divisionplayer.pdga_number_1)))

            if divisionplayer.pdga_number_2 is not None:
                all_pdga_numbers.append(divisionplayer.pdga_number_2)
                logging.info('Division name: %s. Pdga number: %s.' % (division.name, str(divisionplayer.pdga_number_2)))

            divisionplayer.avg_throws_per_round = CalculateAvgFromRounds(divisionplayer.total_throws, divisionplayer.rounds)
            divisionplayer.avg_par_per_round = CalculateAvgFromRounds(divisionplayer.total_par, divisionplayer.rounds)
            divisionplayer.avg_round_rating = CalculateAvgRoundRating(divisionplayer.rounds)
            #divisionplayer.avg_throw_length_meters
            #divisionplayer.avg_throw_length_feet
            #divisionplayer.avg_throws_per_hole
            parsed_players.append(divisionplayer)

        #Calculate extra round statistics here, these can only be calculated after all players have been parsed once.
        #r.round_placement
        #r.tournament_placement

        #divisionround.round_total_throws = ""
        #divisionround.avg_throws = ""
        #divisionround.avg_par = ""
        #divisionround.avg_throw_length_meters = ""
        #divisionround.avg_throw_length_meters = ""
        #divisionround.dns_count = ""
        #divisionround.dnf_count = ""
        #divisionround.round_total_players = ""

        division.players = parsed_players

        #for r in division.rounds:


        #Calculate fields that can not be calculated at the same time while parsing basic data

        all_divisions.append(division)

    return all_divisions, all_pdga_numbers



    #Divisions (Open, FPO, MP40)
        #division name
        #division short name
        #division type (singles, doubles, team)
        #division total players
        ##division total throws
        ##division avg player rating
        ##division avg throws
        ##division avg par
        ##division avg round rating
        ##division avg throw length_meters
        ##division avg throw length_feet
        ##division total course holes (course)
        ##division total course par (course)
        ##division total course length meters
        ##division total course length feet
        ##dns count
        ##dnf count
        #rounds
            #round number
            #round_total_players
            #course name
            #course layout
            #course holes
            #course par
            #course_avg_hole_par
            #course length meters
            #course length feet
            #course pdga page
            #total throws
            #avg par
            #avg throws
            #avg round rating
            #dns count
            #dnf count
        #players
            #full_name
            #pdga_number
            #pdga_page
            #propagator
            #rating_during_tournament
            #final_placement
            #money_won
            #total_throws
            #total_par
            #avg_throws_per_round
            #avg_par_per_round
            #avg_round_rating
            #avg throw length meters
            #avg throw length feet
            #avg throws per hole
            #event_points
            #dns
            #dnf
            #rounds
                #round_number
                #round_throws
                #round_rating
                #round_placement
                #tournament_placement
                #avg throw length
                #avg throws per hole
                #dns
                #dnf
