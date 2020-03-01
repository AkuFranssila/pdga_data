# coding=utf-8
import json
import logging
from datetime import date
from project.models.schemas import Player
from mongoengine import *
from project.helpers.helpers_data_parsing import *
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


def ParsePlayer(data):

    #first create the new player
    #check if player exists.
    #if player exists compare the fields and generate the new player
    # save the new player and send to mongo

    new_player = Player()
    new_player.pdga_number = str(data.get('player_pdga_number'))
    new_player.pdga_id_status = ParseIdStatus(data)
    new_player.membership_status = CheckMembership(data) 
    new_player.membership = CheckAndNormalizeMembershipStatus(data)
    new_player.membership_status_expiration_date = ParseDate(data.get('player_membership_expiration_date'))
    new_player.full_name = CleanPlayerFullName(data)
    new_player.first_name, new_player.middle_name, new_player.last_name = ParsePlayerFullName(data)
    new_player.location_full = CleanFullLocation(data)
    new_player.city, new_player.state, new_player.country = ParseFullLocation(data)
    new_player.classification = ParseClassification(data)
    new_player.member_since = ParseMemberSince(data)
    new_player.career_earnings = data.get('player_career_earnings')
    new_player.total_events = data.get('player_events_played')
    new_player.total_wins = data.get('player_career_wins')
    new_player.pdga_page_link = GeneratePDGAplayerlink(data)
    new_player.latest_update = str(date.today())
    new_player.first_crawl_date = data.get('player_crawl_date')
    new_player.lowest_rating = data.get('player_current_rating')
    new_player.highest_rating = data.get('player_current_rating')
    new_player.current_rating = data.get('player_current_rating')
    new_player.rating_difference = data.get('player_rating_difference')
    new_player.latest_rating_update = ParseDate(data.get('player_rating_updated'))
    new_player.individual_tournament_years = data.get('player_individual_tournament_years')
    new_player.certified_status = ParseCertifiedStatus(data)
    new_player.certified_status_expiration_date = ParseDate(data.get('player_certified_status_expiration'))

    old_player = CheckifPlayerExists(new_player.pdga_number)

    if old_player:
        """
            If player already exists we want to update only specific fields. 
            Other fields can be updated always when crawling new player.
        """
        new_player.id = old_player.id
        new_player.lowest_rating = CheckLowestRating(new_player, old_player)
        new_player.highest_rating = CheckHighestRating(new_player, old_player)
        new_player.current_rating = CheckCurrentRating(new_player, old_player)
        new_player.rating_difference = CheckRatingDifference(new_player, old_player)
        new_player.latest_rating_update = CheckLatestRatingUpdate(new_player, old_player)

        new_player.first_crawl_date = old_player.first_crawl_date

        new_player.certified_status = CheckCertifiedStatus(new_player, old_player)
        new_player.certified_status_expiration_date = CheckCertifiedStatusExpirationDate(new_player, old_player)

        new_player.fields_updated = CheckFieldsUpdated(new_player, old_player)

        new_player.save()
    else:
        new_player.to_mongo().to_dict()
        new_player.save()
    logging.info("Player with PDGA number %s has been added to Mongo", str(new_player.pdga_number))

