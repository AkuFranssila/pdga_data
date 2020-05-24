# coding=utf-8
import os
import json
import logging
import datetime
import requests
import pycountry
import time
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
        if var == "999":
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


def CalculateAvgFromRounds(throws, rounds):
    if throws is not None:
        if throws == 0 or len(rounds) == 0:
            return 0
        else:
            ttl = throws / len(rounds)
    else:
        return None


def CalculateAvgRoundRating(rounds):
    r_numbers = len(rounds)
    total_rating = 0
    for r in rounds:
        r = json.loads(r.to_json())
        try:
            if r['round_rating'] is not None and r['round_throws'] < 980:
                total_rating += r['round_rating']
            else:
                r_numbers -= 1
        except:
            r_numbers -= 1
    try:
        avgrating = total_rating / r_numbers
    except:
        avgrating = None

    return avgrating


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
