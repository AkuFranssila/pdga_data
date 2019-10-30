# coding=utf-8
import json
import logging
from connect_mongodb import ConnectMongo
from schemas import Player
from mongoengine import *
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

def ParseFullName(name):
    if name == "Page not found":
        return None, None
    if name is not None:
        name = name.split(' ')
        if len(name) > 2:
            first_name = name[0] + ' ' + name[1]
            last_name = name[-1]
        else:
            first_name = name[0]
            last_name = name[-1]
        return first_name, last_name
    else:
        return None, None

def ParseFullLocation(location):
    us_states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
        }

    if location is None:
        return None, None, None

    location = location.split(',')
    cleaned_location = []
    for loc in location:
        cleaned_location.append(loc.strip())
    location = cleaned_location
    if len(location) >= 3 and location[-1] == "United States":
        city = location[0]
        try:
            state = us_states[location[1]]
        except:
            state = location[1]
        country = "United States"
        logging.info('If statement 1')
    elif len(location) >= 3 and "United States" in location:
        logging.info('If statement 2')
        city = location[0]
        try:
            state = us_states[location[1]]
        except:
            state = location[1]
        country = location[-1]
    elif len(location) >= 3:
        logging.info('If statement 3')
        city = location[0]
        state = location[1]
        country = location[-1]
    elif len(location) == 2 and "United States" not in location:
        logging.info('If statement 4')
        if len(location[1]) == 2:
            country = "United States"
            try:
                state = us_states[location[1]]
            except:
                state = location[1]
            city = location[0]
        else:
            city = location[0]
            state = None
            country = location[-1]
    elif len(location) == 2 and "United States" in location:
        logging.info('If statement 5')
        city = None
        state = location[0]
        country = location[-1]
    else:
        logging.info('If statement 6')
        city = None
        state = None
        country = location[-1]

    return city, state, country

def ParseDate(date):
    #import pdb; pdb.set_trace()
    if date is None:
        return None
    day,month,year = date.split('-')
    month_dict = {
            "Jan":"01",
            "Feb":"02",
            "Mar":"03",
            "Apr":"04",
            "May":"05",
            "Jun":"06",
            "Jul":"07",
            "Aug":"08",
            "Sep":"09",
            "Oct":"10",
            "Nov":"11",
            "Dec":"12"
            }
    date = year + '-' + month_dict[month] + '-' + day
    return date

def PlayerExists(pdga_number):
    logging.info(f'Checking if player exists {str(pdga_number)}')
    try:
        player = Player.objects.get(pdga_number=pdga_number)
        player_exists = True
    except: #schemas.DoesNotExist
        player = Player()
        player_exists = False

    return player, player_exists

def ParseIdStatus(full_name, id_status):
    if full_name == "Page not found":
        return False
    else:
        return id_status

def CheckMembershipStatus(membership_status):
    if membership_status is not None:
        membership_status = membership_status.lower().strip()
    accepted_statuses = ['ace club', 'eagle club', 'birdie club', 'active', 'current']
    if membership_status in accepted_statuses:
        return membership_status, True
    else:
        return membership_status, False

def ParseClassification(classification):
    if classification is None:
        return None
    else:
        return classification.lower()

def ParseMemberSince(year):
    if year == "Unknown":
        return 0
    elif year is not None:
        return year
    else:
        return None

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


def ParseRatings(
                rating,
                old_rating,
                old_lowest,
                old_highest,
                rating_difference,
                latest_update,
                membership_status
                ):

    if old_rating is None or old_lowest is None and old_highest is None:
        highest_rating = rating
        current_rating = rating
        lowest_rating = rating
        latest_update = latest_update
        difference = rating_difference
        return (lowest_rating,
                current_rating,
                highest_rating,
                difference,
                latest_update)
    elif old_rating is not None and old_lowest is not None and old_highest is not None and CheckMembershipStatus(membership_status)[1]:
        current_rating = rating
        if rating > old_highest:
            highest_rating = rating
        else:
            highest_rating = old_highest
        if old_lowest > rating:
            lowest_rating = rating
        else:
            lowest_rating = old_lowest

        return (lowest_rating,
                current_rating,
                highest_rating,
                rating_difference,
                latest_update
                )
    else:
        return (old_lowest, rating,old_highest, rating_difference, latest_update)

def ParseIndividualTournamentYears(list_of_years, membership_status, old_data):
    if CheckMembershipStatus(membership_status)[1]:
        return list_of_years
    elif old_data is None:
        return list_of_years

def ParseCertifiedStatus(certified_status, expiration_date):
    if certified_status == "Certified":
        return True, ParseDate(expiration_date)
    else:
        return False, None

def FindPlayedEventIds(pdga_number):
    played_events = Tournament.objects.filter(player__pdga_id=pdga_number).only("tournament_id")
    return played_events

def CompareDicts(old_data, new_data):
    if old_data == 418:
        import pdb; pdb.set_trace()
    try:
        old_data = Player.objects(pdga_number=old_data).first().to_json()
    except:
        old_data = None
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
        all_new = new_data
        None, None, None, None, all_new

def CreateFieldsUpdated(added_data, removed_data, modified_data, date, all_new):
    parsed_added = {}
    parsed_removed = {}
    parsed_modified = {}

    if added_data and removed_data and modified_data is not None:
        if len(added_data) != 0:
            parsed_added = list(added_data)


        if len(removed_data) != 0:
            parsed_removed = list(removed_data)
            import pdb; pdb.set_trace()
            for k, v in removed_data.items():
                try:
                    v[0]['date'] = v[0].pop('$date')
                    v[1]['date'] = v[1].pop('$date')
                except:
                    None
                parsed_removed[k] = {'old_value': v[0], 'new_value': v[1]}


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

    return all_new
