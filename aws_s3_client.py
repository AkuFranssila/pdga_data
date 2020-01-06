import os
import boto3


def AWS_S3CLIENT():
    ACCESS_KEY= os.environ['AWS_ACCESS_KEY_ID']
    SECRET_KEY= os.environ['AWS_SECRET_ACCESS_KEY']

    client = boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY
    )

    return client
