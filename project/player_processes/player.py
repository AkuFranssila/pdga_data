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
    new_player.pdga_id_status = ParseIdStatus(data)
    new_player.membership_status = CheckAndNormalizeMembershipStatus(data)
    new_player.membership = CheckMembership(data)
    new_player.membership_status_expiration_date = ParseDate(data.get('player_membership_expiration_date'))
    new_player.full_name = CleanPlayerFullName(data)
    new_player.first_name, new_player.middle_name, new_player.last_name = ParsePlayerFullName(data)
    new_player.location_full = CleanFullLocation(data)
    new_player.city, new_player.state, new_player.country = ParseFullLocation(data)
    new_player.classification = ParseClassification(data)

    #player, player.player_exists = PlayerExists(data.get('player_pdga_number'))
    #player.pdga_id_status = ParseIdStatus(data.get('player_name'), data.get('player_id'))
    #player.membership, player.membership_status = CheckMembershipStatus(data.get('player_membership_status'))
    #player.membership_status_expiration_date = ParseDate(data.get('player_membership_expiration_date'))
    #player.full_name = data.get('player_name')
    #player.first_name, player.last_name = ParseFullName(data.get('player_name'))
    #player.location_full = data.get('player_location_raw')
    #player.city, player.state, player.country = ParseFullLocation(data.get('player_location_raw'))


    # player.classification = ParseClassification(data.get('player_classification'))
    # player.member_since = ParseMemberSince(data.get('player_member_since'))
    # player.career_earnings = CheckIfValueNone(data.get('player_career_earnings'))
    # player.total_events = CheckIfValueNone(data.get('player_events_played'))
    # player.total_wins= CheckIfValueNone(data.get('player_career_wins'))
    # player.pdga_page_link = "https://www.pdga.com/player/" + str(data.get('player_pdga_number'))
    # player.latest_update = str(date.today())
    # player.first_crawl_date = CheckIfNewPlayer(data.get('player_crawl_date'), player.first_crawl_date)
    # player.pdga_number = CheckIfNewPlayer(data.get('player_pdga_number'), player.pdga_number)
    # player.lowest_rating, player.current_rating, player.highest_rating, player.rating_difference, player.latest_rating_update = ParseRatings(data.get('player_current_rating'), player.current_rating, player.lowest_rating, player.highest_rating, data.get('player_rating_difference'), ParseDate(data.get('player_rating_updated')), data.get('player_membership_status'))
    # player.individual_tournament_years = ParseIndividualTournamentYears(data.get('player_individual_tournament_years'), data.get('player_membership_status'), player.individual_tournament_years)
    # player.certified_status, player.certified_status_expiration_date = ParseCertifiedStatus(data.get('player_certified_status'), data.get('player_certified_status_expiration'))
    # added_data, removed_data, modified_data, same_data, all_new = CompareDicts(data.get('player_pdga_number'), player)
    #player.fields_updated.append(CreateFieldsUpdated(added_data, removed_data, modified_data, str(date.today()), all_new))
    #player.fields_updated = []
    #logging.info("Player with PDGA number %s has been added to Mongo", str(player.pdga_number))

    new_player.save()

#ParsePlayer(data)
