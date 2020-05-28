# coding=utf-8
import os
import json
import logging
import datetime
import requests
import pycountry
import time
import copy
from project.models.schemas import Player, Tournament
from project.helpers.helper_data import ACCEPTED_STATUSES, US_STATES, MONTH_DICT, HISTORY_FIELDS, US_STATES_LIST, HISTORY_FIELDS_TOURNAMENT
from mongoengine import *
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

def ParsePlayerFullName(data):
    first_name = None
    middle_name = None
    last_name = None
    full_name = data.get('player_name')

    if full_name and full_name != "Page not found":
        full_name = full_name.split(' ')
        if len(full_name) > 2:
            first_name = full_name[0] + ' ' + full_name[1]
            last_name = full_name[-1]
        else:
            first_name = full_name[0]
            last_name = full_name[-1]

    return first_name, middle_name, last_name


def CleanFullLocation(data, type=None):
    if type == "player":
        location_full = data.get("player_location_raw")
    elif type == "tournament":
        location_full = data.get("event_location")
    else:
        location_full = data
    if location_full:
        location_full = location_full.replace('Location:', '').replace('?', '').strip()

    return location_full


def ParseFullLocation(data, allow_google_api=True, recheck=False, type=None):
    """
    Parse full location
    """
    if not recheck and type == "player":
        full_location = data.get("player_location_raw")
    elif not recheck and type == "tournament":
        full_location = data.get("event_location")
    else:
        full_location = data

    full_location = CleanFullLocation(full_location)

    city = None
    state = None
    country = None

    def GoogleMapsAPILocationCheck(data, allow_google_api):
        new_location = None
        if allow_google_api:
            google_geolocation_query = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=' + data + '&key=' + os.environ['google_geolocation_apikey'])
            json_data = json.loads(google_geolocation_query.text)
            #logging.info(json_data)
            new_location = json_data['results'][0]['formatted_address'].lower()
            logging.info(new_location)

        return new_location


    def TurnLocationToList(full_location):
        full_location_list = []
        for field in full_location.split(','):
            field = field.strip().lower()
            if field == "usa":
                field = "united states"

            full_location_list.append(field)

        return full_location_list

    if full_location:
        full_location_list = TurnLocationToList(full_location)

        if "united states" in full_location_list:
            country = "united states"

            if len(full_location_list) == 3:
                city = full_location_list[0]
                state = US_STATES.get(full_location_list[1], full_location_list[1])
            elif len(full_location_list) == 2:
                if full_location_list[0] in map(str.lower, US_STATES_LIST):
                    state = full_location_list[0]
                elif len(full_location_list[0]) == 2:
                    state = US_STATES.get(full_location_list[0])
                else:
                    city = full_location_list[0]

            for field in full_location_list:
                if not state:
                    state = US_STATES.get(field)
                if not state and field != "united states":
                    city = field
        else:

            if len(full_location_list) >= 3:
                city = full_location_list[0]
                state = full_location_list[1]
                country = full_location_list[2]
            elif len(full_location_list) == 2:

                if len(full_location_list[1]) == 2:
                    state = US_STATES.get(full_location_list[1])
                    if state:
                        country = "united states"
                        city = full_location_list[0]
                else:
                    city = full_location_list[0]
                    country = full_location_list[1]
            elif len(full_location_list) == 1:

                if len(full_location_list[0]) == 2:
                    country = "united states"
                    state = US_STATES.get(full_location_list[0])
                elif pycountry.countries.get(name=full_location_list[0].title()):
                    country = full_location_list[0]
                elif len(full_location_list[0]) > 2:
                    new_location = GoogleMapsAPILocationCheck(full_location_list[0], allow_google_api)
                    if full_location_list[0] in new_location:
                        city, state, country = ParseFullLocation(new_location, allow_google_api=False, recheck=True)


    return city, state, country


def ParseDate(date):
    """
    Accepts date in the format posted in PDGA. Returns the date in year-month-day format.
    """
    if date:
        print(date)
        day,month,year = date.split(' ')[0].strip().split('-')
        date = year + '-' + MONTH_DICT[month] + '-' + day
    return date


def CleanPlayerFullName(data):
    """
    Remove trailing white space. Add more normalization or validation to full name if needed in the future.
    """
    full_name = data.get('player_name')
    if full_name:
        full_name = full_name.strip()

    return full_name


def PlayerExists(pdga_number):
    logging.info(f'Checking if player exists {str(pdga_number)}')
    try:
        player = Player.objects.get(pdga_number=pdga_number)
        player_exists = True
    except: #schemas.DoesNotExist
        player = Player()
        player_exists = False

    return player, player_exists


def ParseIdStatus(data):
    """
    If player name can be found then the player ID is in use
    """
    name = data.get('player_name')
    if name:
        return True
    else:
        False


def CheckAndNormalizeMembershipStatus(data):
    membership_status = data.get('player_membership_status')
    if membership_status:
        membership_status = str(membership_status).lower().strip()

    return membership_status


def CheckMembership(data):
    """
    Check if membership is active. Return true or false depending on the membership status
    """
    membership_active = False
    membership_status = data.get('player_membership_status')
    if membership_status:
        membership_status = str(membership_status).lower().strip()
        if membership_status in ACCEPTED_STATUSES:
            membership_active = True

    return membership_active


def ParseClassification(data):
    classification = data.get('player_classification')
    if classification:
        classification = str(classification).lower().strip()

    return classification


def ParseMemberSince(data):
    member_since = data.get('player_member_since')

    if member_since == "Unknown":
        member_since = None 

    return member_since


