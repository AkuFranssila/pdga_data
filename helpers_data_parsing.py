# coding=utf-8
import json
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


#name = "Aku Franssila"


def ParseFullName(name):
    name = name.split(' ')
    if len(name) > 2:
        first_name = name[0] + ' ' + name[1]
        last_name = name[-1]
    else:
        first_name = name[0]
        last_name = name[-1]

    return first_name, last_name


def ParseFullLocation(location):
    location = location.split(',')
    if len(location) >= 3 and location[-1] == "United States":
        location_city = location[0]
        location_state = location[1]
        location_country = "United States"
        logging.info('If statement 1')
    elif len(location) >= 3:
        logging.info('If statement 2')
        location_city = location[0]
        location_state = location[1]
        location_country = location[-1]
    elif len(location) == 2 and "United States" not in location:
        location_city = location[0]
        location_state = None
        location_country = location[-1]
    elif len(location) == 2 and "United States" in location:
        location_city = None
        location_state = location[0]
        location_country = location[-1]
    else:
        location_city = None
        location_state = None
        location_country = location[-1]

    return city, state, country




def ParseDate(date):
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
    date = day + '-' + month_dict[month] + '-' + year
    return date
