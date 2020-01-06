# coding=utf-8
from bs4 import BeautifulSoup
import requests
import json
import logging
from datetime import date
from helpers_crawler import FindNewestMemberId
from helpers_data_management import AppendToFile
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


def PlayerCrawlRawData(first_id, last_id, crawl_all):
    first_id = first_id
    last_id = last_id
    if crawl_all:
        first_id = 1
        last_id = FindNewestMemberId()

    for i in range(first_id, last_id):
        logging.info('Crawling player with pdga number %s' % str(i))
        response = requests.get('https://www.pdga.com/player/' + str(i))
        data = response.content.decode('utf8').replace("'", '"')
        json_data = {"pdga_number" : i, "raw_data" : data}
        AppendToFile('player', 'crawl',  json_data)


# f = open('.\\crawled_players\\player_raw_data_2020-01-06.json', "r")
# for x in f:
#     print(x)
#     print('\n\n\n\n\n\n')
