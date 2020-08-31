# coding=utf-8
import os
from mongoengine import connect

def ConnectMongo():
    connect('pdga', host=f"mongodb://{os.environ['mongodb_user']}:{os.environ['mongodb_pw']}@pdga-ht2vk.mongodb.net/pdga?ssl=true&authSource=admin&retryWrites=true&w=majority")
