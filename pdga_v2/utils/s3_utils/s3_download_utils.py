import logging
import datetime
import tempfile
import json
from pdga_v2.utils.general_utils.aws_client import AWS_CLIENT

logging.getLogger().setLevel("INFO")
TEMP_DIRECTORY = tempfile.mkdtemp()
aws_s3 = AWS_CLIENT("s3")

def download_file_from_s3_return_file_path(key, download_name, bucket="pdga-project-data"):
    """
    Downloads file from S3 and returns the path of the file.
    """
    logging.info("Downloading %s as %s", key, download_name)
    full_download_path = f'{TEMP_DIRECTORY}\\{download_name}'
    aws_s3.download_file(bucket, key, full_download_path)

    return full_download_path


def download_object_s3(key, bucket="pdga-project-data"):
    """
    Download object from S3 and return it's content
    """

    logging.info("Downloading object from key %s", key)

    s3_object = aws_s3.get_object(Bucket=bucket, Key=key)
    s3_object_as_json = json.loads(s3_object['Body'].read().decode('utf-8'))

    return s3_object_as_json
    