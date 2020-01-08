# coding=utf-8
from bs4 import BeautifulSoup
import requests
import json
import logging
from datetime import date
from helpers_crawler import FindNewestMemberId
from helpers_data_management import AppendToFile, ReturnFileLocation, DeleteFile
from send_file_to_s3 import send_file_to_s3
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


def PlayerCrawlRawData(first_id, last_id, crawl_all):
    first_id = first_id
    last_id = last_id
    if crawl_all:
        first_id = 1
        last_id = FindNewestMemberId()

    file_location = ReturnFileLocation("player", "crawl")

    for i in range(first_id, last_id):
        logging.info('Crawling player with pdga number %s' % str(i))
        response = requests.get('https://www.pdga.com/player/' + str(i))
        data = response.content.decode('utf8').replace("'", '"')
        json_data = {"pdga_number" : i, "raw_data" : data}
        AppendToFile('player', 'crawl',  json_data)

    file_send_status = send_file_to_s3(file_location, "player-raw-data")
    if file_send_status:
        DeleteFile(file_location)

# f = open('.\\crawled_players\\player_raw_data_2020-01-06.json', "r")
# for x in f:
#     print(x)
#     print('\n\n\n\n\n\n')