def GeneratePDGAplayerlink(data):
    pdga_id = data.get('player_pdga_number')
    pdga_link = f"https://www.pdga.com/player/{pdga_id}"

    return pdga_link


def CheckIfValueNone(value):
    if value is not None:
        return value
    else:
        return None


def CheckIfNewPlayer(value, old_data):
    #Checks if player is new or old. If player is old returns current data in db. Used for fields that only need to be updated once.
    if old_data is not None:
        return old_data
    else:
        return value


def CheckifPlayerExists(pdga_number):
    player = Player.objects(pdga_number=pdga_number).first()

    if player:
        return player
    else:
        return None


def ParseIndividualTournamentYears(list_of_years, membership_status, old_data):
    if CheckMembershipStatus(membership_status)[1]:
        return list_of_years
    elif old_data is None:
        return list_of_years


def ParseCertifiedStatus(data):
    certified_status = data.get('player_certified_status')
    status = False
    if certified_status == "Certified":
        status = True

    return status
    

def FindPlayedEventIds(pdga_number):
    played_events = Tournament.objects.filter(player__pdga_id=pdga_number).only("tournament_id")
    return played_events


def CompareDicts(old_data, new_data):
    old_data = Player.objects(pdga_number=old_data).first()
    if old_data is not None:
        old_data = old_data.to_json()
    if new_data is not None and old_data is not None:
        new_data = new_data.to_json()
        old_data = json.loads(old_data)
        new_data = json.loads(new_data)
        old_data_keys = set(old_data.keys())
        new_data_keys = set(new_data.keys())
        intersect_keys = old_data_keys.intersection(new_data_keys)
        added = old_data_keys - new_data_keys
        removed = new_data_keys - old_data_keys
        modified = {o : (old_data[o], new_data[o]) for o in intersect_keys if old_data[o] != new_data[o]}
        same = set(o for o in intersect_keys if old_data[o] == new_data[o])
        return added, removed, modified, same, None
    else:
        all_new = new_data.to_json()
        all_new = json.loads(all_new)
        return None, None, None, None, all_new


def CreateFieldsUpdated(added_data, removed_data, modified_data, date, all_new):
    parsed_added = []
    parsed_removed = []
    parsed_modified = {}

    if added_data and removed_data and modified_data is not None:
        if len(added_data) != 0:
            parsed_added = list(added_data)


        if len(removed_data) != 0:
            parsed_removed = list(removed_data)

        if len(modified_data) != 0:
            for k, v in modified_data.items():
                try:
                    v[0]['date'] = v[0].pop('$date')
                    v[1]['date'] = v[1].pop('$date')
                except:
                    None
                parsed_modified[k] = {'old_value': v[0], 'new_value': v[1]}

        updated_data = {
            "new_data": parsed_added,
            "modified_data": parsed_modified,
            "removed_data": parsed_removed,
            "updated_date": date
        }

        return updated_data
    elif all_new is not None:
        for k, v in all_new.items():
            parsed_added.append(k.replace('$', ''))

        updated_data = {
            "new_data": parsed_added,
            "modified_data": parsed_modified,
            "removed_data": parsed_removed,
            "updated_date": date
        }

        return updated_data
    else:
        updated_data = {
            "new_data": parsed_added,
            "modified_data": parsed_modified,
            "removed_data": parsed_removed,
            "updated_date": date
        }

        return updated_data


def ParseTournamentName(name):
    if name is not None:
        return name
    else:
        return "Unnamed tournament"


def TournamentExists(tournament_id):
    tournament = Tournament.objects(tournament_id=tournament_id).first()

    if tournament:
        return tournament
    else:
        return None


def ParseTournamentDates(data):
    #Date: 03-Nov-2019
    #Date: 02-Nov to 03-Nov-2019
    #Date: 17-May to 19-May-2019
    event_dates = data.get("event_date")
    event_dates = event_dates.replace('Date: ', '')
    if " to " in event_dates:
        start = event_dates.split(' to ')[0]
        end = event_dates.split(' to ')[1]
        end = ParseDate(end)
        start= end.split('-')[0] + '-' + MONTH_DICT[start.split('-')[1]] + '-' + start.split('-')[0]
    else:
        date = ParseDate(event_dates)
        start = date
        end = date

    if start == end:
        length = 1
    else:
        d1 = datetime.date(int(start.split('-')[0]), int(start.split('-')[1]), int(start.split('-')[2]))
        d2 = datetime.date(int(end.split('-')[0]), int(end.split('-')[1]), int(end.split('-')[2]))
        length = d2 - d1
        length = length.days + 1


    return start, end, length


def ParseTournamentDirectorName(data, type):
    if type == "td":
        td = data.get("event_tournament_director_name")
    elif type == "td_assistant":
        td = data.get("event_assistant_dt_name")

    parsed_td = None 

    if td:
        parsed_td = td.replace('Tournament Director:', '').replace('Asst. Tournament Director:', '').replace('Asst. ', '').strip()

    return parsed_td


def ParseTournamentDirectorID(data, type):
    if type == "td":
        td = data.get("event_tournament_director_id")
    elif type == "td_assistant":
        td = data.get("event_assistant_dt_id")

    parsed_td = None 

    if td:
        parsed_td = td.replace('/general-contact?pdganum=', '').split('&token')[0].strip()
        parsed_td = int(parsed_td)

    return parsed_td


