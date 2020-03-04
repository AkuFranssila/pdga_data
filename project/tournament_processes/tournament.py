# coding=utf-8
import json
import logging
from datetime import date
from project.models.schemas import Tournament
from mongoengine import *
from project.utils.connect_mongodb import ConnectMongo
from project.helpers.helpers_data_parsing import *
from project.tournament_processes.division import ParseDivisions
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


def ParseTournament(data):
    ConnectMongo()

    tournament = Tournament()
    tournament.tournament_id = parse_tournament_id(data)
    tournament.pdga_page_link = data.get("event_link")
    tournament.tournament_name = data.get("event_title")
    tournament.location_full = CleanFullLocation(data)
    tournament.location_city, tournament.location_state, tournament.location_country = ParseFullLocation(data, type="tournament")
    tournament.tournament_start, tournament.tournament_end, tournament.tournament_length_days = ParseTournamentDates(data)
    tournament.tournament_director = ParseTournamentDirectorName(data, "td")
    tournament.tournament_director_id = ParseTournamentDirectorID(data, "td")
    tournament.assistant_director = ParseTournamentDirectorName(data, "td_assistant")
    tournament.assistant_director_id = ParseTournamentDirectorID(data, "td_assistant")
    tournament.tournament_tier = data.get("event_tier")
    tournament.tournament_website = ParseTournamentWebsite(data)
    tournament.tournament_phone = data.get("event_phone")
    tournament.tournament_email = data.get("event_email")
    tournament.total_players = parse_tournament_total_players(data)
    tournament.tournament_classification = data.get("event_classification")
    tournament.event_results_status = data.get("event_status")
    tournament.pdga_latest_update = ParseDate(data.get("event_status_last_updated"))
    tournament.pro_prize_money = ParseTournamentProPurse(data)
    tournament.tournament_type = data.get("event_type")
    tournament.hole_by_hole_scoring = data.get("event_livescoring")
    tournament.first_crawl_date = data("event_crawl_date")
    tournament.latest_update = str(date.today())
    tournament.divisions = ParseDivisions(data)
    tournament.players = ""

    old_tournament = TournamentExists(tournament.tournament_id)

    if old_tournament:
        tournament.id = old_tournament.id
        tournament.first_crawl_date = old_tournament.first_crawl_date
        tournament.tournament_director = check_tournament_director(tournament, old_tournament)
        tournament.tournament_director_id = check_tournament_director_id(tournament, old_tournament)
        tournament.assistant_director = check_assistant_tournament_director(tournament, old_tournament)
        tournament.assistant_director_id = check_assistant_tournament_director_id(tournament, old_tournament)
        tournament.fields_updated = CheckFieldsUpdatedTournament(tournament, old_tournament)
    
    tournament.save()

    #Divisions (Open, FPO, MP40)
        #division name
        #division short name
        #division type (singles, doubles, team)
        #division total players
        #division total throws
        #division avg player rating
        #division avg throws
        #division avg par
        #division avg round rating
        #division avg throw length_meters
        #division avg throw length_feet
        #division total course holes (course)
        #division total course par (course)
        #division total course length meters
        #division total course length feet
        #dns count
        #dnf count
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


    #Fields calculated from data received from crawler
    #avg_total_player_par
    #avg_player_rating
    #avg_total_round_rating
    #avg_money_all_players
    #avg_money_mpo_players
    #print (tournament.to_json())
