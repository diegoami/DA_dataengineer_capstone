import json
import os
import traceback
import boto3
from botocore.errorfactory import ClientError


def check_bucket(s3, bucket_name, file_path):
    """
    check the existence of a s3 file
    :param s3 the boto3 client
    :param bucket_name: the s3 bucket name
    :param file_path: the full path of a file in a S3 bucket
    :return:
    """
    try:
        s3.head_object(Bucket=bucket_name, Key=file_path)
    except ClientError:
        return False
    return True


def try_read_data_from_json_file(file_name):
    """
    tries to retrieve data from wikipedia cached locally in a json file
    :param file_name: the name of the file containing data
    :return: data retrieved from file
    """
    rel_data = None
    if os.path.isfile(file_name):
        print("Reading data from file {}".format(file_name))
        with open(file_name, 'r', encoding="utf-8") as fhandle:
            try:
                rel_data = json.load(fhandle)
            except ValueError as ve:
                print("Could not read data from file {}".format(file_name))
                traceback.print_exc(ve)
    return rel_data


def try_read_data_from_s3(bucket_name, object_name, file_output, region_name):
    """
    tries to retrieve data from a S3 bucket
    :param bucket_name: name of the bucket to retrieve data from
    :param object_name: object in the S3 bucket to retrieve data from
    :param file_output: the local file to download data into
    :param region_name: the region where the file is located
    :return: the data contained in the file
    """
    s3_client = boto3.client('s3', region_name=region_name)
    if not check_bucket(s3_client, bucket_name, object_name):
        print("s3://{}/{} does not exist, skipping".format(bucket_name, object_name))
        return None
    s3_client.download_file(bucket_name, object_name, file_output)
    return try_read_data_from_json_file(file_output)


def save_to_s3(bucket, file_name, object_name):
    """
    tries and save file to S3
    :param bucket: the bucket to save the file into
    :param file_name: the name of the file to save data into
    :param object_name:
    :return: the response from the upload file execution
    """
    s3_client = boto3.client('s3')
    response = s3_client.upload_file(file_name, bucket, object_name)
    return response