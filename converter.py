import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def write_json_to_csv_file(event_array):
    try:
        with open("/tmp/output.txt", "a") as f:
            f.truncate(0)
            for i in event_array:
                file_name = (i["file_name"])
                row_count = (i["row_count"])
                
                f.write(f"{file_name},{row_count}\n")
                logger.info("File write completed successfully")

    except Exception as e:
        logger.error("Error in write_json_to_csv_file: {e}".format(e=e))
        raise

def upload_file_to_s3(file_name, bucket_name, object_name):
    try:
        s3 = boto3. client('s3')
        s3.upload_file(file_name, bucket_name, object_name)
        logger.info("Successfully uploaded file to s3 bucket")
    except Exception as e:
        logger.error("Error during writing to s3 bucket: {e}".format(e=e))
        raise


def lambda_handler(event, context):
    try:
        target_s3_bucket = event["bucket_name"]
        target_file_name = event["target_file_name"]
        tmp_file_name = "/tmp/output.txt"

        write_json_to_csv_file(event["input"])
        upload_file_to_s3(tmp_file_name, target_s3_bucket, target_file_name)

        return {
             "statusCode": 200,
             "status" : "File written successfully to lambda",
        }
    except Exception as e:
        logger.error("Error in lambda_handler: {e}".format(e=e))
        raise
