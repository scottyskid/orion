"""Core API Stack
"""
from os import path

from constructs import Construct
from aws_cdk import (
    Stack,
    aws_apigateway as apigateway,
    aws_lambda as lambda_,
)


class OrionApiStack(Stack):
    """Core API Stack
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        api = apigateway.RestApi(self, "OrionApi", rest_api_name="OrionApi")

        root_method = lambda_.Function(self, "ApiMethodFunction",
            code=lambda_.Code.from_asset(path.join("lambdas", "api")),
            handler="root.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_10
        )
        
        api.root.add_method("GET", apigateway.LambdaIntegration(root_method))
