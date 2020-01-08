import json
from aws_s3_client import AWS_S3CLIENT

s3 = AWS_S3CLIENT()

files = s3.list_objects_v2(Bucket="pdga-project-data", Prefix="player-raw-data")["Contents"]

for f in files:
    print(f["Key"])

#s3.download_file('pdga-project-data','player-raw-data/january-test-data.json','.\\crawled_players\\list_of_dicts.json')

#with open('.\\crawled_players\\list_of_dicts.json', 'r') as file:
#    data = json.load(file)
#    print(data[0]["pdga_number"])
