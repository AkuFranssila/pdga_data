# coding=utf-8
from bs4 import BeautifulSoup
import requests
import json
import logging
import datetime
from project.helpers.helpers_crawler import TournamentDate, TournamentLastPage
from project.utils.s3_tools import save_to_temp_file_and_upload_to_s3
from project.utils.slack_message_sender import SendSlackMessageToChannel
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

SendSlackMessageToChannel("%s Starting tournament_crawl_raw_data.py" % str(datetime.datetime.today()), "#data-reports")

def TournamentCrawlRawData(options, file_date, chunk_counter=0):
    url = TournamentDate(options)
    last_page = TournamentLastPage(url)
    tournament_links = []
    for i in range(0, last_page):
        response = requests.get(url + '&page=' + str(i))
        soup = BeautifulSoup(response.content, "html.parser")
        all_links = soup.find_all('a')
        for link in all_links:
            try:
                link = "https://www.pdga.com" + link['href']
                if 'https://www.pdga.com/tour/event/' in link and link not in tournament_links and "/global-event/results/" not in link:
                    tournament_links.append(link)
            except:
                None

    logging.info(f'Number of tournaments found {str(len(tournament_links))}')
    SendSlackMessageToChannel("%s Tournament link collection done. Found %s tournament links." % (str(datetime.datetime.today()), str(len(tournament_links))), "#data-reports")

    collected_json = []

    for count, link in enumerate(tournament_links):
        logging.info(f'Parsing tournament number {str(count)}/{str(len(tournament_links))}')
        response = requests.get(link)
        data = response.content.decode('utf8').replace("'", '"')
        json_data = {"pdga_number" : int(link.rsplit("/", 1)[1]), "raw_data" : data}

        collected_json.append(json_data)

        print(count)
        print(len(tournament_links))

        if (count % 1000 == 0 or count == (len(tournament_links) - 1)) and count > 0:
            save_to_temp_file_and_upload_to_s3("tournament-raw-data", file_date, chunk_counter, collected_json, suffix=".json")
            collected_json = []
            chunk_counter += 1


    SendSlackMessageToChannel("%s Tournament page crawling and S3 upload done." % (str(datetime.datetime.today())), "#data-reports")

    
