# coding=utf-8
import json
import logging
from datetime import date
from schemas import Player
from mongoengine import *
from connect_mongodb import ConnectMongo
from helpers_data_parsing import *
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


def ParsePlayer(data):
    ConnectMongo()
    player, player.player_exists = PlayerExists(data['player_pdga_number'])
    player.pdga_id_status = data['player_id']
    player.membership, player.membership_status = CheckMembershipStatus(data['player_membership_status'])
    player.membership_status_expiration_date = ParseDate( data['player_membership_expiration_date'])
    player.full_name = data['player_name']
    player.first_name, player.last_name = ParseFullName(data['player_name'])
    player.location_full = data['player_location_raw']
    player.city, player.state, player.country = ParseFullLocation(data['player_location_raw'])
    player.classification = ParseClassification(data['player_classification'])
    player.member_since = ParseMemberSince(data['player_member_since'])
    player.career_earnings = CheckIfValueNone(data['player_career_earnings'])
    player.total_events = CheckIfValueNone(data['player_events_played'])
    player.total_wins= CheckIfValueNone(data['player_career_wins'])
    player.pdga_page_link = "https://www.pdga.com/player/" + str(data['player_pdga_number'])
    player.latest_update = str(date.today())
    player.first_crawl_date = CheckIfNewPlayer(data['player_crawl_date'], player.first_crawl_date)
    player.pdga_number = CheckIfNewPlayer(data['player_pdga_number'], player.pdga_number)

    if player.pdga_id_status and data['player_membership_status'] is not None:
        #^ Always available fields end
        #Special cases (well because of course those exists)
        #Fields that require that the player already exists
        #Fields that require that the player is active
        #Fields that require that the player exists and is active
        #Fields that only need to be updated if player does not exists
        #Fields that only need to be updated if player active and doesn not exists
        if not player_exists and player.membership_status:
            player.highest_rating = data['player_current_rating']
            player.lowest_rating = data['player_current_rating']
            player.current_rating = data['player_current_rating']
        if player_exists and player.membership_status:
            if type(player.current_rating).__name__ == 'int' and type(player.highest_rating).__name__ == 'int' and type(player.lowest_rating).__name__ == 'int':
                player.current_rating = data['player_current_rating']
                if player.current_rating > player.highest_rating:
                    player.highest_rating = data['player_current_rating']
                if player.lowest_rating > player.current_rating:
                    player.lowest_rating = data['player_current_rating']
        if player.membership_status:
            player.current_rating = data['player_current_rating']
            player.latest_rating_update = ParseDate(data['player_rating_updated'])
            player.individual_tournament_years = data['player_individual_tournament_years']
            if data['player_rating_difference'] is not None:
                player.rating_difference = data['player_rating_difference']

            if data['player_certified_status'] == "Certified":
                player.certified_status = True
                player.certified_status_expiration_date = ParseDate(data['player_certified_status_expiration'])
            else:
                player.certified_status = False
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

#ParsePlayer(data)
