# coding=utf-8
import json
import logging
from datetime import date
from project.models.schemas import Player
from project.helpers.helpers_data_parsing import *
from project.player_processes.player_statistics import GeneratePlayerStatistics
from project.utils.s3_tools import download_file_from_s3_return_file_path
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


def handle_arguments() -> (str):
    parser = argparse.ArgumentParser()
    parser.add_argument('--s3_key',
        type=str,
        help="S3 folder name that is date in format YearMonthDay",
        required=False
    )
    parser.add_argument('--send',
        action="store_true",
        help="Send data, defaults to False",
    )
    parser.add_argument('--statistics',
        action="store_true",
        help="Argument if statistics should be created. By default statistics are not created.",
    )
    parser.add_argument('--clear_updated_fields',
        action="store_true",
        help="Argument if updated_fields should be cleaned. By default fields are not cleared.",
    )
    parser.add_argument('--index',
        type=int,
        help="Index key if you want to start parsing from different key. Files in order the keys are downloaded from S3.",
    )
    args = parser.parse_args()

    return args.s3_key, args.send, args.statistics, args.clear_updated_fields, args.index


def ParsePlayer(data, send_data=True, generate_statistics=False, clear_fields_updated=False):

    data_pdga_number = data.get('player_pdga_number')

    if not data_pdga_number:
        return

    new_player = Player()
    new_player.pdga_number = str(data.get('player_pdga_number'))
    new_player.pdga_id_status = ParseIdStatus(data)
    new_player.membership_status = CheckMembership(data) 
    new_player.membership = CheckAndNormalizeMembershipStatus(data)
    new_player.membership_status_expiration_date = ParseDate(data.get('player_membership_expiration_date'))
    new_player.full_name = CleanPlayerFullName(data)
    new_player.first_name, new_player.middle_name, new_player.last_name = ParsePlayerFullName(data)
    new_player.location_full = CleanFullLocation(data, type="player")
    new_player.city, new_player.state, new_player.country = ParseFullLocation(data, type="player")
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


    if generate_statistics:
        GeneratePlayerStatistics(new_player)

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

        if clear_fields_updated:
            new_player.fields_updated = []
        else:
            new_player.fields_updated = CheckFieldsUpdated(new_player, old_player)

    if send_data:
        new_player.save()
    else:
        print_data = json.loads(new_player.to_json())
        print(json.dumps(print_data, indent=4))
    logger.info("Player with PDGA number %s has been added to Mongo", str(new_player.pdga_number))


def loop_through_data(s3_key, send, statistics, clear_updated_fields, start_index):
    file_counter = s3_key.split('.json')[0].split('data_')[1]
    download_name = f"data_{file_counter}"
    file_path = download_file_from_s3_return_file_path(s3_key, download_name)

    with open(file_path, "r") as data:
        all_data = json.load(data)
        for d in all_data:
            if d:
                ParsePlayer(d, send, statistics, clear_updated_fields)


if __name__ == "__main__":
    s3_key, send, statistics, clear_updated_fields, start_index = handle_arguments()
    loop_through_data(s3_key, send, statistics, clear_updated_fields, start_index)