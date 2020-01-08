# coding=utf-8
import json
import logging
import os
import sys
import boto3
from datetime import datetime
from aws_s3_client import AWS_S3CLIENT
from helpers_data_management import OpenFileReturnData
from find_file import FindFiles
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

def check_if_file_exists_s3(client, key):
    """return the key's size if it exist, else None"""
    response = client.list_objects_v2(
        Bucket="pdga-project-data",
        Prefix=key,
    )
    for obj in response.get('Contents', []):
        if obj['Key'] == key:
            return obj['Size']

def send_file_to_s3(filename, type):
    s3 = AWS_S3CLIENT()
    test_data = [{"player":"test1"},{"player":"test2"}]


    data_to_s3 = []
    with open(filename, "r") as file_data:
        for single_line in file_data:
            json_data = json.loads(single_line)
            data_to_s3.append(json_data)

    binary_data = bytes(json.dumps(data_to_s3).encode('UTF-8'))

    accepted_types = ["old_pdga_data", "player-parsed-data", "player-raw-data", "tournament-parsed-data", "tournament-raw-data"]

    if type not in accepted_types:
        logging.critical("Type is not accepted value, check accepted types: %s" % ", ".join(accepted_types))
        return False
    else:
        file_extension = ".json"
        data_location = type + "/" + filename.split('\\')[-1].rsplit('.', 1)[0] + file_extension
        logging.info('Sending data to S3 bucket pdga-project-data, location of the file is %s' % data_location)
        s3.put_object(Bucket="pdga-project-data", Key=data_location, Body=binary_data)

        logging.info("Checking if file exists on S3 we just sent")
        if check_if_file_exists_s3(s3, data_location) > 0:
            logging.info("File exists on S3")
            return True
        else:
            return False

#latest_file = FindFiles('crawled_players').find_latest_file()
#print(latest_file)
send_file_to_s3('.\\crawled_players\\january-test-data.txt', "player-raw-data")
