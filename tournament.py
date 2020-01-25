# coding=utf-8
import json
import logging
from datetime import date
from schemas import Tournament
from mongoengine import *
from connect_mongodb import ConnectMongo
from helpers_data_parsing import *
from division import ParseDivisions
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


def ParseTournament(data):
    ConnectMongo()
    #print (json.dumps(data, indent=4))
    #Fields from crawler
    tournament, exists, tournament.tournament_id, tournament.pdga_page_link = TournamentExists(data['event_link'])
    #if not exists:
    tournament.tournament_name = ParseTournamentName(data['event_title'])
    tournament.location_full = data["event_location"]
    tournament.location_city, tournament.location_state, tournament.location_country = ParseFullLocation(data["event_location"])
    tournament.tournament_start, tournament.tournament_end, tournament.tournament_length_days = ParseTournamentDates(data["event_date"])
    tournament.tournament_director, tournament.tournament_director_id = ParseTournamentDirector(data['event_tournament_director_name'], data['event_tournament_director_id'])
    tournament.assistant_director, tournament.assistant_director_id = ParseTournamentDirector(data['event_assistant_dt_name'], data['event_assistant_dt_id'])
    tournament.tournament_tier = data['event_tier']
    tournament.tournament_website = ParseTournamentWebsite(data["event_website"])
    tournament.tournament_phone = data["event_phone"]
    tournament.tournament_email = data["event_email"]
    tournament.total_players = int(data["event_total_players"])
    tournament.tournament_classification = data["event_classification"]
    tournament.event_results_status = data["event_status"]
    tournament.pdga_latest_update = ParseDate(data["event_status_last_updated"])
    tournament.pro_prize_money = ParseTournamentProPurse(data["event_pro_purse"])
    tournament.tournament_type = data["event_type"]
    tournament.first_crawl_date = data["event_crawl_date"]
    tournament.latest_update = str(date.today())
    hole_by_hole_scoring = data['event_livescoring']
    tournament.divisions, tournament.players = ParseDivisions(data)
    #print (tournament.to_json())
    logging.info('----------------------------')
    logging.info('Tournament: %s. PDGA page: %s' % (tournament.tournament_name, tournament.pdga_page_link))
    logging.info('Tournament ID: %s' % str(tournament.tournament_id))

    #bbb = json.loads(tournament.to_json())
    #print (json.dumps(bbb, indent=4, sort_keys=True))
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
