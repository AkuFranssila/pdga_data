# coding=utf-8
import json
import logging
from schemas import Player
from mongoengine import *
from connect_mongodb import ConnectMongo
from helpers_data_parsing import ParseFullName, ParseFullLocation, ParseDate


data = {
"player_name": "Steady Ed Headrick",
"player_pdga_number": 1,
"player_id": True,
"player_location_raw": "Watsonville, California, United States",
"player_classification": "Professional",
"player_member_since": 1976,
"player_membership_status": "Eagle Club",
"player_membership_expiration_date": "31-Dec-2200",
"player_current_rating": 736,
"player_rating_difference": None,
"player_rating_updated": "15-Sep-2004",
"player_events_played": 41,
"player_career_wins": 8,
"player_certified_status": None,
"player_certified_status_expiration": None,
"player_career_earnings": 602.0,
"player_individual_tournament_years": ["2001", "2000", "1999", "1998", "1997", "1996", "1995", "1994", "1993", "1992", "1991", "1990", "1989", "1988", "1987", "1986", "1985", "1984", "1983", "1981"]
}

ConnectMongo()
try:
    player_from_db = Player.objects.get(pdga_number=pdga_number)
    player_exists = True
except: #schemas.DoesNotExist
    player_exists = False

membership = data['player_membership_status'].lower()
if membership == "ace club":
    membership_status = True
elif membership == "eagle club":
    membership_status = True
elif membership == "birdie club":
    membership_status = True
elif membership == "active":
    membership_status = True
elif membership == "expired":
    membership_status = False
else:
    membership_status = False
player = Player()
full_name = data['player_name']
first_name, last_name = ParseFullName(data['player_name'])
pdga_number = data['player_pdga_number']
pdga_number_status = data['player_id']
location_full = data['player_location_raw']
city, state, country = ParseFullLocation(data['player_location_raw'])
classification = data['player_classification']
member_since = data['player_member_since']
membership_status_expiration_date = ParseDate( data['player_membership_expiration_date'])

if membership_status:
    current_rating = data['player_current_rating']
if player_exists and current_rating > player_from_db.highest_rating and membership_status:
    highest_rating = data['player_current_rating']
elif player_exists and player_from_db.lowest > current_rating and membership_status:
    lowest_rating = data['player_current_rating']
elif player_exists == False:
    highest_rating = data['player_current_rating']
    lowest_rating = data['player_current_rating']

if data['player_rating_difference'] is not None and membership_status:
    rating_difference = data['player_rating_difference']

if membership_status:
    latest_rating_update = ParseDate(data['player_rating_updated'])
total_events = data['player_events_played']
total_wins = data['player_career_wins']
if membership_status:
    
# certified_status = data['']
# certified_status_expiration_date = data['']
# career_earnings = data['']
# individual_tournament_years = data['']
# pdga_page_link = data['']
# played_event_ids = data['']
# played_countries = data['']
# first_crawl_date = data['']
# latest_update = data['']
# fields_updated = data['']
