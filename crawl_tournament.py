# coding=utf-8
from bs4 import BeautifulSoup
import requests
import json
import logging
from datetime import date
from helpers_crawler import TournamentDate, TournamentLastPage
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


#https://www.pdga.com/tour/search?date_filter[min][date]=1979-1-1&date_filter[max][date]=2019-12-3&page=0

url = TournamentDate('test')
last_page = TournamentLastPage(url)
tournament_data = []
tournament_links = []
for i in range(0, last_page):
    response = requests.get(url + '&page=' + str(i))
    soup = BeautifulSoup(response.content, "html.parser")
    all_links = soup.find_all('a')
    for link in all_links:
        try:
            if '/tour/event/' in link['href']:
                tournament_links.append("https://www.pdga.com" + link['href'])
                #print ("https://www.pdga.com" + link['href'])
        except:
            None

logging.info(f'Number of tournaments found {str(len(tournament_links))}')

for link in tournament_links:
    response = requests.get(link)
    soup = BeautifulSoup(response.content, "html.parser")
    logging.info(f'Checking tournament {link}')
    event = {}
    event['event_link'] = link
    #Basic info
    event['event_title'] = soup.find(id="page-title").text
    event['event_date'] = soup.find(class_="tournament-date").text
    event['event_location'] = soup.find(class_="tournament-location").text
    event['event_tournament_director_name'] = soup.find(class_="tournament-director").text
    event['event_tournament_director_id'] = soup.find(class_="tournament-director").find('a')['href']
    event['event_assistant_dt_name'] = soup.find_all(class_="tournament-director")[1].text
    event['event_assistant_dt_id'] = soup.find_all(class_="tournament-director")[1].find('a')['href']
    event['event_website'] = soup.find(class_="tournament-website").text
    event['event_email'] = soup.find(class_="tournament-email").find('a')['href']
    event['event_phone'] = soup.find(class_="tournament-phone").text

    #Tournament categorization
    event['event_tier'] = soup.find_all(class_="tier")[1].text
    event['event_classification'] = soup.find_all(class_="classification")[1].text
    event['event_total_players'] = soup.find_all(class_="players")[1].text
    event['event_pro_purse'] = soup.find_all(class_="purse")[1].text


    #Player parsing
    event['event_divisions'] = []
    all_divisions = soup.find_all('details')
    for division in all_divisions:
        div = {}
        logging.info('Division name ' + division.find(class_="division").text)
        div['division_name'] = division.find(class_="division").text
        div['division_short_name'] = division.find(class_="division")['id']
        div['division_total_players'] = division.find(class_="players").text
        div['division_players'] = []
        all_players = division.find('tbody').find_all('tr')
        for player in all_players:
            player_data = {}
            logging.info('Player name ' + player.find(class_="player").text)
            player_data['division_name'] = div['division_name']
            player_data['division_short_name'] = div['division_short_name']
            player_data['player_full_name'] = player.find(class_="player").text
            player_data['player_pdga_number'] = player.find(class_="pdga-number").text
            player_data['player_pdga_link'] = "https://www.pdga.com" + player.find(class_="player").find('a')['href']
            try:
                player_data['player_propagator'] = player.find(class_="player-rating propagator").text #if found then true, otherwise false
                player_data['player_propagator'] = True
            except:
                player_data['player_propagator'] = False
            try:
                player_data['player_rating_during_tournament'] = player.find(class_="player-rating propagator").text
            except:
                player_data['player_rating_during_tournament'] = player.find(class_="player-rating").text
            player_data['player_final_placement'] = player.find(class_="place").text
            player_data['player_money_won'] = player.find(class_="prize").text
            player_data['player_total_throws'] = player.find(class_="total").text
            try:
                player_data['player_total_par'] = player.find(class_="par under").text
            except:
                try:
                    player_data['player_total_par'] = player.find(class_="par").text
                except:
                    try:
                        player_data['player_total_par'] = player.find(class_="par over").text
                    except:
                        player_data['player_total_par'] = "DNF/DNS"
            player_data['player_event_points'] = player.find(class_="points").text
            player_data['player_rounds'] = []
            for round_number, round in enumerate(player.find_all(class_="round")):
                round_data = {}
                round_data['round_number'] = round_number + 1
                round_data['round_throws'] = round.text
                round_data['round_rating'] = player.find_all(class_="round-rating")[round_number].text
                player_data['player_rounds'].append(round_data)
            div['division_players'].append(player_data)

        event['event_divisions'].append(div)

    print (json.dumps(event, indent=4))
