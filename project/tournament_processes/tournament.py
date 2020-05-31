# coding=utf-8
import json
import logging
from datetime import date
from project.models.schemas import Tournament
from mongoengine import *
from project.utils.connect_mongodb import ConnectMongo
from project.helpers.helpers_data_parsing import *
from project.tournament_processes.division import ParseDivisions
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


def ParseTournament(data, send_data=True, generate_statistics=False, clear_fields_updated=False):
    ConnectMongo()

    print(json.dumps(data, indent=4))

    tournament = Tournament()
    tournament.tournament_id = parse_tournament_id(data)
    tournament.pdga_page_link = data.get("event_link")
    tournament.tournament_name = data.get("event_title")
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
        if clear_fields_updated:
            tournament.fields_updated = []
        else:
            tournament.fields_updated = CheckFieldsUpdatedTournament(tournament, old_tournament)
    
    if send_data:
        tournament.save()
    else:
        print_data = json.loads(tournament.to_json())
        print(json.dumps(print_data, indent=4))
