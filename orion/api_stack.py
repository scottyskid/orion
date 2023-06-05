"""Core API Stack
"""
from os import path

from constructs import Construct
from aws_cdk import Duration
from aws_cdk import Stack
from aws_cdk import Tags
from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_lambda_python_alpha as lambda_python


class ApiStack(Stack):
    """Core API Stack
    """

    def __init__(self, scope: Construct, construct_id: str, config, data_bucket, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        Tags.of(self).add('ccx:project:subgroup', 'orion-api')

        api = apigateway.RestApi(self, 'RestApi', rest_api_name='OrionRestApi')

        # powertools_layer = lambda_.LayerVersion.from_layer_version_arn(self, 'LambdaPowertoolsLayer', config.api.lambda_powertools_layer_arn.format(aws_region=self.region))

        root_method = lambda_python.PythonFunction(self, 'ApiRootFunction',
            entry=str(config.root_dir / 'lambdas' / 'api' / 'root'),
            index='index.py',
            handler='lambda_handler',
            runtime=lambda_.Runtime.PYTHON_3_10,
            timeout=Duration.minutes(1),
        )

        api.root.add_method('GET', apigateway.LambdaIntegration(root_method))

        endpoint_resource = api.root.add_resource('api').add_resource('{api_route+}')

        pokeapi_method = lambda_python.PythonFunction(self, 'ApiPokeFunction',
            entry=str(config.root_dir / 'lambdas' / 'api' / 'pokeapi'),
            index='index.py',
            handler='lambda_handler',
            runtime=lambda_.Runtime.PYTHON_3_10,
            environment={'DATA_BUCKET': data_bucket.bucket_name, 'DATA_KEY_BASE': config.api.pokeapi_data_s3_key},
            timeout=Duration.minutes(1),
        )

        data_bucket.grant_read(pokeapi_method)
        
        endpoint_resource.add_method('GET', apigateway.LambdaIntegration(pokeapi_method))

