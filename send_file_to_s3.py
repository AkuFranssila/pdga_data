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
    accepted_types = ["old_pdga_data", "player-parsed-data", "player-raw-data", "tournament-parsed-data", "tournament-raw-data"]

    if type not in accepted_types:
        logging.critical("Type is not accepted value, check accepted types: %s" % ", ".join(accepted_types))
        return False
    else:

        all_data = []
        with open(filename, "r") as data:
            logging.info("Opening file %s" % filename)
            for line in data:
                all_data.append(line)

        file_extension = ".txt"
        data_location = type + "/" + type + filename.split(type)[-1].rsplit('.', 1)[0] + file_extension
        #data_location = type + "/" + filename.split('\\')[-1].rsplit('.', 1)[0] + file_extension
        logging.info('Sending data to S3 bucket pdga-project-data, location of the file is %s' % data_location)
        s3.put_object(Bucket="pdga-project-data", Key=data_location, Body=all_data)

        logging.info("Checking if file exists on S3 we just sent")
        if check_if_file_exists_s3(s3, data_location) > 0:
            logging.info("File exists on S3")
            return True
        else:
            logging.info("File not found on S3")
            return False

def send_multipart_file_to_s3(filename, type):
    logging.info("Starting send_multipart_file_to_s3")
    accepted_types = ["old_pdga_data", "player-parsed-data", "player-raw-data", "tournament-parsed-data", "tournament-raw-data"]

    file_ending = filename.rsplit('.', 1)[1]
    if file_ending == "json":
        file_extension = ".json"
    else:
        file_extension = ".txt"
    #local_data_location = filename.rsplit('\\', 1)[0] + "\\" + type + filename.split(type)[-1].rsplit('.', 1)[0] + file_extension

    for type in accepted_types:
        if type in filename:
            break
        else:
            type = ""

    if type == "":
        logging.critical("Type is not accepted value, check accepted types: %s" % ", ".join(accepted_types))
        return False
    s3_data_location = type + "/" + type + filename.split(type)[-1].rsplit('.', 1)[0] + file_extension
    logging.info("Starting s3 upload")

    with open(filename, "rb") as f:
        s3 = AWS_S3CLIENT()
        s3.upload_fileobj(f, "pdga-project-data", s3_data_location)

    logging.info("File uploaded to S3")
    #s3.upload_file(filename, "pdga-project-data", s3_data_location)
    return True


#latest_file = FindFiles('crawled_players').find_latest_file()
#print(latest_file)
#send_file_to_s3('.\\crawled_players\\player-raw-data-2020-01-24.txt', "player-raw-data")
#send_multipart_file_to_s3('.\\crawled_players\\player-raw-data-2020-01-12.txt', "player-raw-data")
#send_file_to_s3('.\\crawled_players\\player-raw-data-2020-01-24.txt', "player-raw-data")
