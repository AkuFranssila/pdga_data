# coding=utf-8
import json
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

def ParseFullName(name):

    #Split name
    #check how long it is
    #put the last part as lastname
    #generate first name by looping through all the names on list except the last one
    name = name.split(' ')
    name_len = len(name)

    if name_len > 4:
        first_name = " ".join(name[:-1])
        last_name = name[-1]
    elif len(name) == 4:
        first_name = name[0] + ' ' + name[1]
        last_name = name[2] + ' ' + name[3]
    elif len(name) > 2:
        first_name = name[0] + ' ' + name[1]
        last_name = name[-1]
    else:
        first_name = name[0]
        last_name = name[-1]

    return first_name, last_name


def ParseFullLocation(location):
    logging.info('Parsing location: ' + location)
    location = location.split(',')
    logging.info(location)
    if len(location) >= 3 and location[-1] == "United States":
        location_city = location[0].strip()
        location_state = location[1].strip()
        location_country = "United States"
        logging.info('If statement 1')
    elif len(location) >= 3:
        logging.info('If statement 2')
        location_city = location[0].strip()
        location_state = location[1].strip()
        location_country = location[-1].strip()
    elif len(location) == 2 and "United States" not in location:
        logging.info('If statement 3')
        location_city = location[0].strip()
        location_state = None
        location_country = location[-1].strip()
    elif len(location) == 2 and "United States" in location:
        logging.info('If statement 4')
        location_city = None
        location_state = location[0].strip()
        location_country = location[-1].strip()
    else:
        logging.info('If statement 5')
        location_city = None
        location_state = None
        location_country = location[-1].strip()

    return location_city, location_state, location_country

def ParseDate(date):
    if date:
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
        day,month,year = date.split('-')
        date = day + '-' + month_dict[month] + '-' + year

    return date
