import os

import boto3
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.typing import LambdaContext

tracer = Tracer()
logger = Logger()


@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def lambda_handler(event: object, context: LambdaContext) -> None:
    print(event, context)
    s3_client = boto3.client("s3")
    response = s3_client.list_objects_v2(
        Bucket=os.environ["DATA_BUCKET"],
        Prefix=os.environ["DATA_KEY_BASE"],
    )
    logger.info(response)
