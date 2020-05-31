# coding=utf-8
import os
import json
import logging
import re
import datetime
import requests
import pycountry
from project.models.schemas import Player, Tournament
from project.helpers.helper_data import ACCEPTED_STATUSES, US_STATES, MONTH_DICT
from mongoengine import *
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


def add_plus_one_check_odd_even(count):
    added_count = count + 1
    even_or_odd = "even"
    if added_count % 2 == 0:
        even_or_odd = "odd"

    return even_or_odd


def parse_singles_tournament(players, div):
    division_players = []

    for count, player in enumerate(players):
        player_data = {}
        player_data['division_name'] = div['division_name']
        player_data['division_short_name'] = div['division_short_name']

        even_or_odd = add_plus_one_check_odd_even(count)

        player_name = player.find(class_="player").text

        propagator = player.find(class_="player-rating propagator")
        propagator = True if propagator else False

        rating_during_tournament = player.find("td", {"class" : re.compile('^(player-rating).*$')})
        rating_during_tournament = rating_during_tournament.text if rating_during_tournament else None
        rating_during_tournament = int(rating_during_tournament) if rating_during_tournament != "" and isinstance(rating_during_tournament, str) else None

        pdga_number = player.find(class_="pdga-number")
        pdga_number = pdga_number.text if pdga_number else None
        pdga_number = int(pdga_number) if pdga_number != "" and isinstance(pdga_number, str) else None

        pdga_page_link = "https://www.pdga.com/player/" + str(pdga_number) if pdga_number else None
        
        player_final_placement = player.find(class_="place")
        player_final_placement = player_final_placement.text if player_final_placement else None
        
        player_money_won = player.find(class_="prize")
        player_money_won = player_money_won.text if player_money_won else None
        if player_money_won == "":
            player_money_won = None
        
        player_total_throws = player.find(class_="total").text if player.find(class_="total") else None
        

        par_under = player.find(class_="par under").text if player.find(class_="par under") else None
        par_neutral = player.find(class_="par").text if player.find(class_="par") else None
        par_over = player.find(class_="par over").text if player.find(class_="par over") else None
        if par_under:
            player_total_par = par_under
        elif par_neutral:
            player_total_par = par_neutral
        else:
            player_total_par = par_over

        player_event_points = player.find(class_="points").text if player.find(class_="points") else "0.00"

        player_rounds = []
        for round_number, round in enumerate(player.find_all(class_="round")):
            round_data = {}
            round_data['round_number'] = round_number + 1

            round_throws = round.text
            if round_throws == "":
                round_throws = None
            round_data['round_throws'] = round_throws
            try:
                round_rating = player.find_all(class_="round-rating")[round_number].text
                if round_rating == "":
                    round_rating = None
                round_data['round_rating'] = round_rating
            except:
                round_data['round_rating'] = None

            player_rounds.append(round_data)

        player_data["player_full_names"] = [player_name]
        player_data["player_propagator"] = propagator
        player_data["player_rating_during_tournament"] = [rating_during_tournament]
        player_data["player_pdga_number"] = [pdga_number]
        player_data['player_pdga_link'] = [pdga_page_link]
        player_data['player_final_placement'] = player_final_placement
        player_data['player_money_won'] = player_money_won
        player_data['player_total_throws'] = player_total_throws
        player_data['player_total_par'] = player_total_par
        player_data['player_event_points'] = player_event_points
        player_data['player_rounds'] = player_rounds

        division_players.append(player_data)
        
    return division_players


