# coding=utf-8
import json
import logging
import sys
import datetime
import argparse
from project.tournament_processes.tournament_crawl_raw_data import TournamentCrawlRawData
from project.utils.slack_message_sender import SendSlackMessageToChannel
logging.getLogger().setLevel("INFO")

def handle_arguments() -> (str):
    parser = argparse.ArgumentParser()
    parser.add_argument('--crawl_options',
        type=str,
        choices=["all", "latest", "test"],
        help="Predefined options what to crawl. Check project\helpers\helpers_crawler.py for more info."
    )

    args = parser.parse_args()

    return args.crawl_options


if __name__ == "__main__":
    crawl_options = handle_arguments()
    SendSlackMessageToChannel("%s Starting run_tournament_crawl.py" % str(datetime.datetime.today()), "#data-reports")

    file_date = datetime.datetime.now().strftime("%m%d%Y")
    TournamentCrawlRawData(crawl_options, file_date)

    SendSlackMessageToChannel("%s Finished run_tournament_crawl.py." % (str(datetime.datetime.today())), "#data-reports")
