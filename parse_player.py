# coding=utf-8
import json
import logging
from mongoengine import connect
from schemas import Player


#Fields from crawler
    #full_name
    #pdga_number
    #location_full
    #classification
    #member since
    #current rating
    #rating_difference
    #total_events
    #total_wins
    #career earnings
    #individual_tournament_years
    #first_crawl_date
#Fields that need to created at parsing
    #Created from player_name
        #first_name
        #last_name
    #Created from player_location_raw
        #city
        #state
        #country
    #Created from player_membership_status
        #membership_status (True/False, add field info depending on what is received from player_membership_status)
        #membership (add if normal/eagle club/ace club/birdie club and so on)
    #Created from player_current_rating
        #highest_rating (crawl from pdga and add logic that would do this from current rating)
        #lowest_rating (crawl from pdga and add logic that would do this from current rating)
    #Created from player_rating_updated
        #latest_rating_update (need to parse date)
    #Created from player_certified_status
        #certified_status (parse from crawler data)
    #Created from player_certified_status_expiration
        #certified_status_expiration_date (need to parse date)
    #Created from player_id
        #pdga_page_link (create from ID)
    #Created from Tournaments
        #played_event_ids (add data to this field once tournaments parsed)
        #played_countries (add data to this field once tournaments parsed)
    #Created during parse, no original data source
        #latest_update (add during parse)
        #fields_updated (add if field exists already, logic how to compare data)