def ParseTournamentWebsite(data):
    website = data.get("event_website")

    if website and website != "n/a":
        #why .split('\m')[0] in the code? There is a random case that was most easy to solve adding the split
        website = website.replace('Website: ', '').replace('[email protected]', '').strip().replace(',', '.').replace('\\', '/')
        if "https://" or "http://" not in website:
            website = "https://" + website
            website = website.replace('https:///', 'https://').replace('ttp://', '').replace(' ', '')
    else:
        website = None
    if website:
        if website == "https://n/a" or website == "https://[email protected]" or "." not in website:
            website = None

    return website


def ParseTournamentProPurse(data):
    pro_purse = data.get("event_pro_purse")

    if pro_purse:
        pro_purse = pro_purse.replace('$', '').strip().replace(',', '')
        try:
            pro_purse = float(pro_purse)
        except ValueError:
            pro_purse = None

    return pro_purse

def ParseDivisionFullName(name):
    if name is not None:
        name = name.split('  ')[0]
    return name


def ParseDivisionTotalPlayers(division_players):
    if division_players is not None:
        division_players = division_players.strip().replace('(', '').replace(')', '')
        division_players = int(division_players)
    return division_players


def ParseCourseDetails(course, pdga_page):
    #"course_details": "\n\nJoe Wheeler State Park - Default Layout; 18 holes; Par 55\n\n"
    #"course_pdga_link": "/node/223286"
    #"course_details": "\n\nDacey Field Disc Golf - Blues - Longs; 18 holes; Par 62; 6,185 ft.\n\n"
    #"course_details": "\n\nMatt Keatts Memorial at Forest Hills 2019; 20 holes; Par 66; 7,390 ft.\n\
    # - B&amp;C; 18 holes; Par 58; 5,252 ft.

    logging.info(repr(course))

    if pdga_page is not None:
        pdga_page = "https://www.pdga.com" + pdga_page

    if course is not None:
        course = course.replace('\n', '').replace(u'&amp;', u'&')
        if len(course.split(' - ')) >= 2:
            name = course.split(' - ', 1)[0]
            course = course.split(' - ', 1)[1].split(';')
            if len(course) == 4:
                layout, holes, par, length = course
            elif len(course) == 3:
                layout, holes, par = course
                if "par" in holes.lower():
                    holes, par, length = course
                    holes = holes.split(' ')[1]
                    layout = None
                else:
                    length = None
            else:
                layout, holes, par, length = None, None, None, None
        elif len(course.split(';')) == 4:
            name, holes, par, length = course.split(';')
            try:
                int(holes.strip().replace(' holes', ''))
                layout = None
            except:
                layout1, layout2, holes, par = course.split(';')
                name = "Unnamed course"
                layout = layout1 + layout2
        elif len(course.split(';')) == 3:
            name, holes, par = course.split(';')
            length = None
            layout = None
        else:
            name, holes, par, length, layout = None, None, None, None, None

    if name is not None:
        name = name.strip()
    if holes is not None:
        holes = holes.strip().replace(' holes', '')
        try:
            holes = int(holes)
        except:
            holes = None
    if par is not None:
        par = par.strip().replace('Par ', '')
        par = int(par)
    if length is not None:
        if "ft." in length:
            length = length.strip().replace(' ft.', '').replace(',', '').replace(' ', '')
            length = int(length)
            length_feet = length
            length_meters = length * 0.3048
        elif " m" in length:
            length = length.strip().replace(' m', '').replace(',', '').replace(' ', '')
            length = int(length)
            length_meters = length
            length_feet = length * 3.2808399
        else:
            length_meters, length_feet = None, None
    else:
        length_meters, length_feet = None, None

    return name, layout, holes, par, pdga_page, length_meters, length_feet


def ParsePDGAnumber(type, data):
    pdga1 = None
    pdga2 = None
    if type == "singles":
        if data['player_pdga_number'] is not None:
            pdga1 = int(data['player_pdga_number'].strip())
    elif type == "doubles":
        if data['player_1_pdga_number'] is not None:
            pdga1 = data['player_1_pdga_number']
        if data['player_2_pdga_number'] is not None:
            pdga2 = data['player_2_pdga_number']
    else:
        if data['team_pdga_number'] is not None:
            pdga1 = int(data['team_pdga_number'].strip())

    return pdga1, pdga2


def ParseTournamentPlayerName(type, data):
    if type == "singles":
        name1 = data['player_full_name']
        name2 = None
    elif type == "doubles":
        name1 = data['player_1_full_name']
        name2 = data['player_2_full_name']
    else:
        if data['team_full_name'] is not None:
            name1 = data['team_full_name'].strip()
        else:
            name1 = None
        if data['team_player_name'] is not None:
            name2 = data['team_player_name'].strip()
        else:
            name2 = None

    return name1, name2


def ParseTournamentPDGApage(type, data):
    if type == "singles":
        page1 = data["player_pdga_link"]
        page2 = None
    elif type == "doubles":
        page1 = data["player_1_pdga_link"]
        page2 = data["player_2_pdga_link"]
    else:
        page1 = data["team_pdga_link"]
        page2 = None

    return page1, page2


def ParsePropagator(type, data):
    if type == "singles":
        var1 = data["player_propagator"]
        var2 = False
    elif type == "doubles":
        var1 = data["player_1_propagator"]
        var2 = data["player_2_propagator"]
    else:
        var1 = data["team_propagator"]
        var2 = False

    return var1, var2


def ParseRatingTournament(type, data):
    if type == "singles":
        var1 = data["player_rating_during_tournament"]
        var2 = None
    elif type == "doubles":
        #import pdb; pdb.set_trace()
        var1 = data['player_1_rating_during_tournament']
        var2 = data['player_2_rating_during_tournament']
    else:
        var1 = data["team_rating_during_tournament"]
        var2 = None

    if var1 == "":
        var1 = None
    if var2 == "":
        var2 = None
    return var1, var2


