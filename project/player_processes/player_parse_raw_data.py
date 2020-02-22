# coding=utf-8
from bs4 import BeautifulSoup
import requests
import json
import logging
from datetime import date
from project.helpers.helpers_crawler import FindNewestMemberId
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


def PlayerParseRawData(pdga_number, raw_data, file_location):
    soup = BeautifulSoup(raw_data, "html.parser")
    logging.info('----------------------------------------')
    logging.info("Parsing raw data for player %s" % str(pdga_number))
    i = pdga_number
    player_data = {}
    player_pdga_page_link = 'https://www.pdga.com/player/' + str(pdga_number)
    try:
        player_name = soup.find('h1').text.split(' #')[0].strip()
        #ID is actice = 1
        player_id_active = True
    except:
        logging.error('Player ID %s in URL https://www.pdga.com/player/%s is not working', str(pdga_number), str(pdga_number))
        player_name = None
        player_id_active = False

    try:
        player_location_raw = soup.find(class_="location").text.replace('Location:', '').strip()
    except:
        logging.error('Unable to find location in https://www.pdga.com/player/%s', str(i))
        player_location_raw = None

    try:
        player_classification = soup.find(class_="classification").text.replace('Classification: ', '').strip()
    except:
        logging.error('Unable to find classification in https://www.pdga.com/player/%s', str(i))
        player_classification = None

    try:
        player_member_since = soup.find(class_="join-date").text.replace('Member Since:', '').strip()
        player_member_since = int(player_member_since)
    except:
        logging.error('Unable to find member since info in https://www.pdga.com/player/%s', str(i))
        player_member_since = "Unknown"

    try:
        player_membership_status = soup.find(class_="membership-status").find('a').text.strip()
    except:
        logging.error('Unable to find membership status in https://www.pdga.com/player/%s', str(i))
        player_membership_status = None

    try:
        player_membership_expiration_date = soup.find(class_="membership-expiration-date").text.replace('(as of ', '').replace(')','').replace('(until', '').strip()
    except:
        logging.error('Unable to find membership expiration date in https://www.pdga.com/player/%s', str(i))
        player_membership_expiration_date = None

    try:
        player_current_rating = soup.find(class_="current-rating").text.replace('Current Rating:', '').strip().split(' ')[0]
        player_current_rating = int(player_current_rating)
    except:
        logging.error('Unable to find rating in https://www.pdga.com/player/%s', str(i))
        player_current_rating = None

    try:
        try:
            player_rating_difference = soup.find(class_="rating-difference gain").text
        except:
            player_rating_difference = soup.find(class_="rating-difference loss").text
        if "+" in player_rating_difference:
            player_rating_difference = int(player_rating_difference.replace('+', ''))
        else:
            player_rating_difference = int(player_rating_difference.replace('-', '')) * -1
    except:
        logging.error('Unable to find rating difference in https://www.pdga.com/player/%s', str(i))
        player_rating_difference = None

    try:
        player_rating_updated = soup.find(class_="rating-date").text.replace('(as of ', '').replace(')','').strip()
    except:
        logging.error('Unable to find rating update date in https://www.pdga.com/player/%s', str(i))
        player_rating_updated = None

    try:
        player_events_played = soup.find(class_="career-events disclaimer").text.replace('Career Events:', '').strip()
        player_events_played = int(player_events_played)
    except:
        logging.error('Unable to find events played in https://www.pdga.com/player/%s', str(i))
        player_events_played = 0

    try:
        player_career_wins = soup.find(class_="career-wins disclaimer").find('a').text.strip()
        player_career_wins = int(player_career_wins)
    except:
        logging.error('Unable to find career wins in https://www.pdga.com/player/%s', str(i))
        player_career_wins = 0

    try:
        player_career_earnings = soup.find(class_="career-earnings").text.replace('Career Earnings:', '').strip().replace('$', '').replace(',', '')
        player_career_earnings = float(player_career_earnings)
    except:
        logging.error('Unable to find career earnings in https://www.pdga.com/player/%s', str(i))
        player_career_earnings = float(0)

    try:
        player_certified_status = soup.find(class_="official").find('a').text.strip()
    except:
        logging.error('Unable to certified official status in https://www.pdga.com/player/%s', str(i))
        player_certified_status = None

    try:
        player_certified_status_expiration = soup.find(class_="official").find(class_="official-expiration-date").text.replace('(until ', '').replace(')', '').replace('(as of ', '')
    except:
        logging.error('Unable to find certified official expiration date in https://www.pdga.com/player/%s', str(i))
        player_certified_status_expiration = None

    try:
        tournament_years = soup.find(class_="year-link").find(class_="tabs secondary").find_all('li')
        years = []
        for year in tournament_years:
            year = year.find('a').text.strip()
            years.append(int(year))
        player_individual_tournament_years = years
    except:
        logging.error('Unable to find individual tournament years in https://www.pdga.com/player/%s', str(i))
        player_individual_tournament_years = []

    player_data['player_name'] = player_name
    player_data['player_pdga_number'] = int(pdga_number)
    player_data['player_id'] = player_id_active
    player_data['player_location_raw'] = player_location_raw
    player_data['player_classification'] = player_classification
    player_data['player_member_since'] = player_member_since
    player_data['player_membership_status'] = player_membership_status
    player_data['player_membership_expiration_date'] = player_membership_expiration_date
    player_data['player_current_rating'] = player_current_rating
    player_data['player_rating_difference'] = player_rating_difference
    player_data['player_rating_updated'] = player_rating_updated
    player_data['player_events_played'] = player_events_played
    player_data['player_career_wins'] = player_career_wins
    player_data['player_certified_status'] = player_certified_status
    player_data['player_certified_status_expiration'] = player_certified_status_expiration
    player_data['player_career_earnings'] = player_career_earnings
    player_data['player_individual_tournament_years'] = player_individual_tournament_years
    player_data['player_crawl_date'] = str(date.today())

    return player_data


#print (json.dumps(CrawlPlayers(1,20,False), indent=4))
