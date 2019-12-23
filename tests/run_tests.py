# coding=utf-8
import runpy

def RunAllTests():
    runpy.run_path('test_data_parsing.py', run_name='__main__')

def RunSingleTest(filename):
    runpy.run_path(filename)

def main():
    RunAllTests()

if __name__=='__main__':
   main()