def ParseTournamentPlacement(var):
    if var is not None:
        var = int(var)

    return var


def ParseTournamentWinnings(var):
    if var is not None and len(var.strip()) > 0:
        var = var.replace(',', '').replace(' ', '').replace('$', '').strip()
        try:
            var = float(var)
        except ValueError:
            var = 0
    else:
        var = float(0)

    return var


def ParseTournamentTotalThrows(var):
    dnf = False
    dns = False
    if var is not None and len(var.strip()) > 0:
        var = var.replace(',', '').replace(' ', '').replace('$', '').strip()
        if var.lower() == "dnf":
            dnf = True
            var = None
        elif var.lower() == "dns":
            dns = True
            var = None
        else:
            var = int(var)
    else:
        var = int(0)

    return var, dnf, dns


def ParseTournamentPar(var, dnf, dns):
    if var is not None:
        var = var.replace(',', '').strip()
        if var == "E":
            var = 0
        elif var == "DNF/DNS":
            dnf = True
            var = None
        else:
            var = int(var)

    return var, dnf, dns


def ParsePlayerRoundThrows(var, dnf):
    if dnf is None:
        dnf = False
    if var is not None and len(var) > 1:
        if var in ["999", "888"]:
            dnf = True
            var = None
        else:
            try:
                var = int(var)
            except:
                var = None
    else:
        var = None

    return var, dnf


def ParsePlayerRoundRating(var):
    if var is not None and len(var) > 0:
        var = int(var)
    else:
        var = None

    return var


def CalculateAvgFromRounds(data, rounds_with_results):
    avg_from_rounds = None
    if data and rounds_with_results:
        try:
            avg_from_rounds = data / rounds_with_results
        except:
            logging.info("Average from rounds could not be calculated. Data: %s, Rounds: %s" % (str(data), str(rounds_with_results)))

    return avg_from_rounds



def CalculateAvgRoundRating(rounds):
    avg_round_rating = None

    total_round_rating = 0
    rounds_with_rating = 0

    for round in rounds:
        if round.round_rating:
            total_round_rating += round.round_rating
            rounds_with_rating += 1

    if total_round_rating > 0 and rounds_with_rating > 0:
        avg_round_rating = total_round_rating / rounds_with_rating

    return avg_round_rating


def ParseTournamentPoints(points):
    if points is not None:
        try:
            points = float(points.strip())
        except:
            points = None

    return points


def ParseTournamentTeamName(team_name):
    if team_name is not None:
        team_name = team_name.strip()
    else:
        team_name = None

    return team_name


def CheckLowestRating(new_player, old_player):
    old_lowest_rating = old_player.lowest_rating
    new_lowest_rating = new_player.lowest_rating

    lowest_rating = new_lowest_rating

    if old_lowest_rating and new_lowest_rating:

        if new_lowest_rating < old_lowest_rating:
            lowest_rating = new_lowest_rating 
        else:
            lowest_rating = old_lowest_rating 
    elif old_lowest_rating:
        lowest_rating = old_lowest_rating

    return lowest_rating


def CheckHighestRating(new_player, old_player):
    old_highest_rating = old_player.highest_rating
    new_highest_rating = new_player.highest_rating

    highest_rating = new_highest_rating

    if old_highest_rating and new_highest_rating:

        if new_highest_rating > old_highest_rating:
            highest_rating = new_highest_rating 
        else:
            highest_rating = old_highest_rating 
    elif old_highest_rating:
        highest_rating = old_highest_rating

    return highest_rating


def CheckCurrentRating(new_player, old_player):
    new_rating = new_player.current_rating
    old_rating = old_player.current_rating

    current_rating = old_rating

    if new_rating:
        current_rating = new_rating 

    return current_rating


def CheckRatingDifference(new_player, old_player):
    old_difference = old_player.rating_difference
    new_difference = new_player.rating_difference

    current_difference = old_difference

    if new_difference:
        current_difference = new_difference 

    return current_difference


def CheckLatestRatingUpdate(new_player, old_player):
    old_update = old_player.latest_rating_update
    new_update = new_player.latest_rating_update

    current_update = old_update

    if new_update:
        current_update = new_update 

    return current_update


def CheckCertifiedStatus(new_player, old_player):

    new_expiration_date = new_player.certified_status_expiration_date
    old_expiration_date = old_player.certified_status_expiration_date
    old_cert_status = old_player.certified_status
    new_cert_status = new_player.certified_status

    current_cert_status = None

    if new_cert_status:
        current_cert_status = new_cert_status 
    elif not new_cert_status and old_expiration_date:
        if old_expiration_date > datetime.datetime.today():
            current_cert_status = True

    return current_cert_status


def CheckCertifiedStatusExpirationDate(new_player, old_player):
    new_expiration_date = new_player.certified_status_expiration_date
    old_expiration_date = old_player.certified_status_expiration_date
    current_cert_date = None

    if new_expiration_date:
        current_cert_date = new_expiration_date
    elif not new_expiration_date and old_expiration_date:
        if old_expiration_date > datetime.datetime.today():
            current_cert_date = old_expiration_date


    return current_cert_date


