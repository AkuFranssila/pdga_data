# coding=utf-8
import json
import logging


#Class
#Contains function to open files
    #if **kwargs are list then loop through all lists


#Open & loop file(s)
#Send data to mongo
#Save file
#Find file


#open and loop files logic
# 1. check if given argument is correct type
    # if anything other than list or string -> error
    # if list

#Works only if single file given
file = '.\\crawled_players\\player_data_2019-09-13.json'
with open(file, 'r') as opened_file:
    data = json.load(opened_file)

#print (data_from_file)

multi_files = ['.\\crawled_players\\player_data_2019-09-13.json', '.\\crawled_players\\player_data_2019-10-01.json', '.\\crawled_players\\player_data_2019-10-14.json']

data_from_files = []
for i in multi_files:
    with open(i, 'r') as opened_file:
        data = json.load(opened_file)
        data_from_files.append(data)
    #    for data in opened_file:
    #        data_from_files.append(data)

import pdb; pdb.set_trace()
combined_data = []
for i in data_from_files:
    combined_data += i

print ('Len single')
print (len(data_from_file))
print ('Len multi')
print (len(combined_data))

print (combined_data)
# print ('-')
# print ('-')
# print ('-')
# print ('-')
# print ('-')
# print (data_from_files[1])
