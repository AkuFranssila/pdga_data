# coding=utf-8
import logging
import unittest
import sys
import os
cwd = os.getcwd()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
from helpers.helpers_data_parsing import *
from tournament_processes.tournament import ParseTournament
from mongoengine import connect, disconnect
from models.schemas import Player, Tournament

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

class TestTournament(unittest.TestCase):
    logging.info('Starting mongodb tournament schema tests')
    @classmethod
    def setUpClass(cls):
        connect('mongoenginetest', host='mongomock://localhost')

    @classmethod
    def tearDownClass(cls):
       disconnect()

    def test_create_and_update_tournament(self):
        tournament_data = {}


if __name__ == '__main__':
    unittest.main()