def CheckFieldsUpdated(new_player, old_player, reset_history=False):

    if old_player:
        updated_fields = old_player.fields_updated
        changed_data = {}
        new_data = json.loads(new_player.to_json())
        old_data = json.loads(old_player.to_json())

        for history_field in HISTORY_FIELDS:
            history_old = old_data.get(history_field)
            history_new = new_data.get(history_field)
            try:
                if "$date" in history_old:
                    history_old = history_old.get("$date")
                    history_new = history_new.get("$date")
                    history_new = datetime.datetime.fromtimestamp(history_new/1000)
                    history_old = datetime.datetime.fromtimestamp(history_old/1000)
            except TypeError:
                continue
            if history_old != history_new:
                changed_data_details = {}
                changed_data_details["new"] = history_new
                changed_data_details["old"] = history_old
                changed_data[history_field] = changed_data_details

                updated_fields.append(changed_data.copy())

    else:
        updated_fields = []

    if reset_history:
        updated_fields = []

    return updated_fields

def parse_tournament_id(data):
    event_link = data.get("event_link")

    tournament_id = event_link.strip().split('/')[-1]
    tournament_id = int(tournament_id)

    return tournament_id


def parse_tournament_total_players(data):
    total_players = data.get("event_total_players")

    if total_players:
        total_players = int(total_players)

    return total_players


def check_tournament_director(tournament, old_tournament):
    old_td = old_tournament.tournament_director
    td = tournament.tournament_director

    if not td:
        td = old_td 

    return td


def check_tournament_director_id(tournament, old_tournament):
    old_td = old_tournament.tournament_director_id
    td = tournament.tournament_director_id

    if not td:
        td = old_td 

    return td


def check_assistant_tournament_director(tournament, old_tournament):
    old_td = old_tournament.assistant_director
    td = tournament.assistant_director

    if not td:
        td = old_td 

    return td


def check_assistant_tournament_director_id(tournament, old_tournament):
    old_td = old_tournament.assistant_director_id
    td = tournament.assistant_director_id

    if not td:
        td = old_td 

    return td


def CheckFieldsUpdatedTournament(tournament, old_tournament, reset_history=False):

    if old_tournament:
        updated_fields = old_tournament.fields_updated
        changed_data = {}
        new_data = json.loads(tournament.to_json())
        old_data = json.loads(old_tournament.to_json())

        for history_field in HISTORY_FIELDS:
            history_old = old_data.get(history_field)
            history_new = new_data.get(history_field)
            try:
                if "$date" in history_old:
                    history_old = history_old.get("$date")
                    history_new = history_new.get("$date")
                    history_new = datetime.datetime.fromtimestamp(history_new/1000)
                    history_old = datetime.datetime.fromtimestamp(history_old/1000)
            except TypeError:
                continue
            if history_old != history_new:
                changed_data_details = {}
                changed_data_details["new"] = history_new
                changed_data_details["old"] = history_old
                changed_data[history_field] = changed_data_details

                updated_fields.append(changed_data.copy())

    else:
        updated_fields = []

    if reset_history:
        updated_fields = []

    return updated_fields

def ParseTournamentRoundsWithResults(player):
    rounds = player.get("player_rounds")

    rounds_with_results = 0

    if rounds:
        for round in rounds:
            if round.get("round_throws"):
                rounds_with_results += 1


    return rounds_with_results


def PlayerRoundAvgThrowLength(all_rounds, throws, round_number, type):
    round_avg_throw_length = None

    if all_rounds and throws and round_number:
        if type == "meters":
            round_index = round_number - 1
            round_info = all_rounds[round_index]
            course_length = round_info.course_length_meters
            if course_length:
                round_avg_throw_length = course_length / throws
        elif type == "feet":
            round_index = round_number - 1
            round_info = all_rounds[round_index]
            course_length = round_info.course_length_feet
            if course_length:
                round_avg_throw_length = course_length / throws


    return round_avg_throw_length


def PlayerRoundPar(all_rounds, throws, round_number):
    round_par = None
    if all_rounds and throws and round_number:
        round_index = round_number - 1
        round_info = all_rounds[round_index]
        course_par = round_info.course_par
        if course_par:
            round_par = throws - course_par


    return round_par


def PlayerRoundAvgThrowsPerHole(all_rounds, throws, round_number):
    avg_throws_per_hole = None
    if all_rounds and throws and round_number:
        round_index = round_number - 1
        round_info = all_rounds[round_index]
        course_holes = round_info.course_holes
        if course_holes:
            avg_throws_per_hole = throws / course_holes


    return avg_throws_per_hole


def CalculatePlayerTournamentAvgThrowLenght(rounds, type):
    total_avg_length = 0
    rounds_with_avg_length = 0
    total_tournament_avg_length = None

    if rounds:
        for round in rounds:
            type_dict = {
                "meters": round.avg_throw_length_meters,
                "feet": round.avg_throw_length_feet
            }
            avg_length = type_dict.get(type)
            if avg_length:
                total_avg_length += avg_length
                rounds_with_avg_length += 1

    if total_avg_length > 0 and rounds_with_avg_length > 0:
        total_tournament_avg_length = total_avg_length / rounds_with_avg_length

    return total_tournament_avg_length


def CalculateAverageFromTwoFields(first_field, second_field):

    avg_to_return = None

    if first_field and second_field:
        if first_field > 0 and second_field > 0:
            avg_to_return = first_field / second_field
        elif first_field == 0 and second_field > 0:
            avg_to_return = 0

    return avg_to_return


def CalculateDifferenceFromTwoFields(first_field, second_field):

    difference_to_return = None

    if first_field and second_field:
        difference_to_return = first_field - second_field

    return difference_to_return

            
def CalculateTotalHolesPlayed(player_rounds, course_rounds):

    total_holes_played = 0

    played_rounds_index = []

    if player_rounds and course_rounds:
        for p_round in player_rounds:
            if p_round.round_throws:
                played_rounds_index.append(p_round.round_number - 1)
              
        for round_index in played_rounds_index:
              c_round = course_rounds[round_index]

              if c_round.course_holes:
                  total_holes_played += c_round.course_holes

    if total_holes_played == 0:
        total_holes_played = None

    return total_holes_played


