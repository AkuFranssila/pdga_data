# coding=utf-8
import os
from mongoengine import connect

def ConnectMongo():
    #connect('pdga', host=f"mongodb://{os.environ['mongodb_user']}:{os.environ['mongodb_pw']}@pdga-ht2vk.mongodb.net/pdga?ssl=true&authSource=admin&retryWrites=true&w=majority")
    connect('pdga', host=f'mongodb://{os.environ["mongodb_user"]}:{os.environ["mongodb_pw"]}@pdga-shard-00-00-ht2vk.mongodb.net:27017,pdga-shard-00-01-ht2vk.mongodb.net:27017,pdga-shard-00-02-ht2vk.mongodb.net:27017/pdga?ssl=true&replicaSet=pdga-shard-0&authSource=admin&retryWrites=true&w=majority')
