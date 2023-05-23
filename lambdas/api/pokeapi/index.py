import os
import boto3

def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    s3_object = s3.Object(bucket_name=os.envron['DATA_BUCKET'], key=os.envion['DATA_KEY'])
    body = s3_object.get()['Body'].read()
    
    response = {
      "statusCode": 200,
      "headers": {
        "Content-Type": "application/json"
      },
      "isBase64Encoded": False,
      "body": body
    }

    return response