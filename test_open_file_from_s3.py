import json
from aws_s3_client import AWS_S3CLIENT

#s3 = AWS_S3CLIENT()

#s3.download_file('pdga-project-data','player-raw-data/january-test-data.json','.\\crawled_players\\list_of_dicts.json')

with open('.\\crawled_players\\list_of_dicts.json', 'r') as file:
    data = json.load(file)
    print(data[0]["pdga_number"])