def parse_doubles_tournament(player1, player2, div):
    division_players = []

    for count, (player_1, player_2) in enumerate(zip(player1, player2)):
        player_data = {}
        player_data['division_name'] = div['division_name']
        player_data['division_short_name'] = div['division_short_name']

        even_or_odd = add_plus_one_check_odd_even(count)

        player_names = []
        pdga_numbers = []
        pdga_page_links = []
        rating_during_tournaments = []

        player_name_1 = player_1.find(class_=f"{even_or_odd} player")
        player_name_1 = player_name_1.text if player_name_1 else None

        player_name_2 = player_2.find(class_=f"{even_or_odd} player")
        player_name_2 = player_name_2.text if player_name_2 else None

        player_names.append(player_name_1)
        player_names.append(player_name_2)

        propagator = player_1.find(class_=f"{even_or_odd} player-rating propagator")
        propagator = True if propagator else False


        rating_during_tournament_p1 = player_1.find("td", {"class" : re.compile('^(even player-rating|odd player-rating).*$')})
        rating_during_tournament_p1 = rating_during_tournament_p1.text if rating_during_tournament_p1 else None
        rating_during_tournament_p1 = int(rating_during_tournament_p1) if rating_during_tournament_p1 != "" and isinstance(rating_during_tournament_p1, str) else None

        rating_during_tournament_p2 = player_2.find("td", {"class" : re.compile('^(even player-rating|odd player-rating).*$')})
        rating_during_tournament_p2 = rating_during_tournament_p2.text if rating_during_tournament_p2 else None
        rating_during_tournament_p2 = int(rating_during_tournament_p2) if rating_during_tournament_p2 != "" and isinstance(rating_during_tournament_p2, str) else None

        rating_during_tournaments.append(rating_during_tournament_p1)
        rating_during_tournaments.append(rating_during_tournament_p2)

        raw_pdga_numbers = [player_1.find("td", {"class" : re.compile('^(even pdga-number|odd pdga-number).*$')}), player_2.find("td", {"class" : re.compile('^(even pdga-number|odd pdga-number).*$')})]
        for number in raw_pdga_numbers:
            if number:
                if number.text != "":
                    pdga_numbers.append(int(number.text))
                else:
                    pdga_numbers.append(None)
            else:
                pdga_numbers.append(None)
        
        pdga_page_link_p1 = "https://www.pdga.com/player/" + str(pdga_numbers[0]) if pdga_numbers[0] else None
        pdga_page_link_p2 = "https://www.pdga.com/player/" + str(pdga_numbers[1]) if pdga_numbers[1] else None

        pdga_page_links.append(pdga_page_link_p1)
        pdga_page_links.append(pdga_page_link_p2)
        
        player_final_placement = player_1.find(class_=f"{even_or_odd} place")
        player_final_placement = player_final_placement.text if player_final_placement else None
        
        player_money_won = player_1.find(class_=f"{even_or_odd} prize")
        player_money_won = player_money_won.text if player_money_won else None
        if player_money_won == "":
            player_money_won = None
        
        player_total_throws = player_1.find(class_=f"{even_or_odd} total").text if player_1.find(class_=f"{even_or_odd} total") else None
        

        par_under = player_1.find(class_=f"{even_or_odd} par under").text if player_1.find(class_=f"{even_or_odd} par under") else None
        par_neutral = player_1.find(class_=f"{even_or_odd} par").text if player_1.find(class_=f"{even_or_odd} par") else None
        par_over = player_1.find(class_=f"{even_or_odd} par over").text if player_1.find(class_=f"{even_or_odd} par over") else None
        if par_under:
            player_total_par = par_under
        elif par_neutral:
            player_total_par = par_neutral
        else:
            player_total_par = par_over

        player_event_points = player_1.find(class_=f"{even_or_odd} points").text if player_1.find(class_=f"{even_or_odd} points") else "0.00"

        player_rounds = []
        for round_number, round in enumerate(player_1.find_all(class_=f"{even_or_odd} round")):
            round_data = {}
            round_data['round_number'] = round_number + 1

            round_throws = round.text
            if round_throws == "":
                round_throws = None
            round_data['round_throws'] = round_throws
            try:
                round_rating = player_1.find_all(class_=f"{even_or_odd} round-rating")[round_number].text
                if round_rating == "":
                    round_rating = None
                round_data['round_rating'] = round_rating
            except:
                round_data['round_rating'] = None

            player_rounds.append(round_data)

        player_data["player_full_names"] = player_names
        player_data["player_propagator"] = propagator
        player_data["player_rating_during_tournament"] = rating_during_tournaments
        player_data["player_pdga_number"] = pdga_numbers
        player_data['player_pdga_link'] = pdga_page_links
        player_data['player_final_placement'] = player_final_placement
        player_data['player_money_won'] = player_money_won
        player_data['player_total_throws'] = player_total_throws
        player_data['player_total_par'] = player_total_par
        player_data['player_event_points'] = player_event_points
        player_data['player_rounds'] = player_rounds

        division_players.append(player_data)

    return division_players



