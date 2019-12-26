# coding=utf-8
import runpy

def RunAllTests():
    #Closes after first test, just add all tests to circleci config so it runs them in order
    runpy.run_path('test_data_parsing.py', run_name='__main__')
    runpy.run_path('test_mongodb.py', run_name='__main__')

def RunSingleTest(filename):
    runpy.run_path(filename, run_name='__main__')

def main():
    RunAllTests()

if __name__=='__main__':
   main()
