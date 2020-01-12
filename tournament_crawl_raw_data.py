# coding=utf-8
from bs4 import BeautifulSoup
import requests
import json
import logging
from datetime import date
from helpers_crawler import TournamentDate, TournamentLastPage
from helpers_data_management import AppendToFile, ReturnFileLocation, DeleteFile
from send_file_to_s3 import send_file_to_s3
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


def TournamentCrawlRawData(options, file_location):
    url = TournamentDate(options)
    last_page = TournamentLastPage(url)
    tournament_data = []
    tournament_links = []
    for i in range(0, last_page):
        response = requests.get(url + '&page=' + str(i))
        soup = BeautifulSoup(response.content, "html.parser")
        all_links = soup.find_all('a')
        for link in all_links:
            try:
                link = "https://www.pdga.com" + link['href']
                if 'https://www.pdga.com/tour/event/' in link and link not in tournament_links:
                    tournament_links.append(link)
                    #print ("https://www.pdga.com" + link['href'])
            except:
                None

    logging.info(f'Number of tournaments found {str(len(tournament_links))}')

    for count, link in enumerate(tournament_links):
        logging.info(f'Parsing tournament number {str(count)}/{str(len(tournament_links))}')
        response = requests.get(link)
        data = response.content.decode('utf8').replace("'", '"')
        json_data = {"pdga_number" : i, "raw_data" : data}
        AppendToFile(file_location,  json_data)

    file_send_status = send_file_to_s3(file_location, "tournament-raw-data")
    if file_send_status:
        DeleteFile(file_location)