def FillTotalThrowsIfEmpty(total_throws, division_rounds):

    if not total_throws:
        total_throws = 0
        for round in division_rounds:
            if round.round_throws:
                total_throws += round.round_throws

        if total_throws == 0:
            total_throws = None

    return total_throws


def ReturnValueOrZero(value):
    value_to_return = 0

    if value:
        value_to_return = value

    return value_to_return


def ReturnRatingDuringTournamentAverage(rating_during_tournament, type="singles"):
    rating_to_return = None

    if type == "doubles":
        rating_for_doubles = 0
        for r in rating_during_tournament:
            if r:
                rating_for_doubles += r
        
        if rating_for_doubles > 0:
            rating_to_return = rating_for_doubles / 2
    else:
        rating_to_return = rating_during_tournament[0]

    return rating_to_return


def CheckHighestLowestRoundRating(rating, type, dict):
    if rating:
        if type == "highest":
            if dict["players_highest_round_rating"] < rating:
                dict["players_highest_round_rating"] = rating
        else:
            if dict["players_lowest_round_rating"] > rating or dict["players_lowest_round_rating"] == 0:
                dict["players_lowest_round_rating"] = rating


def CheckPlayerRoundDetails(division):

    def CalculatePlayerPlacementOnRound(division_players):
        rounds_and_throws = {}
        rounds_and_placement = {}
        
        for player in division_players:
            if player.rounds:
                for p_round in player.rounds:
                    if p_round.round_throws:
                        if rounds_and_throws.get(p_round.round_number):
                            rounds_and_throws[p_round.round_number].append(p_round.round_throws)
                        else:
                            rounds_and_throws[p_round.round_number] = [p_round.round_throws]

        for k, v in rounds_and_throws.items():
            v.sort()

            placement_dict = {}
            placement_number = 1
            for throws in v:
                if not placement_dict.get(throws):
                    placement_dict[throws] = placement_number
                    placement_number += 1

            rounds_and_placement[k] = placement_dict

        for player in division_players:
            if player.rounds:
                for p_round in player.rounds:
                    p_round.round_placement = None
                    if p_round.round_throws:
                        p_round.round_placement = rounds_and_placement[p_round.round_number][p_round.round_throws]

    def CalculateDifferencesToPlayerAverages(division_players):
        """
        Update fields on player rounds with differences to players whole tournament averages.
        """
        for player in division_players:

            for round in player.rounds:
                round.throw_difference_to_player_avg = CalculateDifferenceFromTwoFields(round.round_throws, player.avg_throws_per_round)
                round.throw_length_difference_to_player_avg_meters = CalculateDifferenceFromTwoFields(round.avg_throw_length_meters, player.avg_throw_length_meters)
                round.throw_length_difference_to_player_avg_feet = CalculateDifferenceFromTwoFields(round.avg_throw_length_feet, player.avg_throw_length_feet)
                round.par_difference_to_player_avg = CalculateDifferenceFromTwoFields(round.round_par, player.avg_par_per_round)
                round.round_rating_difference_to_player_avg = CalculateDifferenceFromTwoFields(round.round_rating, player.avg_round_rating)
                round.round_rating_difference_to_rating_during_tournament = CalculateDifferenceFromTwoFields(round.round_rating, ReturnRatingDuringTournamentAverage(player.rating_during_tournament, type=division.type))
                #import pdb; pdb.set_trace()



    
    def CalculateDifferencesToRoundAverages(division_players, division_rounds):
        for player in division_players:
            for round, course_round in zip(player.rounds, division_rounds):
                round.throw_difference_to_round_avg = CalculateDifferenceFromTwoFields(round.round_throws, course_round.players_avg_throws)
                round.throw_length_difference_to_round_avg_meters = CalculateDifferenceFromTwoFields(round.avg_throw_length_meters, course_round.players_avg_throw_length_meters)
                round.throw_length_difference_to_round_avg_feet = CalculateDifferenceFromTwoFields(round.avg_throw_length_feet, course_round.players_avg_throw_length_feet)
                round.par_difference_to_round_avg = CalculateDifferenceFromTwoFields(round.round_par, course_round.players_avg_par)
                round.round_rating_difference_to_round_avg = CalculateDifferenceFromTwoFields(round.round_rating, course_round.players_avg_round_rating)
                round.avg_throws_per_hole_difference_to_round_avg = CalculateDifferenceFromTwoFields(round.avg_throws_per_hole, course_round.players_avg_throws_per_hole)

        return None

    CalculatePlayerPlacementOnRound(division.players)
    CalculateDifferencesToRoundAverages(division.players, division.rounds)
    CalculateDifferencesToPlayerAverages(division.players)


