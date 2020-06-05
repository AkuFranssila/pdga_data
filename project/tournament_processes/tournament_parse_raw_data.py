# coding=utf-8
from bs4 import BeautifulSoup
import requests
import json
import logging
import re
from datetime import date
from project.helpers.helpers_crawler import TournamentDate, TournamentLastPage
from project.helpers.helpers_raw_tournament_parsing import *
from project.utils.slack_message_sender import SendSlackMessageToChannel
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

def TournamentParseRawData(id, raw_data):
    logging.info("Starting TournamentParseRawData for pdga ")
    soup = BeautifulSoup(raw_data, "html.parser")
    event = {}

    special_event = False 
    if "/global-event/results/" in raw_data:
        special_event = True
        logging.info("Event is special event. Logging whole raw data.")
        logging.info(raw_data)

    if not special_event:
        logging.info("Event was not special event. Starting raw data parsing")
        event['event_crawl_date'] = str(date.today())
        event['event_link'] = soup.find("link", attrs={"rel":"shortlink"})["href"]

        event_title = soup.find(id="page-title")
        event['event_title'] = event_title.text if event_title else None

        event_date = soup.find(class_="tournament-date")
        event['event_date'] = event_date.text if event_date else None
        print(event['event_link'], event['event_title'], event['event_date'])

        event_location = soup.find(class_="tournament-location")
        event['event_location'] = event_location.text if event_location else None

        event_tournament_director_name = soup.find(class_="tournament-director")
        event['event_tournament_director_name'] = event_tournament_director_name.text if event_tournament_director_name else None

        event_tournament_director_id = soup.find(class_="tournament-director")
        event_tournament_director_id = event_tournament_director_id.find('a') if event_tournament_director_id else None 
        event['event_tournament_director_id'] = event_tournament_director_id['href'] if event_tournament_director_id else None

        event_assistant_dt_name = soup.find_all(class_="tournament-director")
        event_assistant_dt_name = event_assistant_dt_name[1].text if len(event_assistant_dt_name) > 1 else None
        event['event_assistant_dt_name'] = event_assistant_dt_name

        event_assistant_dt_id = soup.find_all(class_="tournament-director")
        event_assistant_dt_id = event_assistant_dt_id[1] if len(event_assistant_dt_id) > 1 else None
        event_assistant_dt_id = event_assistant_dt_id.find('a') if event_assistant_dt_id else None
        event['event_assistant_dt_id'] = event_assistant_dt_id['href'] if event_assistant_dt_id else None

        event_website = soup.find(class_="tournament-website")
        event['event_website'] = event_website.text if event_website else None

        event_email = soup.find(class_="tournament-email")
        event_email = event_email.find('a') if event_email else None
        event['event_email'] = event_email['href'] if event_email else None

        event_phone = soup.find(class_="tournament-phone")
        event['event_phone'] = event_phone.text if event_phone else None

        live_scoring_links = soup.find(class_="live-scoring")
        live_scoring_links = live_scoring_links.find_all('a', href=True) if live_scoring_links else []
        live_score_link_list = []
        for link in live_scoring_links:
            live_score_link_list.append(link["href"])
        event['event_livescoring'] = live_score_link_list if live_score_link_list else None

        event_tier_classification = soup.find(class_="panel-pane pane-tournament-event-info")
        event_tier_classification = event_tier_classification.find("h4").text if event_tier_classification else None

        event["event_tier"] = event_tier_classification.split(' ')[1] if event_tier_classification else None
        event["event_classification"] = event_tier_classification.split(' ')[0] if event_tier_classification else None
        #import pdb; pdb.set_trace()

        event_total_players = soup.find("td", class_="players")
        event_total_players = event_total_players.text if event_total_players else None
        event_total_players_second_check = soup.find_all("td", class_="players") if not event_total_players else None
        event_total_players_second_check = event_total_players_second_check[1].text if event_total_players_second_check and len(event_total_players_second_check) > 1 else None
        event['event_total_players'] = event_total_players if event_total_players else event_total_players_second_check

        event_status = soup.find_all(class_="status")
        event['event_status'] = event_status[-1].text if len(event_status) > 1 else None

        event_status_last_updated = soup.find_all(class_="date updated")
        event['event_status_last_updated'] = event_status_last_updated[1].text if len(event_status_last_updated) > 1 else None

        event_pro_purse = soup.find_all(class_="purse")
        event['event_pro_purse'] = event_pro_purse[1].text if len(event_pro_purse) > 1 else None

        event_type = []

        singles = soup.find("div", {"class": re.compile('^(leaderboard singles).*$')})
        doubles = soup.find("div", {"class": re.compile('^(leaderboard doubles).*$')})
        teams = soup.find("div", {"class": re.compile('^(leaderboard team).*$')})

        if not teams:
            teams = soup.find("div", {"class": re.compile('^(leaderboard points-based).*$')})

        if not singles and not doubles and not teams:
            singles = soup.find("div", {"class": re.compile('^(leaderboard unknown).*$')})

        all_divisions = {}
        event['event_divisions'] = []

        if singles:
            singles_player_details = singles.find_all('details')
            for detail in singles_player_details:
                all_divisions[detail] = "singles"
            event_type.append("singles")
        if doubles:
            doubles_player_details = doubles.find_all('details')
            for detail in doubles_player_details:
                all_divisions[detail] = "doubles"
            event_type.append("doubles")
        if teams:
            teams_player_details= teams.find_all('details')
            for detail in teams_player_details:
                all_divisions[detail] = "teams"
            event_type.append("team")

        for division, division_type in all_divisions.items():
            div = {}
            division_name = division.find(class_="division")
            div['division_name'] = division_name.text if division_name else None
            div['division_short_name'] = division_name["id"] if division_name else None

            division_total_players = division.find(class_="players")
            div['division_total_players'] = division_total_players.text if division_total_players else None

            division_course_details = []

            round_course_infos = division.find_all("span", {"id" : re.compile('^(layout-details-).*$')})

            if round_course_infos:
                for round_number, course_info in enumerate(round_course_infos):
                    course_details = {}
                    round_number = f"round_{round_number+1}"

                    course_round_details = course_info.text if course_info else None
                    course_pdga_link = course_info.find('a') if course_info else None
                    course_pdga_link = course_pdga_link["href"] if course_pdga_link else None

                    course_details[round_number] = {"course_details": course_round_details, "course_pdga_link": course_pdga_link}

                    division_course_details.append(course_details)
            else:
                round_course_infos = division.find('tr').find_all(class_="round") + division.find('tr').find_all(class_="semi-finals") + division.find('tr').find_all(class_="finals")
                for round_number, course_info in enumerate(round_course_infos):
                    course_details = {}
                    round_number = f"round_{round_number+1}"
                    course_details[round_number] = {"course_details" : None, "course_pdga_link": None}
                    division_course_details.append(course_details)

            
            #### Double check that there is enough number of rounds
            validate_round_number = division.find("tbody")
            validate_round_number = validate_round_number.find("tr") if validate_round_number else None
            validate_round_number = validate_round_number.find_all("td", {"class" : re.compile('^(round-rating).*$')}) if validate_round_number else None

            if validate_round_number and len(division_course_details) != len(validate_round_number):
                division_course_details = []
                try:
                    SendSlackMessageToChannel("Course validation check failed for id %s" % (str(id)), "#debugging")
                except:
                    logger.info("Course validation check failed for id %s" % (str(id)))
                for i, _ in enumerate(validate_round_number):
                    course_details = {}
                    round_number = f"round_{i+1}"
                    course_details[round_number] = {"course_details" : None, "course_pdga_link": None}
                    division_course_details.append(course_details)

            #import pdb; pdb.set_trace()

            if division_type == "singles":
                all_players = division.find('tbody')
                all_players = all_players.find_all('tr') if all_players else []
                if all_players:
                    division_players = parse_singles_tournament(all_players, div)
                else:
                    division_players = []
            elif division_type == "doubles":
                all_players_odd = division.find('tbody').find_all('tr', class_="odd")
                all_players_even = division.find('tbody').find_all('tr', class_="even")
                division_players = parse_doubles_tournament(all_players_odd, all_players_even, div)
            else:
                all_players = division.find('tbody').find_all('tr')
                division_players = parse_teams_tournament(division, div)

            div['division_course_details'] = division_course_details
            div['division_players'] = division_players
            event['event_type'] = event_type

            event['event_divisions'].append(div)


        print(json.dumps(event, indent=4))
        return event

