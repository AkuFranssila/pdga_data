# coding=utf-8
import json
import logging
from datetime import date
from schemas import *
from mongoengine import *
from connect_mongodb import ConnectMongo
from helpers_data_parsing import *
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


def ParseDivisions(data):
    #ConnectMongo()
    division = Division()
    for div in data['event_divisions']:
        print (div)
        division.name = ParseDivisionFullName(div['division_name'])
        division.short_name = div['division_short_name']
        division.type = data["event_type"][0]
        division.total_players = ParseDivisionTotalPlayers(div["division_total_players"])
        #division.rounds =
        #divisionround = DivisionRound()
        try:
            all_players = div['division_players_singles']
        except:
            try:
                all_players = div['division_players_doubles']
            except:
                all_players = div['division_players_team']

        parsed_players = []
        for player in all_players:
            divisionplayer = DivisionPlayer()
            divisionplayer.full_name_1, divisionplayer.full_name_2 = ParseTournamentName(data["event_type"][0], player)
            divisionplayer.pdga_number_1, divisionplayer.pdga_number_2 = ParsePDGAnumber(data["event_type"][0], player)
            divisionplayer.pdga_page_1, divisionplayer.pdga_page_2 = player["player_pdga_link"]
            divisionplayer.propagator_1, divisionplayer.propagator_2 = player["player_propagator"]
            divisionplayer.rating_during_tournament_1, divisionplayer.rating_during_tournament_2 = player["player_rating_during_tournament"]
            divisionplayer.final_placement = "" #funk
            divisionplayer.money_won = "" #funk
            divisionplayer.total_throws = "" #funk
            divisionplayer.total_par = "" #funk
            divisionplayer.event_points = float(player["player_event_points"])
            print(player["player_final_placement"])
            #divisionplayers.dns = ""
            #divisionplayers.dnf = ""
            #divisionplayers.avg_throws_per_round
            #divisionplayers.avg_par_per_round
            #divisionplayers.avg_round_rating
            #divisionplayers.avg_throw_length_meters
            #divisionplayers.avg_throw_length_feet
            #divisionplayers.avg_throws_per_hole
            parsed_players.append(divisionplayer)

        for count, round in enumerate(div['division_course_details']):
            divisionround = DivisionRound()
            divisionround.round_number = count + 1
            divisionround.round_total_players = ""
            divisionround.course_name, divisionround.course_layout, divisionround.course_holes, divisionround.course_par, divisionround.course_pdga_page, divisionround.course_length_meters, divisionround.course_length_feet = ParseCourseDetails(round['round_' + str(count + 1)]['course_details'], round['round_' + str(count + 1)]['course_pdga_link'])
            divisionround.round_total_throws = ""
            divisionround.avg_throws = ""
            divisionround.avg_par = ""
            divisionround.avg_throw_length_meters = ""
            divisionround.avg_throw_length_meters = ""
            divisionround.dns_count = ""
            divisionround.dnf_count = ""

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
