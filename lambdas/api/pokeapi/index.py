import json
import os

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEvent

import boto3
import botocore

tracer = Tracer()
logger = Logger()
app = APIGatewayRestResolver()

@app.get("/api/.+")
@tracer.capture_method
def get_file():
    path = app.current_event.path.rstrip('/')

    bucket = os.environ['DATA_BUCKET']
    key = f"{os.environ['DATA_KEY_BASE']}{path}/index.json"

    logger.info('getting s3 file', bucket=bucket, key=key)

    s3 = boto3.resource('s3') # pylint: disable=invalid-name
    s3_object = s3.Object(bucket_name=bucket, key=key)
    try:
        response = s3_object.get()
        #TODO Raise 404 on missing file
        # response.raise_for_status()
        body = response['Body'].read()
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'NoSuchBucket':
            logger.exception(f'The bucket {bucket} doesnt exist. Check the param is accurate. If local check you have imported environment variables')
            raise error
        else:
            raise error

    # Must return a JSON object
    return json.loads(body)


@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True)
@tracer.capture_lambda_handler
def lambda_handler(event: APIGatewayProxyEvent, context: LambdaContext):
    
    app_resolve = app.resolve(event, context)

    return app_resolve
    
    #TODO parse in full url at call time ??

    #TODO pagenation and multiple calls - DynamoDB

    #TODO allow searching for name i can use the index in the upper level index.json to do this - DynamoDB

    #TODO implement https://docs.aws.amazon.com/apigateway/latest/developerguide/integrating-api-with-aws-services-s3.html
    