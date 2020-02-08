# coding=utf-8
import json
import logging
from datetime import date
from models.schemas import Player
from mongoengine import *
from helpers.helpers_data_parsing import *
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


def ParsePlayer(data):
    player, player.player_exists = PlayerExists(data['player_pdga_number'])
    player.pdga_id_status = ParseIdStatus(data['player_name'], data['player_id'])
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
    player.lowest_rating, player.current_rating, player.highest_rating, player.rating_difference, player.latest_rating_update = ParseRatings(data['player_current_rating'], player.current_rating, player.lowest_rating, player.highest_rating, data['player_rating_difference'], ParseDate(data['player_rating_updated']), data['player_membership_status'])
    player.individual_tournament_years = ParseIndividualTournamentYears(data['player_individual_tournament_years'], data['player_membership_status'], player.individual_tournament_years)
    player.certified_status, player.certified_status_expiration_date = ParseCertifiedStatus(data['player_certified_status'], data['player_certified_status_expiration'])
    added_data, removed_data, modified_data, same_data, all_new = CompareDicts(data['player_pdga_number'], player)
    #player.fields_updated.append(CreateFieldsUpdated(added_data, removed_data, modified_data, str(date.today()), all_new))
    player.fields_updated = []
    logging.info("Player with PDGA number %s has been added to Mongo", str(player.pdga_number))

    player.save()

#ParsePlayer(data)
