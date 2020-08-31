import logging
import datetime
import tempfile
import json
from project.utils.aws_s3_client import AWS_S3CLIENT
from project.utils.send_file_to_s3 import upload_data_to_s3

logging.getLogger().setLevel("INFO")
s3_client = AWS_S3CLIENT("s3")
TEMP_DIRECTORY = tempfile.mkdtemp()

def find_all_keys_from_s3_folder(key, bucket="pdga-project-data"):
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
        file_key = key_json.get("Key")
        if file_key:
            found_keys.append(file_key)


    return found_keys


def download_file_from_s3_return_file_path(key, download_name, bucket="pdga-project-data"):
    """
    Downloads file from S3 and returns the path of the file.
    """
    full_download_path = TEMP_DIRECTORY + "\\" + download_name
    s3_client.download_file(bucket, key, full_download_path)

    return full_download_path


def save_to_temp_file_and_upload_to_s3(s3_folder, file_date, file_counter, data_to_send, suffix=".json"):
    """
    Create temp file and save crawled or parsed data there. Send it to a specific main folder and subfolder with date.

    Main folders are player-raw-data, player-parsed-data, tournament-parsed-data, tournament-raw-data
    """

    logging.info("Sending data to %s with date %s", s3_folder, file_date)
    with tempfile.NamedTemporaryFile(suffix=suffix, mode="w", delete=False) as tp:
        s3_folder_key = f'{s3_folder}/{file_date}/data_{file_counter}.json'
        tp.write(json.dumps(data_to_send))
        upload_data_to_s3(s3_folder_key, tp.name)
        tp.close()


