import os
import boto3
import json

ACCESS_KEY= os.environ['AWS_ACCESS_KEY_ID']
SECRET_KEY= os.environ['AWS_SECRET_ACCESS_KEY']

client = boto3.client(
    's3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY
)

#player-raw-data/player-raw-data-<crawldatetime>.json
#put_object(Bucket=dest_bucket_name, Key=dest_object_name, Body=object_data)
for bucket in client.list_buckets()['Buckets']:
    print(bucket)

test_data = [{"player":"test1"},{"player":"test2"}]
binary_data = bytes(json.dumps(test_data).encode('UTF-8'))

client.put_object(Bucket="pdga-project-data", Key="player-parsed-data/test_file.json", Body=binary_data)
# s3 = boto3.Session(
#     aws_access_key_id=ACCESS_KEY,
#     aws_secret_access_key=SECRET_KEY
# )

import pdb; pdb.set_trace()
print('')
