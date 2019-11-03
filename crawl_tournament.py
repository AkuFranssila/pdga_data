# coding=utf-8
from bs4 import BeautifulSoup
import requests
import json
import logging
from datetime import date
from helpers_crawler import TournamentDate, TournamentLastPage
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


#https://www.pdga.com/tour/search?date_filter[min][date]=1979-1-1&date_filter[max][date]=2019-12-3&page=0

url = TournamentDate('latest')
last_page = TournamentLastPage(url)
tournament_data = []
tournament_links = []
for i in range(0, last_page):
    response = requests.get(url + '&page=' + str(i))
    soup = BeautifulSoup(response.content, "html.parser")
    all_links = soup.find_all('a')
    for link in all_links:
        try:
            if '/tour/event' in link['href']:
                tournament_links.append(link['href'])
                print ("https://www.pdga.com" + link['href'])
        except:
            None

for link in tournament_links:
    response = requests.get(link)
    soup = BeautifulSoup(response.content, "html.parser")

    event_title = soup.find(id="page-title").text
    event_date = soup.find(class_="tournament-date").text
    event_location = soup.find(class_="tournament-location").text
    event_tournament_director_name = soup.find(class_="tournament-director").text
    event_tournament_director_id = soup.find(class_="tournament-director").find('a')['href']
    event_assistant_dt_name = ""
    event_assistant_dt_id = ""
