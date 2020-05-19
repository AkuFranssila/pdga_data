# coding=utf-8
import json
import logging
import sys
import datetime
import argparse
from project.player_processes.player_crawl_raw_data import CrawlRawPlayerData
from project.helpers.helpers_data_management import ReturnFileLocation
from project.utils.slack_message_sender import SendSlackMessageToChannel

logging.getLogger().setLevel("INFO")

def handle_arguments() -> (int, int):
    parser = argparse.ArgumentParser()
    parser.add_argument('--start_id',
        type=int,
        help="Starting PDGA number from where to crawl"
    )
    parser.add_argument('--end_id',
        type=int,
        help="Ending PDGA number from where to crawl."
    )
    parser.add_argument('--all',
        action="store_true",
        help="Argument if all players should be crawled."
    )
    args = parser.parse_args()

    return args.start_id, args.end_id, args.all


if __name__ == "__main__":
    start_id, end_id, crawl_all = handle_arguments()
    SendSlackMessageToChannel("%s Starting run_player_crawl.py" % str(datetime.datetime.today()), "#data-reports")

    file_date = datetime.datetime.now().strftime("%m%d%Y")
    CrawlRawPlayerData(start_id, end_id, crawl_all, file_date)

    SendSlackMessageToChannel("%s Finished run_player_crawl.py." % (str(datetime.datetime.today())), "#data-reports")
