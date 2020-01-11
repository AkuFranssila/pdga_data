# coding=utf-8
import json
import logging
from helpers_data_management import DownloadFileFromS3
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


file_location = DownloadFileFromS3("player-raw-data")

with open(file_location, "r") as data:
    logging.info("Opening file %s" % file_location)
    json_data = json.loads(data)
    for json in json_data:
        import pdb; pdb.set_trace()

#logging.info('Finished parse - parsed ' + str(len(data_from_file)) + ' players')
