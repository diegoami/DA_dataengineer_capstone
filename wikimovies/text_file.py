import csv
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



def export_to_csv(exp_data, exp_output, map_query_columns):
    with open(exp_output, 'w', encoding="utf-8") as ehandle:
        print("Writing to {}".format(exp_output))
        f = csv.writer(ehandle)
        f.writerow(map_query_columns.values())
        for item in exp_data:
            f.writerow(item.values())


def try_read_data_from_json_file(file_output):
    rel_data = None
    if os.path.isfile(file_output):
        print("Reading data from file {}".format(file_output))
        with open(file_output, 'r', encoding="utf-8") as fhandle:
            try:
                rel_data = json.load(fhandle)
            except ValueError as ve:
                print("Could not read data from file {}".format(file_output))
                traceback.print_exc(ve)
    return rel_data


def try_read_data_from_s3(bucket_name, object_name, file_output, region_name):
    s3_client = boto3.client('s3', region_name=region_name)
    if not check_bucket(s3_client, bucket_name, object_name):
        print("s3://{}/{} does not exist, skipping".format(bucket_name, object_name))
        return None
    s3_client.download_file(bucket_name, object_name, file_output)
    return try_read_data_from_json_file(file_output)


def save_to_s3(bucket, file_name, object_name):
    s3_client = boto3.client('s3')
    response = s3_client.upload_file(file_name, bucket, object_name)
    return response