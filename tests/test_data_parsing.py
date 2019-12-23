# coding=utf-8
import logging
import unittest
import sys
import os
cwd = os.getcwd()
from os import listdir

print (cwd)
print (os.listdir())
#sys.path.append('../pdga_data')
#from helpers_data_parsing import *
#import .helpers_data_parsing
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

class TestDataParsers(unittest.TestCase):

    def test_fullname_parser(self):
        #self.assertEqual(ParseFullName("Clark Kent"), ('Clark', 'Kent'))
        print ('lol')

    # def test_upper(self):
    #     self.assertEqual('foo'.upper(), 'FOO')
    #
    # def test_isupper(self):
    #     self.assertTrue('FOO'.isupper())
    #     self.assertFalse('Foo'.isupper())
    #
    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)

if __name__ == '__main__':
    unittest.main()
