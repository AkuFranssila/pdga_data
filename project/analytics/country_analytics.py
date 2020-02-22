# coding=utf-8
import sys
import json
import logging
import datetime
from project.utils.connect_mongodb import ConnectMongo
from project.models.schemas import Player, Tournament
from mongoengine import *
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

logging.info('Starting country analytics generation script')
ConnectMongo()

all_countries = Player.objects.filter().distinct(field="country")
import pdb; pdb.set_trace()
all_countries.append('all')

#for country in all_countries:
#    if country == "all":
