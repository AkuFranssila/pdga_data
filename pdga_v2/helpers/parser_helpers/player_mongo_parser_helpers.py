import logging
import requests
import datetime
import json
import argparse
import re
import asyncio
import time

import pycountry

from pdga_v2.models.player import Player

from pdga_v2.helpers.mapping_helpers.us_states import US_STATE_SHORT_FULL
from pdga_v2.helpers.mapping_helpers.pdga_field_mapping import PDGA_PLAYER_CLASSIFICATION
from pdga_v2.helpers.mapping_helpers.date_time_mapping import MONTH_SHORT_TO_NUMBER

from pdga_v2.utils.general_utils.mongo_connect import ConnectMongo

logging.getLogger().setLevel("INFO")
ConnectMongo()

def handle_arguments() -> (str):
    parser = argparse.ArgumentParser()
    parser.add_argument('--local_file',
        type=str,
        help="Local file path to test single player parsing without S3",
    )
    args = parser.parse_args()

    return args.local_file


async def player_mongo_field_parser(raw_data):
    """
        Only parse raw data fields and turn them into the correct field formats as defined in Schema.
    """
    start_time = time.perf_counter()

    async def _parse_player_name(parsed_data):

        fields_to_update = {
            "first_name": None,
            "middle_name": None,
            "last_name": None,
        }

        if parsed_data.get("full_name"):
            split_name = parsed_data.get("full_name").split(' ')
            if len(split_name) == 2:
                fields_to_update["first_name"] = split_name[0]
                fields_to_update["last_name"] = split_name[1]
            elif len(split_name) == 3:
                if split_name[1] in ["De", "Van", "Von"]:
                    fields_to_update["first_name"] = split_name[0]
                    fields_to_update["last_name"] = f"{split_name[1]} {split_name[2]}"

        parsed_data.update(fields_to_update)


    async def _parse_location_fields(parsed_data):
        fields_to_update = {
            "full_location": parsed_data.get("full_location"),
            "city": parsed_data.get("city"),
            "state": None,
            "state_short": parsed_data.get("state_short"),
            "country": None,
            "country_short": parsed_data.get("country_short"),
        }

        if fields_to_update["full_location"]:
            split_full_location = fields_to_update["full_location"].split(", ")
            if fields_to_update["city"]:
                fields_to_update["city"] = fields_to_update["city"].replace('%20', ' ')

            if "United States" in split_full_location[-1]:
                fields_to_update["country_short"] = "US"

            if fields_to_update["country_short"]:
                try:
                    fields_to_update["country"] = pycountry.countries.get(alpha_2=fields_to_update["country_short"]).name
                except AttributeError:
                    logging.info("Country code %s was not found from pycountry", fields_to_update["country_short"])

            if fields_to_update["state_short"] and fields_to_update["country_short"] == "US":
                fields_to_update["state"] = US_STATE_SHORT_FULL.get(fields_to_update["state_short"])

        parsed_data.update(fields_to_update)

    
    async def _parse_classification(parsed_data):
        fields_to_update = {
            "classification": parsed_data.get("classification"),
            "classification_short": None,
        }

        if fields_to_update["classification"]:
           fields_to_update["classification"] = fields_to_update["classification"].replace("Classification:", "").strip()
           fields_to_update["classification_short"] = PDGA_PLAYER_CLASSIFICATION.get(fields_to_update["classification"])

        parsed_data.update(fields_to_update)


    async def _parse_member_since(parsed_data):
        fields_to_update = {
            "member_since": parsed_data.get("member_since"),
        }

        if fields_to_update["member_since"]:
           fields_to_update["member_since"] = fields_to_update["member_since"].replace("Member Since:", "").strip()
           fields_to_update["member_since"] = int(fields_to_update["member_since"])

        parsed_data.update(fields_to_update)


    async def _parse_membership_status(parsed_data):
        fields_to_update = {
            "membership_status": parsed_data.get("membership_status"),
        }

        if fields_to_update["membership_status"]:
           fields_to_update["membership_status"] = fields_to_update["membership_status"].replace("Membership Status:", "").strip()
           fields_to_update["membership_status"] = fields_to_update["membership_status"].split('(')[0].strip()

        parsed_data.update(fields_to_update)


    async def _parse_membership_expiration_date(parsed_data):
        fields_to_update = {
            "membership_expiration_date": parsed_data.get("membership_expiration_date"),
        }

        if fields_to_update["membership_expiration_date"]:
            matched_date = re.search(r"(\d{2})-(\w{3})-(\d{4})", fields_to_update["membership_expiration_date"])
            if matched_date:
                matched_date = matched_date.group(0)
                day, month, year = matched_date.split('-')
                month = MONTH_SHORT_TO_NUMBER.get(month)
                formatted_date = f"{year}-{month}-{day}"
                fields_to_update["membership_expiration_date"] = formatted_date

        parsed_data.update(fields_to_update)


    async def _parse_rating(parsed_data):
        fields_to_update = {
            "rating": parsed_data.get("rating"),
        }

        if fields_to_update["rating"]:
            fields_to_update["rating"] = fields_to_update["rating"].replace("Current Rating:", "").strip().split(' ')[0]
            fields_to_update["rating"] = int(fields_to_update["rating"])

        parsed_data.update(fields_to_update)


    async def _parse_rating_difference(parsed_data):
        fields_to_update = {
            "rating_difference": parsed_data.get("rating_difference"),
        }

        if fields_to_update["rating_difference"]:
            fields_to_update["rating_difference"] = int(fields_to_update["rating_difference"].strip())

        parsed_data.update(fields_to_update)


    async def _parse_rating_updated(parsed_data):
        fields_to_update = {
            "rating_updated": parsed_data.get("rating_updated"),
        }

        if fields_to_update["rating_updated"]:
            matched_date = re.search(r"(\d{2})-(\w{3})-(\d{4})", fields_to_update["rating_updated"])
            if matched_date:
                matched_date = matched_date.group(0)
                day, month, year = matched_date.split('-')
                month = MONTH_SHORT_TO_NUMBER.get(month)
                formatted_date = f"{year}-{month}-{day}"
                fields_to_update["rating_updated"] = formatted_date

        parsed_data.update(fields_to_update)


    async def _parse_total_tournaments_singles(parsed_data):
        fields_to_update = {
            "total_tournaments_singles": parsed_data.get("total_tournaments_singles"),
        }

        if fields_to_update["total_tournaments_singles"]:
            fields_to_update["total_tournaments_singles"] = fields_to_update["total_tournaments_singles"].replace('Career Events:', '').strip()
            fields_to_update["total_tournaments_singles"] = int(fields_to_update["total_tournaments_singles"])

        parsed_data.update(fields_to_update)


    async def _parse_total_money_won(parsed_data):
        fields_to_update = {
            "total_money_won": parsed_data.get("total_money_won"),
        }

        if fields_to_update["total_money_won"]:
            fields_to_update["total_money_won"] = fields_to_update["total_money_won"].replace('Career Earnings: $', '').strip().replace(',', '')
            fields_to_update["total_money_won"] = float(fields_to_update["total_money_won"])

        parsed_data.update(fields_to_update)


    async def _parse_total_wins_singles(parsed_data):
        fields_to_update = {
            "total_wins_singles": parsed_data.get("total_wins_singles"),
        }

        if fields_to_update["total_wins_singles"]:
            fields_to_update["total_wins_singles"] = fields_to_update["total_wins_singles"].replace('Career Wins:', '').strip()
            fields_to_update["total_wins_singles"] = int(fields_to_update["total_wins_singles"])

        parsed_data.update(fields_to_update)


    async def _parse_official_status(parsed_data):
        fields_to_update = {
            "official_status": parsed_data.get("official_status"),
        }

        if fields_to_update["official_status"]:
            fields_to_update["official_status"] = fields_to_update["official_status"].replace('Official Status:', '').strip().split("(")[0].strip()

        parsed_data.update(fields_to_update)


    async def _parse_official_status_expiration_date(parsed_data):
        fields_to_update = {
            "official_status_expiration_date": parsed_data.get("official_status_expiration_date"),
        }

        if fields_to_update["official_status_expiration_date"]:
            matched_date = re.search(r"(\d{2})-(\w{3})-(\d{4})", fields_to_update["official_status_expiration_date"])
            if matched_date:
                matched_date = matched_date.group(0)
                day, month, year = matched_date.split('-')
                month = MONTH_SHORT_TO_NUMBER.get(month)
                formatted_date = f"{year}-{month}-{day}"
                fields_to_update["official_status_expiration_date"] = formatted_date

        parsed_data.update(fields_to_update)


    async def _parse_tournament_years(parsed_data):
        fields_to_update = {
            "tournament_years": parsed_data.get("tournament_years", []),
        }

        parsed_list = []

        if fields_to_update["tournament_years"]:
            for list_item in fields_to_update["tournament_years"]:
                parsed_list.append(int(list_item))

            fields_to_update["tournament_years"] = parsed_list

        parsed_data.update(fields_to_update)


    async def _parse_upcoming_tournaments(parsed_data):
        fields_to_update = {
            "upcoming_tournaments": parsed_data.get("upcoming_tournaments", []),
        }

        parsed_list = []

        if fields_to_update["upcoming_tournaments"]:
            for list_item in fields_to_update["upcoming_tournaments"]:
                parsed_list.append(int(list_item.replace('/tour/event/', '')))

            fields_to_update["upcoming_tournaments"] = parsed_list

        parsed_data.update(fields_to_update)


    async def _parse_add_mongo_parser_datetime(parsed_data):
        fields_to_update = {
            "mongo_data_datetime": str(datetime.datetime.now()),
        }

        parsed_data.update(fields_to_update)



    await asyncio.gather(
        _parse_player_name(raw_data),
        _parse_location_fields(raw_data),
        _parse_classification(raw_data),
        _parse_member_since(raw_data),
        _parse_membership_status(raw_data),
        _parse_membership_expiration_date(raw_data),
        _parse_rating(raw_data),
        _parse_rating_difference(raw_data),
        _parse_rating_updated(raw_data),
        _parse_total_tournaments_singles(raw_data),
        _parse_total_money_won(raw_data),
        _parse_total_wins_singles(raw_data),
        _parse_official_status(raw_data),
        _parse_official_status_expiration_date(raw_data),
        _parse_tournament_years(raw_data),
        _parse_upcoming_tournaments(raw_data),
        _parse_add_mongo_parser_datetime(raw_data),
    )

    print(json.dumps(raw_data, indent=4))
    player = Player(**raw_data)
    player._calculate_analytics()
    print(json.dumps(json.loads(player.to_json()), indent=4))
    import pdb; pdb.set_trace()
    elapsed_time = time.perf_counter() - start_time
    logging.info("player_mongo_field_parser took %s", elapsed_time)


    return raw_data

if __name__ == "__main__":
    local_file = handle_arguments()
    with open(local_file, "r") as data:
        json_data = json.load(data)
        parsed_data = asyncio.run(player_mongo_field_parser(json_data))
        print(json.dumps(parsed_data, indent=4))