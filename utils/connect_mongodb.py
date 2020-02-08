# coding=utf-8
import json
import logging
import os
from mongoengine import connect
from schemas import Player, Tournament

def ConnectMongo():
    connect('pdga', host='mongodb://' + os.environ['mongodb_user'] + ':' + os.environ['mongodb_pw'] + '@pdga-shard-00-00-ht2vk.mongodb.net:27017,pdga-shard-00-01-ht2vk.mongodb.net:27017,pdga-shard-00-02-ht2vk.mongodb.net:27017/pdga?ssl=true&replicaSet=pdga-shard-0&authSource=admin&retryWrites=true&w=majority')
