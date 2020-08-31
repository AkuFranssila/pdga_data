import argparse
from pdga_v2.parsers.player_raw_parser import PlayerRawParser

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
    parser.add_argument('--parse_all',
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
    parser.add_argument('--raw_data_folder',
        type=str,
        help="Give subfolder name where to store data. Usually in format year-month-day"
    )
    parser.add_argument('--is_subprocess',
        action="store_true",
        help="True False if parser is subprocess. If not subprocess then it will create subprocesses."
    )
    args = parser.parse_args()

    return args.start_id, args.end_id, args.test_id, args.parse_all, args.send, args.print_results, args.subfolder, args.raw_data_folder, args.is_subprocess

def run(start_id, end_id, test_id, parse_all, send, print_results, subfolder, raw_data_folder, is_subprocess):
    player = PlayerRawParser({
        "test_id": test_id,
        "crawl_start_id": start_id,
        "crawl_end_id": end_id,
        "parse_all": parse_all,
        "send_results": send,
        "print_results": print_results,
        "folder_date": subfolder,
        "raw_data_folder": raw_data_folder,
        "is_subprocess": is_subprocess,
    })
    player._run()


if __name__ == "__main__":
    start_id, end_id, test_id, parse_all, send, print_results, subfolder, raw_data_folder, is_subprocess = handle_arguments()
    run(start_id, end_id, test_id, parse_all, send, print_results, subfolder, raw_data_folder, is_subprocess)