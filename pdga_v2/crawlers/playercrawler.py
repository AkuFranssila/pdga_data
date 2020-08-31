import logging
import requests
import datetime
import json

from pdga_v2.utils.s3_utils.s3_upload_utils import save_to_temp_file_and_upload_to_s3

from bs4 import BeautifulSoup

logging.getLogger().setLevel("INFO")

class PlayerCrawler:
    def __init__(self, params):
        logging.info("Initializing PlayerCrawler")
        self.test_id = params.get("test_id")
        self.crawl_start_id = params.get("start_id")
        self.crawl_end_id = params.get("end_id")
        self.crawl_all = params.get("crawl_all")
        self.send_results = params.get("send_results")
        self.print_results = params.get("print_results")
        self.folder_date = params.get("folder_date")
        self.raw_crawled_data = None

        if not self.folder_date:
            logging.info("Folder date not found. Setting the folder_date to %s", datetime.datetime.now().strftime("%Y%m%d"))
            self.folder_date = datetime.datetime.now().strftime("%Y%m%d")

        if self.crawl_all:
            self.crawl_start_id = 1
            self.crawl_end_id = self._crawl_latest_player_id()
        elif not self.crawl_start_id and self.crawl_end_id:
            self.crawl_start_id = 1
        elif self.crawl_start_id and not self.crawl_end_id:
            self.crawl_end_id = self._crawl_latest_player_id()
        elif not self.crawl_start_id and not self.crawl_end_id and not self.test_id:
            raise ValueError("Please define what you wish to crawl in the parameters.")

        if self.crawl_start_id and self.crawl_end_id:
            self.crawl_end_id += 1
        

    def _crawl_latest_player_id(self):
        """
        Get latest player ID from PDGA.
        """
        def validate_latest_player_id(player_id):
            if player_id.isdigit():
                player_id = int(player_id)
                if player_id < 100_000:
                    raise ValueError("Player ID was less than 100 000. The number can not be correct.")
            else:
                raise ValueError("Player ID was not convertable to INT. Check PlayerCrawler.crawl_latest_player_id()")


            return player_id

        response = requests.get('https://www.pdga.com/players?FirstName=&LastName=&PDGANum=&Status=All&Class=All&MemberType=All&City=&StateProv=All&Country=All&Country_1=All&UpdateDate=&order=PDGANum&sort=desc')
        soup = BeautifulSoup(response.content, "html.parser")
        latest_player_id = soup.find(class_="odd views-row-first").find_all('td')[1].text.strip()
        latest_player_id = validate_latest_player_id(latest_player_id)

        logging.info("Latest player ID crawled and validated. Latest ID is %s", latest_player_id)

        return latest_player_id


    def _crawl_player_data(self, player_id):
        player_url = f"https://www.pdga.com/player/{str(player_id)}"
        logging.info("Crawling %s", player_url)
        response = requests.get(player_url)
        data = response.content.decode('utf8').replace("'", '"')

        player_data = {
            "url": player_url,
            "pdga_number": player_id,
            "html": data,
            "crawled-datetime": str(datetime.datetime.now()),
            "status_code": response.status_code,
        }

        self.raw_crawled_data = player_data

        return player_data


    def _loop_through_player_ids(self):
        logging.info("Starting to loop through player IDs from %s to %s", self.crawl_start_id, self.crawl_end_id)
        for i in range(self.crawl_start_id, self.crawl_end_id):
            crawled_data = self._crawl_player_data(i)
            if self.send_results:
                save_to_temp_file_and_upload_to_s3("player-raw-data", self.folder_date, "player_raw_", str(i), crawled_data)
            if self.print_results:
                print(json.dumps(crawled_data, indent=4))


    def _run(self):
        if self.test_id:
            crawled_data = self._crawl_player_data(self.test_id)
            if self.send_results:
                save_to_temp_file_and_upload_to_s3("player-raw-data", self.folder_date, "player_raw_", str(self.test_id), crawled_data)
            if self.print_results:
                print(json.dumps(crawled_data, indent=4))
        else:
            self._loop_through_player_ids()
