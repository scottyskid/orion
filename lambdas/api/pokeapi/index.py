""" Lambda function that gets pokeapi data
"""

import json
import os
import typing

import boto3
import botocore
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import (
    APIGatewayRestResolver,
    Response,
    content_types,
)
from aws_lambda_powertools.event_handler.exceptions import InternalServerError
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEvent
from aws_lambda_powertools.utilities.typing import LambdaContext

tracer = Tracer()
logger = Logger()
app = APIGatewayRestResolver()


@app.exception_handler(ValueError)  # type: ignore[misc]
def handle_invalid_limit_qs(ex: ValueError) -> Response:  # receives exception raised
    metadata: dict[str, str | dict[str, str] | None] = {
        "path": app.current_event.path,
        "query_strings": app.current_event.query_string_parameters,
    }
    logger.error(f"Malformed request: {ex}", extra=metadata)

    return Response(
        status_code=400,
        content_type=content_types.TEXT_PLAIN,
        body="Invalid request parameters.",
    )


@app.exception_handler(botocore.exceptions.ClientError)  # type: ignore[misc]
def handle_botocore_client_error(
    error: botocore.exceptions.ClientError,
) -> Response | None:  # receives exception raised
    if error.response["Error"]["Code"] == "NoSuchBucket":
        logger.exception(
            (
                "The bucket doesnt exist. Check the env var is accurate. ",
                "If local check you have imported environment variables",
            )
        )
        return Response(
            status_code=500,
            content_type=content_types.TEXT_PLAIN,
            body="Internal server error, Bucket does not exist",
        )
    if error.response["Error"]["Code"] == "NoSuchKey":
        logger.exception("The key doesnt exist")
        return Response(
            status_code=404,
            content_type=content_types.TEXT_PLAIN,
            body="Not found",
        )
    logger.exception("Unhandeled Botocore excpetion")
    raise InternalServerError("Internal server error")


@app.get("/api/.+")  # type: ignore[misc]
@tracer.capture_method
def get_file() -> dict[str, typing.Any]:
    path: str = app.current_event.path.rstrip("/")

    bucket: str = os.environ["DATA_BUCKET"]
    key: str = f"{os.environ['DATA_KEY_BASE']}{path}/index.json"

    logger.info("getting s3 file", bucket=bucket, key=key)

    s3 = boto3.resource("s3")  # pylint: disable=invalid-name
    s3_object = s3.Object(bucket_name=bucket, key=key)

    response = s3_object.get()
    body = response["Body"].read()

    # Must return a JSON object
    return json.loads(body)  # type: ignore[no-any-return]


@logger.inject_lambda_context(  # type: ignore[arg-type]
    correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True
)
@tracer.capture_lambda_handler
def lambda_handler(
    event: APIGatewayProxyEvent,
    context: LambdaContext,
) -> dict[str, typing.Any]:
    app_resolve = app.resolve(event, context)

    return app_resolve

    # TODO pagenation and multiple calls - DynamoDB

    # TODO allow searching for name,
    # i can use the index in the upper level index.json to do this - DynamoDB
