# coding=utf-8
import logging
import unittest
import sys
import os
cwd = os.getcwd()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
from helpers_data_parsing import *
from mongoengine import *
from schemas import Player, Tournament

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

class TestMongoDB(unittest.TestCase):
    logging.info('Starting mongodb tests')
    @classmethod
    def setUpClass(cls):
        connect('mongoenginetest', host='mongomock://localhost')

    @classmethod
    def tearDownClass(cls):
       disconnect()

    def test_thing(self):
        pers = Player(full_name='John', pdga_number=1234569)
        pers.save()

        fresh_pers = Player.objects().first()
        assert fresh_pers.full_name ==  'John'

if __name__ == '__main__':
    unittest.main()
