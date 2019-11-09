# coding=utf-8
import json
import logging
from datetime import date
from schemas import Tournament
from mongoengine import *
from connect_mongodb import ConnectMongo
from helpers_data_parsing import *
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


def ParseTournament(data):
    #ConnectMongo()
    #print (json.dumps(data, indent=4))
    #print (data['event_title'])
    #print (data['event_date'])
    #print (data['event_divisions'][0]['division_course_details'])
    tournament, exists, tournament.tournament_id, tournament.pdga_page_link = TournamentExists(data['event_link'])
    tournament.tournament_name = ParseTournamentName(data['event_title'])
    tournament.location_full = data["event_location"]
    tournament.location_city, tournament.location_state, tournament.location_country = ParseFullLocation(data["event_location"])
    tournament.tournament_start, tournament.tournament_end, tournament.tournament_length = ParseTournamentDates(data["event_date"])
    print (data['event_date'])
    print (tournament.tournament_start)
    print (tournament.tournament_end)
    print (tournament.tournament_length)
    #print (tournament.to_json())
