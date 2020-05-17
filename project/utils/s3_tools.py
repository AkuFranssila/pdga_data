import logging
import datetime
import tempfile
from project.utils.aws_s3_client import AWS_S3CLIENT

logging.getLogger().setLevel("INFO")
s3_client = AWS_S3CLIENT()
TEMP_DIRECTORY = tempfile.mkdtemp()

def find_all_keys_from_folder(key, bucket="pdga-project-data"):
    """
    Find all files from specific folder (key). Buckets defaults to pdga-project-data.

    Returns a list of keys found in the specified folder (key).
    """
    response = s3_client.list_objects_v2(
        Bucket=bucket,
        Prefix=key,
    )

    found_keys = []

    for key_json in response["Contents"]:
        file_key = key_json["Key"]
        found_keys.append(file_key)


    return found_keys


def download_file_from_s3_return_file_path(key, download_name, bucket="pdga-project-data"):
    """
    Downloads file from S3 and returns the path of the file.
    """
    full_download_path = TEMP_DIRECTORY + "/" + download_name
    s3_client.download_file(bucket, key, full_download_path)

    return full_download_path


