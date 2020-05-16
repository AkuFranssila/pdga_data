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
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


def CrawlRawPlayerData(first_id, last_id, crawl_all, file_date, chunk_counter=0):
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

        if i % 1000 == 0 or i == last_id:
                #temp = tempfile.NamedTemporaryFile(suffix=".json", mode="w")

            with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False) as tp:
                tp.write(json.dumps(collected_json))
                s3_folder_key = f'player-raw-data/{file_date}/data_{str(chunk_counter)}.json'
                #import pdb; pdb.set_trace()
                upload_data_to_s3(s3_folder_key, tp.name)
                tp.close()
            collected_json = []
            chunk_counter += 1

    

    