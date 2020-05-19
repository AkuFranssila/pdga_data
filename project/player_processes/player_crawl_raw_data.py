# coding=utf-8
from bs4 import BeautifulSoup
import requests
import json
import logging
import tempfile
from datetime import date
from project.helpers.helpers_crawler import FindNewestMemberId
from project.helpers.helpers_data_management import AppendToFile
from project.utils.send_file_to_s3 import upload_data_to_s3
from profile.utils.s3_tools import save_to_temp_file_and_upload_to_s3
from project.utils.slack_message_sender import SendSlackMessageToChannel
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


def CrawlRawPlayerData(first_id, last_id, crawl_all, file_date, chunk_counter=0):
    SendSlackMessageToChannel("%s Starting run_player_crawl.py" % str(datetime.datetime.today()), "#data-reports")
    logging.info("Starting player raw data crawling %s" % file_date)
    if crawl_all:
        logging.info("Crawling all players. Running FindNewestMemberId")
        first_id = 1
        last_id = FindNewestMemberId()


    collected_json = []
    for i in range(first_id, last_id):
        logging.info('Crawling player with pdga number %s/%s' % (str(i), last_id))
        response = requests.get('https://www.pdga.com/player/' + str(i))
        data = response.content.decode('utf8').replace("'", '"')
        json_data = {"pdga_number" : i, "raw_data" : data}
        collected_json.append(json_data)

        if (i % 1000 == 0 or i == (last_id - 1)) and i > 0:
            save_to_temp_file_and_upload_to_s3("player-raw-data", file_date, chunk_counter, collected_json, suffix=".json")
            collected_json = []
            chunk_counter += 1

    SendSlackMessageToChannel("%s Finished run_player_crawl.py." % (str(datetime.datetime.today())), "#data-reports")

    

    