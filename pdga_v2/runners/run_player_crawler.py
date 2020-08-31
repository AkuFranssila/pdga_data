import argparse
from pdga_v2.crawlers.playercrawler import PlayerCrawler

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
    parser.add_argument('--test_id',
        type=int,
        help="Give single pdga number to test."
    )
    parser.add_argument('--crawl_all',
        action="store_true",
        help="Argument if all players should be crawled."
    )
    parser.add_argument('--send',
        action="store_true",
        help="True False if results should be sent to S3."
    )
    parser.add_argument('--print_results',
        action="store_true",
        help="True False if results should be printed."
    )
    parser.add_argument('--subfolder',
        type=str,
        help="Give subfolder name where to store data. Usually in format year-month-day"
    )
    args = parser.parse_args()

    return args.start_id, args.end_id, args.test_id, args.crawl_all, args.send, args.print_results, args.subfolder

def run(start_id, end_id, test_id, crawl_all, send, print_results, subfolder):
    player = PlayerCrawler({
        "test_id": test_id,
        "crawl_start_id": start_id,
        "crawl_end_id": end_id,
        "crawl_all": crawl_all,
        "send_results": send,
        "print_results": print_results,
        "folder_date": subfolder,
    })
    player._run()


if __name__ == "__main__":
    start_id, end_id, test_id, crawl_all, send, print_results, subfolder = handle_arguments()
    run(start_id, end_id, test_id, crawl_all, send, print_results, subfolder)