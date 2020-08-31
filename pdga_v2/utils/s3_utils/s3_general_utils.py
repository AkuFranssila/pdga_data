import logging
import datetime
import tempfile
import json
from pdga_v2.utils.general_utils.aws_client import AWS_CLIENT

logging.getLogger().setLevel("INFO")
TEMP_DIRECTORY = tempfile.mkdtemp()
aws_s3 = AWS_CLIENT("s3")


def find_all_keys_from_s3_folder(key, bucket="pdga-project-data"):
    """
    Find all files from specific folder (key). Buckets defaults to pdga-project-data.

    Returns a list of keys found in the specified folder (key).
    """

    logging.info("Checking S3 keys from: %s", key)

    response = aws_s3.list_objects_v2(
        Bucket=bucket,
        Prefix=key,
    )

    found_keys = []

    for key_json in response["Contents"]:
        file_key = key_json.get("Key")
        if file_key:
            found_keys.append(file_key)


    return found_keys


def check_if_file_exists_s3(key, bucket="pdga-project-data"):
    """
    Return True or False depending on if the file exists
    """

    logging.info("Checking if file exists: %s", key)

    response = aws_s3.list_objects_v2(
        Bucket=bucket,
        Prefix=key,
    )
    object_exists = False
    for obj in response.get('Contents', []):
        if obj['Key'] == key:
            object_exists = True
    
    return object_exists
