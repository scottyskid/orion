"""Core API Stack
"""
import typing

from aws_cdk import Duration, Stack, Tags
from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_lambda_python_alpha as lambda_python
from aws_cdk import aws_s3 as s3
from constructs import Construct

from config.root import ConfigRoot


class ApiStack(Stack):
    """Core API Stack"""

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        config: ConfigRoot,
        data_bucket: s3.IBucket,
        **kwargs: typing.Any,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        Tags.of(self).add("ccx:project:subgroup", "orion-api")

        api = apigateway.RestApi(self, "RestApi", rest_api_name="OrionRestApi")

        pokeapi_method = lambda_python.PythonFunction(
            self,
            "ApiPokeFunction",
            entry=str(config.root_dir / "lambdas" / "api" / "pokeapi"),
            index="index.py",
            handler="lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_10,
            environment={
                "DATA_BUCKET": data_bucket.bucket_name,
                "DATA_KEY_BASE": config.api.pokeapi_data_s3_key,
            },
            timeout=Duration.minutes(1),
        )

        data_bucket.grant_read(pokeapi_method)

        api.root.add_method("GET", apigateway.LambdaIntegration(pokeapi_method))

        endpoint_resource = api.root.add_resource("api").add_resource("{api_route+}")

        endpoint_resource.add_method(
            "GET", apigateway.LambdaIntegration(pokeapi_method)
        )
