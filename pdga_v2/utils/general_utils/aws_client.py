import os
import boto3


def AWS_CLIENT(aws_service, debug=False):
    ACCESS_KEY= os.environ['AWS_ACCESS_KEY_ID']
    SECRET_KEY= os.environ['AWS_SECRET_ACCESS_KEY']

    if debug:
        boto3.set_stream_logger('')

    client = boto3.client(
        aws_service,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY
    )

    return client
    