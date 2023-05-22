"""Core API Stack
"""
from os import path

from constructs import Construct
from aws_cdk import Stack
from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_lambda as lambda_


class ApiStack(Stack):
    """Core API Stack
    """

    def __init__(self, scope: Construct, construct_id: str, config, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        api = apigateway.RestApi(self, "RestApi", rest_api_name="OrionRestApi")

        root_method = lambda_.Function(self, "ApiRootFunction",
            code=lambda_.Code.from_asset(path.join("lambdas", "api")),
            handler="root.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_10
        )
        
        api.root.add_method("GET", apigateway.LambdaIntegration(root_method))
