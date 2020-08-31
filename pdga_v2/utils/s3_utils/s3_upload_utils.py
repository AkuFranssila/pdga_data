import logging
import datetime
import tempfile
import json
import os
from pdga_v2.utils.general_utils.aws_client import AWS_CLIENT

logging.getLogger().setLevel("INFO")
TEMP_DIRECTORY = tempfile.mkdtemp()
aws_s3 = AWS_CLIENT("s3")


def upload_data_to_s3(folders_and_file_name, file_location, bucket="pdga-project-data"):
    """
    Upload bigger files to S3. Bucket is by default pdga data project bucket. file_name is the file location. 
    Folders is the S3 structure where the data needs to be saved and if the file needs to be renamed. 
    """
    logging.info("Uploading to %s", folders_and_file_name)
    aws_s3.upload_file(file_location, bucket, folders_and_file_name)


def save_to_temp_file_and_upload_to_s3(s3_folder_name, sub_folder_name, file_name_prefix, file_name_suffix, data_to_send, suffix=".json"):
    """
    Create temp file and save crawled or parsed data there. Send it to a specific main folder and subfolder with date.

    Main folders are player-raw-data, player-parsed-data, tournament-parsed-data, tournament-raw-data
    """

    logging.info("Sending data to %s and subfolder %s with name %s%s%s", s3_folder_name, sub_folder_name, file_name_prefix, file_name_suffix, suffix)
    with tempfile.NamedTemporaryFile(suffix=suffix, mode="w", delete=False, encoding='utf-8') as tp:
        s3_folder_key = f'{s3_folder_name}/{sub_folder_name}/{file_name_prefix}{file_name_suffix}{suffix}'
        tp.write(json.dumps(data_to_send))
        upload_data_to_s3(s3_folder_key, tp.name)
        tp.close()


def upload_object_s3(s3_folder_name, sub_folder_name, file_name_prefix, file_name_suffix, data_to_send, suffix=".json", bucket="pdga-project-data"):
    """
    Upload single object to S3
    """
    logging.info("Sending data to %s and subfolder %s with name %s%s%s", s3_folder_name, sub_folder_name, file_name_prefix, file_name_suffix, suffix)
    s3_key = f'{s3_folder_name}/{sub_folder_name}/{file_name_prefix}{file_name_suffix}{suffix}'
    
    aws_s3.put_object(Body=json.dumps(data_to_send, indent=4), Bucket=bucket, Key=s3_key)
