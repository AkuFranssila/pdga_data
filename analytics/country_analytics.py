# coding=utf-8
import sys
import json
import logging
import datetime
sys.path.append('/pdga_ratings/pdga_data')
from connect_mongodb import ConnectMongo
from schemas import Player, Tournament
from mongoengine import *
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

logging.info('Starting country analytics generation script')
ConnectMongo()

all_countries = Player.objects.filter().distinct(field="country")
import pdb; pdb.set_trace()
all_countries.append('all')

#for country in all_countries:
#    if country == "all":
