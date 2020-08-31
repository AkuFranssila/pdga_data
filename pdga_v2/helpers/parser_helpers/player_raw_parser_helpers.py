import logging
import requests
import datetime
import json
import argparse
import re
import asyncio
import time

from bs4 import BeautifulSoup

logging.getLogger().setLevel("INFO")

def handle_arguments() -> (str):
    parser = argparse.ArgumentParser()
    parser.add_argument('--local_file',
        type=str,
        help="Local file path to test single player parsing without S3",
    )
    args = parser.parse_args()

    return args.local_file


async def player_raw_data_field_parser(raw_data):
    """
    All functions to parse raw html data from PDGA page.
    """

    async def _parse_player_name(soup, parsed_data):
        html_element = soup.find("meta", attrs={"itemprop": "name"})
        parsed_field = None
        if html_element:
            parsed_field = html_element["content"].split(' #')[0].strip()

        parsed_data["full_name"] = parsed_field


    async def _parse_player_location(soup, parsed_data):
        html_element = soup.find(class_="location")
        parsed_field = None
        parsed_city = None
        parsed_state = None
        parsed_country = None
        if html_element and html_element.find("a", href=True):
            parsed_field = html_element.find("a").text
            location_href = html_element.find("a")["href"]

            parsed_city = location_href.split("City=")[1].split("&")[0] if len(location_href.split("City=")) > 1 else None
            parsed_state = location_href.split("StateProv=")[1].split("&")[0] if len(location_href.split("StateProv=")) > 1 else None
            parsed_country = location_href.split("Country=")[1].split("&")[0] if len(location_href.split("Country=")) > 1 else None
        
        parsed_data["full_location"] = parsed_field
        parsed_data["city"] = parsed_city
        parsed_data["state_short"] = parsed_state
        parsed_data["country_short"] = parsed_country


    async def _parse_player_classification(soup, parsed_data):
        html_element = soup.find("li", class_="classification")
        parsed_field = None
        if html_element:
            parsed_field = html_element.text.strip()

        parsed_data["classification"] = parsed_field

    
    async def _parse_player_member_since(soup, parsed_data):
        html_element = soup.find("li", class_="join-date")
        parsed_field = None
        if html_element:
            parsed_field = html_element.text.strip()

        parsed_data["member_since"] = parsed_field

    
    async def _parse_player_membership_status(soup, parsed_data):
        html_element = soup.find("li", class_="membership-status")
        parsed_field = None
        if html_element:
            parsed_field = html_element.text.strip()

        parsed_data["membership_status"] = parsed_field

    
    async def _parse_player_membership_expiration_date(soup, parsed_data):
        html_element = soup.find(class_="membership-expiration-date")
        parsed_field = None
        if html_element:
            parsed_field = html_element.text.strip()

        parsed_data["membership_expiration_date"] = parsed_field


    async def _parse_player_current_rating(soup, parsed_data):
        html_element = soup.find("li", class_="current-rating")
        parsed_field = None
        if html_element:
            parsed_field = html_element.text.strip()

        parsed_data["rating"] = parsed_field


    async def _parse_player_rating_difference(soup, parsed_data):
        html_element = soup.find(class_= re.compile('^(rating-difference).*$'))
        parsed_field = None
        if html_element:
            parsed_field = html_element.text.strip()

        parsed_data["rating_difference"] = parsed_field

    
    async def _parse_player_rating_date(soup, parsed_data):
        html_element = soup.find(class_= "rating-date")
        parsed_field = None
        if html_element:
            parsed_field = html_element.text.strip()

        parsed_data["rating_updated"] = parsed_field


    async def _parse_player_career_events(soup, parsed_data):
        html_element = soup.find(class_= re.compile('^(career-events).*$'))
        parsed_field = None
        if html_element:
            parsed_field = html_element.text.strip()

        parsed_data["total_tournaments_singles"] = parsed_field


    async def _parse_player_career_wins(soup, parsed_data):
        html_element = soup.find(class_= re.compile('^(career-wins).*$'))
        parsed_field = None
        if html_element:
            parsed_field = html_element.text.strip()

        parsed_data["total_wins_singles"] = parsed_field


    async def _parse_player_career_earnings(soup, parsed_data):
        html_element = soup.find(class_= "career-earnings")
        parsed_field = None
        if html_element:
            parsed_field = html_element.text.strip()

        parsed_data["total_money_won"] = parsed_field


    async def _parse_player_official_status(soup, parsed_data):
        html_element = soup.find(class_= "official")
        parsed_field = None
        if html_element:
            parsed_field = html_element.text.strip()

        parsed_data["official_status"] = parsed_field


    async def _parse_player_official_status_expiration_date(soup, parsed_data):
        html_element = soup.find(class_= "official-expiration-date")
        parsed_field = None
        if html_element:
            parsed_field = html_element.text.strip()

        parsed_data["official_status_expiration_date"] = parsed_field


    async def _parse_player_tournament_years(soup, parsed_data):
        parsed_field = []
        html_element = soup.find(class_= "year-link")
        if html_element:
            html_element = html_element.find(class_="tabs secondary")
            if html_element:
                for year in html_element.find_all("li"):
                    parsed_field.append(year.text.strip())

        parsed_data["tournament_years"] = parsed_field


    async def _parse_player_upcoming_events(soup, parsed_data):
        html_element = soup.find(class_= "upcoming-events")
        parsed_field = []
        if html_element:
            for event_href in html_element.find_all("a", href=True):
                parsed_field.append(event_href["href"])

        parsed_data["upcoming_tournaments"] = parsed_field


    async def _parse_player_profile_picture(soup, parsed_data):
        html_element = soup.find("a", attrs={"rel": "gallery-player_photo"})
        parsed_field = None
        if html_element:
            if html_element.find("img", src=True):
                parsed_field = html_element.find("img", src=True)["src"]

        parsed_data["profile_picture_link"] = parsed_field


    start_time = time.perf_counter()

    parsed_data = {}
    parsed_data["pdga_profile_link"] = raw_data.get("url")
    parsed_data["pdga_number"] = raw_data.get("pdga_number")
    parsed_data["pdga_profile_status_code"] = raw_data.get("status_code")

    soup = BeautifulSoup(raw_data["html"], "html.parser")

    await asyncio.gather(
        _parse_player_name(soup, parsed_data),
        _parse_player_location(soup, parsed_data),
        _parse_player_classification(soup, parsed_data),
        _parse_player_member_since(soup, parsed_data),
        _parse_player_membership_status(soup, parsed_data),
        _parse_player_membership_expiration_date(soup, parsed_data),
        _parse_player_current_rating(soup, parsed_data),
        _parse_player_rating_difference(soup, parsed_data),
        _parse_player_rating_date(soup, parsed_data),
        _parse_player_career_events(soup, parsed_data),
        _parse_player_career_earnings(soup, parsed_data),
        _parse_player_official_status(soup, parsed_data),
        _parse_player_official_status_expiration_date(soup, parsed_data),
        _parse_player_tournament_years(soup, parsed_data),
        _parse_player_upcoming_events(soup, parsed_data),
        _parse_player_profile_picture(soup, parsed_data),
        _parse_player_career_wins(soup, parsed_data),
    )

    elapsed_time = time.perf_counter() - start_time
    logging.info("player_raw_data_field_parser took %s", elapsed_time)


    return parsed_data

if __name__ == "__main__":
    local_file = handle_arguments()
    with open(local_file, "r") as data:
        json_data = json.load(data)
        parsed_data = asyncio.run(player_raw_data_field_parser(json_data))
        print(json.dumps(parsed_data, indent=4))