def parse_teams_tournament(soup_div, div):
    #https://www.pdga.com/tour/event/11912
    #if team names the format is same as singles tournament

    division_players = []

    all_players = soup_div.find_all("tr", {"class" : re.compile('^(even|odd).*$')})

    if not soup_div.find("td", class_="even player"):
        #This is team event with names. Run singles parser
        division_players = parse_singles_tournament(all_players, div)
        return division_players


    players_by_position = {}

    current_position = ""
    for player in all_players:
        #Check if place information found
        position = player.find("td", {"class" : re.compile('^(even place|odd place).*$')})
        if position:
            current_position =  position.text
            players_by_position[position.text] = [player]
        else:
            players_by_position[current_position].append(player)
        
    for position, players in players_by_position.items():

        team_players = []
        team_pdga_numbers = []
        team_ratings = []
        team_pdga_links = []
        player_data = {}
        for player in players:
            player_data['division_name'] = div['division_name']
            player_data['division_short_name'] = div['division_short_name']

            player_name = player.find("td", {"class" : re.compile('^(even player|odd player).*$')}).text

            propagator = player.find("td", {"class" : re.compile('^(even player-rating propagator|odd player-rating propagator).*$')})
            propagator = True if propagator else False
            
            rating_during_tournament_1 = player.find("td", {"class" : re.compile('^(even player-rating propagator|odd player-rating propagator).*$')})
            rating_during_tournament_1 = None if rating_during_tournament_1 == "" else None
            rating_during_tournament_1 = int(rating_during_tournament_1.text) if rating_during_tournament_1 else None
            rating_during_tournament_2 = player.find("td", {"class" : re.compile('^(even player-rating|odd player-rating).*$')})
            rating_during_tournament_2 = None if rating_during_tournament_2 == "" else None
            rating_during_tournament_2 = int(rating_during_tournament_2.text) if rating_during_tournament_2 else None
            rating_during_tournament = rating_during_tournament_1 if rating_during_tournament_1 else rating_during_tournament_2
            
            pdga_number = player.find("td", {"class" : re.compile('^(even pdga-number|odd pdga-number).*$')})
            pdga_number = pdga_number.text if pdga_number else None
            pdga_number = int(pdga_number) if pdga_number != "" and isinstance(pdga_number, str) else None
            
            pdga_page_link = "https://www.pdga.com/player/" + str(pdga_number) if pdga_number else None
            
            player_final_placement = position
            
            player_money_won = player.find("td", {"class" : re.compile('^(even prize|odd prize).*$')})
            player_money_won = player_money_won.text if player_money_won else None
            if player_money_won == "":
                player_money_won = None
            
            player_total_throws = player.find("td", {"class" : re.compile('^(even total|odd total).*$')}).text if player.find({"class" : re.compile('^(even total|odd total).*$')}) else None
            

            par_neutral = player.find("td", {"class" : re.compile('^(even par|odd par).*$')}).text if player.find({"class" : re.compile('^(even par|odd par).*$')}) else None
            player_total_par = par_neutral

            player_event_points = player.find("td", {"class" : re.compile('^(even points|odd points).*$')}).text if player.find({"class" : re.compile('^(even points|odd points).*$')}) else "0.00"

            player_rounds = []
            for round_number, round in enumerate(player.find_all("td", {"class" : re.compile('^(even round|odd round)$')})):
                round_data = {}
                round_data['round_number'] = round_number + 1

                round_throws = round.text
                if round_throws == "":
                    round_throws = None
                round_data['round_throws'] = round_throws
                try:
                    round_rating = player.find_all("td", {"class" : re.compile('^(even round-rating|odd round-rating)$')})[round_number].text
                    if round_rating == "":
                        round_rating = None
                    round_data['round_rating'] = round_rating
                except:
                    round_data['round_rating'] = None

                player_rounds.append(round_data)

            team_players.append(player_name)
            team_pdga_numbers.append(pdga_number)
            player_data["player_propagator"] = propagator
            team_ratings.append(rating_during_tournament)
            team_pdga_links.append(pdga_page_link)
            player_data['player_final_placement'] = player_final_placement
            player_data['player_money_won'] = player_money_won
            player_data['player_total_throws'] = player_total_throws
            player_data['player_total_par'] = player_total_par
            player_data['player_event_points'] = player_event_points
            player_data['player_rounds'] = player_rounds

        player_data["player_full_names"] = team_players
        player_data["player_pdga_number"] = team_pdga_numbers
        player_data["player_rating_during_tournament"] = team_ratings
        player_data["player_pdga_link"] = team_pdga_links
        division_players.append(player_data)

    return division_players