def UpdateDivisionRoundDetails(division_rounds, division_players):

    def GetPlayerRatingDuringTournament(player):
        rating_during_tournament = 0

        if player.rating_during_tournament:
            if player.rating_during_tournament[0]:
                rating_during_tournament = player.rating_during_tournament[0]

        return rating_during_tournament


    def GetPlayerPropagator(player):
        propagator = 0

        if player.propagator:
            propagator = 1

        return propagator


    start_data = {
        "players_round_total_throws": 0,
        "players_avg_throws": 0,
        "players_avg_par": 0,
        "players_avg_throw_length_meters": 0,
        "players_avg_throw_length_feet": 0,
        "players_dns_count": 0,
        "players_dnf_count": 0,
        "round_total_players": 0,
        "players_avg_round_rating": 0,
        "players_highest_round_rating": 0,
        "players_lowest_round_rating": 0,
        "players_avg_rating_during_tournament": 0,
        "propagator_count": 0
    }

    collected_data = {}

    if division_rounds and division_players:
        for player in division_players:
            rating_during_tournament = GetPlayerRatingDuringTournament(player)
            propagator = GetPlayerPropagator(player)
            for round in player.rounds:
                if not collected_data.get(round.round_number):
                    collected_data[round.round_number] = copy.copy(start_data)
                single_round_data = copy.deepcopy(start_data)

                if round.round_throws:
                    single_round_data["players_round_total_throws"] += round.round_throws
                    single_round_data["round_total_players"] += 1
                    single_round_data["players_avg_rating_during_tournament"] += rating_during_tournament
                    single_round_data["propagator_count"] += propagator
                    #import pdb; pdb.set_trace()

                if round.round_rating:
                    single_round_data["players_avg_round_rating"] += round.round_rating
                    single_round_data["players_highest_round_rating"] = round.round_rating
                    single_round_data["players_lowest_round_rating"] = round.round_rating
                
                if round.dns:
                    single_round_data["players_dns_count"] += 1
                
                if round.dnf:
                    single_round_data["players_dnf_count"] += 1

                if round.round_par:
                    single_round_data["players_avg_par"] += round.round_par

                if round.avg_throw_length_meters:
                    single_round_data["players_avg_throw_length_meters"] += round.avg_throw_length_meters

                if round.avg_throw_length_feet:
                    single_round_data["players_avg_throw_length_feet"] += round.avg_throw_length_feet

                if round.to_mongo().to_dict().get("round_number"):
                    for k, v in single_round_data.items():
                        if k in ["players_highest_round_rating"]:
                            if v > collected_data[round.round_number][k]:
                                collected_data[round.round_number][k] = v
                        elif k in ["players_lowest_round_rating"]:
                            if v < collected_data[round.round_number][k] or collected_data[round.round_number][k] == 0:
                                collected_data[round.round_number][k] = v
                        else:
                            collected_data[round.round_number][k] += v

        for k, v in collected_data.items():
            collected_data[k]["players_avg_throws"] = CalculateAverageFromTwoFields(collected_data[k]["players_round_total_throws"], collected_data[k]["round_total_players"])
            collected_data[k]["players_avg_par"] = CalculateAverageFromTwoFields(collected_data[k]["players_avg_par"], collected_data[k]["round_total_players"])
            collected_data[k]["players_avg_throw_length_meters"] = CalculateAverageFromTwoFields(collected_data[k]["players_avg_throw_length_meters"], collected_data[k]["round_total_players"])
            collected_data[k]["players_avg_throw_length_feet"] = CalculateAverageFromTwoFields(collected_data[k]["players_avg_throw_length_feet"], collected_data[k]["round_total_players"])
            collected_data[k]["players_avg_round_rating"] = CalculateAverageFromTwoFields(collected_data[k]["players_avg_round_rating"], collected_data[k]["round_total_players"])
            collected_data[k]["players_avg_rating_during_tournament"] = CalculateAverageFromTwoFields(collected_data[k]["players_avg_rating_during_tournament"], collected_data[k]["round_total_players"])

        for round in division_rounds:
            data_for_round = collected_data.get(round.round_number)

            round.players_avg_throws = data_for_round["players_avg_throws"]
            round.players_avg_par = data_for_round["players_avg_par"]
            round.players_avg_throw_length_meters = data_for_round["players_avg_throw_length_meters"]
            round.players_avg_throw_length_feet = data_for_round["players_avg_throw_length_feet"]
            round.players_round_total_throws = data_for_round["players_round_total_throws"]
            round.round_total_players = data_for_round["round_total_players"]
            round.players_dnf_count = data_for_round["players_dnf_count"]
            round.players_dns_count = data_for_round["players_dns_count"]
            round.players_avg_round_rating = data_for_round["players_avg_round_rating"]
            round.players_avg_throws_per_hole = CalculateAverageFromTwoFields(round.players_avg_throws, round.course_holes)
            round.players_highest_round_rating = data_for_round["players_highest_round_rating"] if data_for_round["players_highest_round_rating"] > 0 else None
            round.players_lowest_round_rating = data_for_round["players_lowest_round_rating"] if data_for_round["players_lowest_round_rating"] > 0 else None
            round.propagator_count = data_for_round["propagator_count"]
            round.players_avg_rating_during_tournament = data_for_round["players_avg_rating_during_tournament"]
            round.players_avg_round_rating_difference_to_avg_rating_during_tournament = CalculateDifferenceFromTwoFields(round.players_avg_round_rating, round.players_avg_rating_during_tournament)


