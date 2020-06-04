# coding=utf-8
import json
import logging
import argparse
from datetime import date
from project.models.schemas import Tournament
from project.utils.connect_mongodb import ConnectMongo
from project.helpers.helpers_data_parsing import *
from project.tournament_processes.division import ParseDivisions
from project.utils.s3_tools import download_file_from_s3_return_file_path
from project.utils.slack_message_sender import SendSlackMessageToChannel
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


def ParseTournament(data, send_data=True, generate_statistics=False, clear_fields_updated=False):
    ConnectMongo()

    #print(json.dumps(data, indent=4))

    tournament = Tournament()
    tournament.tournament_id = parse_tournament_id(data)
    tournament.pdga_page_link = data.get("event_link")
    tournament.tournament_name = data.get("event_title") if data.get("event_title") != "Page not found" else None

    logger.info("Started parsing tournament %s with id %s.", tournament.tournament_name, tournament.tournament_id)

    tournament.location_full = CleanFullLocation(data, type="tournament")
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
    tournament.first_crawl_date = data.get("event_crawl_date")
    tournament.latest_update = str(date.today())
    tournament.divisions, tournament.players = ParseDivisions(data)

    if generate_statistics:
        CalculateTournamentStatistics(tournament)

    old_tournament = TournamentExists(tournament.tournament_id)

    if old_tournament:
        tournament.id = old_tournament.id
        tournament.first_crawl_date = old_tournament.first_crawl_date
        tournament.tournament_director = check_tournament_director(tournament, old_tournament)
        tournament.tournament_director_id = check_tournament_director_id(tournament, old_tournament)
        tournament.assistant_director = check_assistant_tournament_director(tournament, old_tournament)
        tournament.assistant_director_id = check_assistant_tournament_director_id(tournament, old_tournament)
        #if clear_fields_updated:
        tournament.fields_updated = []
        #else:
        #    tournament.fields_updated.append(CheckFieldsUpdatedTournament(tournament, old_tournament))

    #if not tournament.players:
    #    SendSlackMessageToChannel("Could not parse players for tournament %s with id %s" % (str(tournament.tournament_name), str(tournament.tournament_id)), "#data-reports")
    
    if send_data and tournament.tournament_name:
        logger.info("Tournament %s with id %s has been sent to mongo", tournament.tournament_name, tournament.tournament_id)
        tournament.save()
    else:
        print_data = json.loads(tournament.to_json())
        print(json.dumps(print_data, indent=4))


def loop_through_data(s3_key, send, statistics, clear_updated_fields, start_index):
    file_counter = s3_key.split('.json')[0].split('data_')[1]
    download_name = f"data_{file_counter}"
    file_path = download_file_from_s3_return_file_path(s3_key, download_name)

    with open(file_path, "r") as data:
        all_tournaments = json.load(data)
        for tournament in all_tournaments:
            if tournament:
                ParseTournament(tournament, send, statistics, clear_updated_fields)


if __name__ == "__main__":
    s3_key, send, statistics, clear_updated_fields, start_index = handle_arguments()
    loop_through_data(s3_key, send, statistics, clear_updated_fields, start_index)
