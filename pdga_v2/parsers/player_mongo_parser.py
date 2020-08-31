import logging
import requests
import datetime
import json
import asyncio
import subprocess

from pdga_v2.helpers.parser_helpers.player_mongo_parser_helpers import player_mongo_field_parser

from pdga_v2.utils.s3_utils.s3_general_utils import find_all_keys_from_s3_folder
from pdga_v2.utils.s3_utils.s3_download_utils import download_object_s3

import numpy as np

logging.getLogger().setLevel("INFO")
CURRENT_DATE = datetime.datetime.now().strftime("%Y%m%d")
S3_ROOT_DOWNLOAD_FOLDER_NAME = "player-parsed-data"

class PlayerMongoParser:
    def __init__(self, params):
        logging.info("Initializing PlayerMongoParser")
        self.test_id = params.get("test_id")
        self.crawl_start_id = params.get("crawl_start_id")
        self.crawl_end_id = params.get("crawl_end_id")
        self.parse_all = params.get("parse_all")
        self.send_results = params.get("send_results")
        self.print_results = params.get("print_results")
        self.raw_data_folder = params.get("raw_data_folder")
        self.folder_date = params.get("folder_date")
        self.is_subprocess = params.get("is_subprocess", False)
        self.parsed_data = None
        self.folder_keys = []
        self.subprocess_start_end_arrays = []

        if not self.folder_date:
            logging.info("Folder date not found. Setting the folder_date to %s", CURRENT_DATE)
            self.folder_date = CURRENT_DATE

        if not self.raw_data_folder:
            logging.info("Raw data folder not given. Checking if folder with current name %s exists", CURRENT_DATE)
            file_names = find_all_keys_from_s3_folder(f'{S3_ROOT_DOWNLOAD_FOLDER_NAME}/{CURRENT_DATE}')
            if file_names:
                self.raw_data_folder = CURRENT_DATE

        self.folder_keys = find_all_keys_from_s3_folder(f'{S3_ROOT_DOWNLOAD_FOLDER_NAME}/{self.raw_data_folder}')

        if self.parse_all:
            self.crawl_start_id = 1
            self.crawl_end_id = len(self.folder_keys)
        elif not self.crawl_start_id and self.crawl_end_id:
            self.crawl_start_id = 1
        elif self.crawl_start_id and not self.crawl_end_id:
            self.crawl_end_id = len(self.folder_keys)
        elif not self.crawl_start_id and not self.crawl_end_id and not self.test_id:
            raise ValueError("Please define what you wish to crawl in the parameters.")

        if self.crawl_start_id and self.crawl_end_id:
            self.crawl_end_id += 1

        if not self.test_id:
            self._split_ids_to_parse_to_chunks()


    def _split_ids_to_parse_to_chunks(self):
        """
        We want to create subprocesses for smaller chunks to make the parsing faster. Here we create chunks of IDs based on the start and end IDs.
        """
        chunk_count = self.crawl_end_id // 1_000
        if chunk_count == 0:
            chunk_count = 1

        chunked_lists = np.array_split(range(self.crawl_start_id, self.crawl_end_id), chunk_count)
        self.subprocess_start_end_arrays = chunked_lists


    def _parse_player_to_mongo(self, pdga_number):
        player_s3_key = f"{S3_ROOT_DOWNLOAD_FOLDER_NAME}/{self.raw_data_folder}/player_parsed_{str(pdga_number)}.json"
        json_data = download_object_s3(player_s3_key)
        parsed_data = asyncio.run(player_mongo_field_parser(json_data))
        self.parsed_data = parsed_data

    def _loop_through_player_ids(self):
        logging.info("Starting to loop through player IDs from %s to %s", self.crawl_start_id, self.crawl_end_id)
        for i in range(self.crawl_start_id, self.crawl_end_id):
            self._parse_player_to_mongo(i)
            if self.send_results:
               #save data to mongo
               print("Would save data to mongo here")
            if self.print_results:
                print(json.dumps(self.parsed_data, indent=4))


    def _create_subprocess_parsers(self):
        """
        Create subprocceses of pdga_v2.runners.run_player_raw_parser to run parsing faster.
        """

        for subprocess_list in self.subprocess_start_end_arrays:
            subprocess_arguments = [
                "python", "-m", 
                "pdga_v2.runners.run_player_mongo_parser",
                "--start_id", str(subprocess_list[0]), 
                "--end_id", str(subprocess_list[-1]), 
                "--raw_data_folder", self.raw_data_folder, 
                "--subfolder", self.folder_date,
                "--is_subprocess",
            ]
            if self.send_results:
                subprocess_arguments.append("--send")
            if self.print_results:
                subprocess_arguments.append("--print_results")
            subprocess.Popen(subprocess_arguments)


    def _run(self):
        if self.is_subprocess:
            self._loop_through_player_ids()
        elif self.test_id:
            self._parse_player_to_mongo(self.test_id)
            if self.send_results:
                #save data to mongo
               print("Would save data to mongo here")
            if self.print_results:
                print(json.dumps(self.parsed_data, indent=4))
        else:
            self._create_subprocess_parsers()