def UpdateDivisionDetails(division):
    division_data = {
        "total_holes": 0, #course round
        "total_holes_played_by_players": 0, #course round
        "total_course_length_meters": 0, #course round
        "total_course_length_feet": 0, #course round
        "total_throws": 0, #course round
        "total_money_won": 0, #players
        "players_avg_throws": 0, #players
        "players_avg_par": 0, #players
        "players_avg_round_rating": 0, #players
        "players_highest_round_rating": 0, #course round
        "players_lowest_round_rating": 0, #course round
        "players_avg_rating_during_tournament": 0, #players
        "players_avg_round_rating_difference_to_avg_rating_during_tournament": 0, #players
        "total_dns_count": 0, #course round
        "total_dnf_count": 0, #course round
        "total_unique_courses_or_layouts_played": 0, #course round
    }

    unique_courses_or_layouts = []

    def AddCoursesToUniqueCheck(round):
        course_string = ""

        if round.course_name:
            course_string += round.course_name
        if round.course_holes:
            course_string += str(round.course_holes)
        if round.course_par:
            course_string += str(round.course_par)    
        if round.course_length_meters:
            course_string += str(round.course_length_meters) 

        if course_string not in unique_courses_or_layouts:
            course_string = course_string.strip()
            unique_courses_or_layouts.append(course_string)

    all_players = division.players
    all_rounds = division.rounds

    for round in all_rounds:
        division_data["total_holes"] += ReturnValueOrZero(round.course_holes)
        division_data["total_holes_played_by_players"] += ReturnValueOrZero(round.course_holes) * ReturnValueOrZero(round.round_total_players)
        division_data["total_course_length_meters"] += ReturnValueOrZero(round.course_length_meters)
        division_data["total_course_length_feet"] += ReturnValueOrZero(round.course_length_feet)
        division_data["total_throws"] += ReturnValueOrZero(round.players_round_total_throws)

        AddCoursesToUniqueCheck(round)
        CheckHighestLowestRoundRating(round.players_highest_round_rating, type="highest", dict=division_data)
        CheckHighestLowestRoundRating(round.players_lowest_round_rating, type="lowest", dict=division_data)

    division_data["total_unique_courses_or_layouts_played"] = len(unique_courses_or_layouts)


    for player in all_players:
        division_data["total_money_won"] += ReturnValueOrZero(player.money_won)
        division_data["players_avg_throws"] += ReturnValueOrZero(player.total_throws)
        division_data["players_avg_par"] += ReturnValueOrZero(player.total_par)
        division_data["players_avg_round_rating"] += ReturnValueOrZero(player.avg_round_rating)
        division_data["players_avg_rating_during_tournament"] += ReturnValueOrZero(player.rating_during_tournament[0])
        if player.dns:
            division_data["total_dns_count"] += 1
        if player.dnf:
            division_data["total_dnf_count"] += 1
        #division_data["players_avg_round_rating_difference_to_avg_rating_during_tournament"] += ReturnValueOrZero(player.money_won)

    

    division.total_holes = division_data["total_holes"] if division_data["total_holes"] > 0 else None
    division.total_holes_played_by_players = division_data["total_holes_played_by_players"] if division_data["total_holes_played_by_players"] > 0 else None
    division.total_course_length_meters = division_data["total_course_length_meters"] if division_data["total_course_length_meters"] > 0 else None
    division.total_course_length_feet = division_data["total_course_length_feet"] if division_data["total_course_length_feet"] > 0 else None
    division.total_throws = division_data["total_throws"] if division_data["total_throws"] > 0 else None
    division.total_money_won = division_data["total_money_won"] if division_data["total_money_won"] > 0 else None
    division.players_avg_throws = CalculateAverageFromTwoFields(division_data["players_avg_throws"], division.total_players)
    division.players_avg_par = CalculateAverageFromTwoFields(division_data["players_avg_par"], division.total_players)
    division.players_avg_round_rating = CalculateAverageFromTwoFields(division_data["players_avg_round_rating"], division.total_players)
    division.players_highest_round_rating = division_data["players_highest_round_rating"] if division_data["players_highest_round_rating"] > 0 else None
    division.players_lowest_round_rating = division_data["players_lowest_round_rating"] if division_data["players_lowest_round_rating"] > 0 else None
    division.players_avg_rating_during_tournament = CalculateAverageFromTwoFields(division_data["players_avg_rating_during_tournament"], division.total_players)
    division.players_avg_round_rating_difference_to_avg_rating_during_tournament = CalculateDifferenceFromTwoFields(division.players_avg_round_rating, division.players_avg_rating_during_tournament)
    division.total_dns_count = division_data["total_dns_count"]
    division.total_dnf_count = division_data["total_dnf_count"]
    division.total_unique_courses_or_layouts_played = division_data["total_unique_courses_or_layouts_played"]


def CalculateTournamentStatistics(tournament):
    fields = {
        "total_throws": 0,
        "players_highest_round_rating": 0,
        "players_lowest_round_rating": 0,
        "total_dns_count": 0,
        "total_dnf_count": 0,
        "players_avg_rating_during_tournament": 0,
    }

    for div in tournament.divisions:
        fields["total_throws"] += ReturnValueOrZero(div.total_throws)
        CheckHighestLowestRoundRating(div.players_highest_round_rating, "highest", dict=fields)
        CheckHighestLowestRoundRating(div.players_lowest_round_rating, "lowest", dict=fields)
        fields["total_dns_count"] += ReturnValueOrZero(div.total_dns_count)
        fields["total_dnf_count"] += ReturnValueOrZero(div.total_dnf_count)
        fields["players_avg_rating_during_tournament"] += ReturnValueOrZero(div.players_avg_rating_during_tournament)

    tournament.total_throws = fields["total_throws"] if fields["total_throws"] > 0 else None
    tournament.players_highest_round_rating = fields["players_highest_round_rating"] if fields["players_highest_round_rating"] > 0 else None
    tournament.players_lowest_round_rating = fields["players_lowest_round_rating"] if fields["players_lowest_round_rating"] > 0 else None
    tournament.total_dns_count = fields["total_dns_count"]
    tournament.total_dnf_count = fields["total_dnf_count"]
    tournament.players_avg_rating_during_tournament = CalculateAverageFromTwoFields(fields["players_avg_rating_during_tournament"], len(tournament.divisions))
    