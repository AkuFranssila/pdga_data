# coding=utf-8
import json
import logging
from datetime import date
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
"player_current_rating": 888,
"player_rating_difference": None,
"player_rating_updated": "15-Sep-2004",
"player_events_played": 41,
"player_career_wins": 8,
"player_certified_status": None,
"player_certified_status_expiration": None,
"player_career_earnings": 602.0,
"player_crawl_date": "2019-10-20",
"player_individual_tournament_years": ["2001", "2000", "1999", "1998", "1997", "1996", "1995", "1994", "1993", "1992", "1991", "1990", "1989", "1988", "1987", "1986", "1985", "1984", "1983", "1981"]
}

def ParsePlayer(single_dict):
    ConnectMongo()
    player = Player()
    try:
        player_from_db = Player.objects.get(pdga_number=data['player_pdga_number'])
        player_exists = True
    except: #schemas.DoesNotExist
        player_exists = False

    print (player_exists)

    #Fields that are always shown or need to be always updated
    player.membership = data['player_membership_status'].lower()
    if player.membership == "ace club":
        player.membership_status = True
    elif player.membership == "eagle club":
        player.membership_status = True
    elif player.membership == "birdie club":
        player.membership_status = True
    elif player.membership == "active":
        player.membership_status = True
    elif player.membership == "expired":
        player.membership_status = False
    else:
        player.membership_status = False
    player.full_name = data['player_name']
    player.first_name, last_name = ParseFullName(data['player_name'])
    player.pdga_number = data['player_pdga_number']
    player.pdga_id_status = data['player_id']
    player.location_full = data['player_location_raw']
    player.city, player.state, player.country = ParseFullLocation(data['player_location_raw'])
    player.classification = data['player_classification']
    player.member_since = data['player_member_since']
    player.membership_status_expiration_date = ParseDate( data['player_membership_expiration_date'])
    player.career_earnings = data['player_career_earnings']
    player.total_events = data['player_events_played']
    player.total_wins = data['player_career_wins']
    player.pdga_page_link = "https://www.pdga.com/player/" + str(player.pdga_number)
    player.latest_update = str(date.today())
    #^ Always available fields end

    #Fields that require that the player already exists
    #Fields that require that the player is active
    #Fields that require that the player exists and is active
    #Fields that only need to be updated if player does not exists
    #Fields that only need to be updated if player active and doesn not exists
    if player_exists == False:
        player.first_crawl_date = data['player_crawl_date']
    if player_exists == False and player.membership_status:
        player.highest_rating = data['player_current_rating']
        player.lowest_rating = data['player_current_rating']
        player.current_rating = data['player_current_rating']
    if player_exists and player.membership_status:
        player.current_rating = data['player_current_rating']
        if player.current_rating > player_from_db.highest_rating:
            player.highest_rating = data['player_current_rating']
        if player_from_db.lowest_rating > player.current_rating:
            player.lowest_rating = data['player_current_rating']
    if player.membership_status:
        player.current_rating = data['player_current_rating']
        player.latest_rating_update = ParseDate(data['player_rating_updated'])
        player.certified_status = data['player_certified_status']
        player.certified_status_expiration_date = ParseDate(data['player_certified_status_expiration'])
        player.individual_tournament_years = data['player_individual_tournament_years']
        if data['player_rating_difference'] is not None:
            player.rating_difference = data['player_rating_difference']
    #if player_exists:
        #Need to create parsing logic when tournaments have been crawled.
        #player.played_event_ids = data[''] only if player exists
        #player.played_countries = data[''] only if player exists

    #Crawl players first, then create logic to compare new vs previous
    #player.fields_updated = data[''] only if player exists
    # def dict_compare(d1, d2):
    #     d1_keys = set(d1.keys())
    #     d2_keys = set(d2.keys())
    #     intersect_keys = d1_keys.intersection(d2_keys)
    #     added = d1_keys - d2_keys
    #     removed = d2_keys - d1_keys
    #     modified = {o : (d1[o], d2[o]) for o in intersect_keys if d1[o] != d2[o]}
    #     same = set(o for o in intersect_keys if d1[o] == d2[o])
    #     return added, removed, modified, same
    #
    # x = dict(a=1, b=2)
    # y = dict(a=2, b=2)
    # added, removed, modified, same = dict_compare(x, y)


    player.save()

ParsePlayer(data)
