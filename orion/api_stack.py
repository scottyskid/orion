"""Core API Stack
"""
from os import path

from constructs import Construct
from aws_cdk import Stack
from aws_cdk import Tags
from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_lambda as lambda_


class ApiStack(Stack):
    """Core API Stack
    """

    def __init__(self, scope: Construct, construct_id: str, config, data_bucket, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        Tags.of(self).add('ccx:project:subgroup', 'orion-api')

        api = apigateway.RestApi(self, 'RestApi', rest_api_name='OrionRestApi')

        powertools_layer = lambda_.LayerVersion.from_layer_version_arn(self, 'LambdaPowertoolsLayer', config.api.lambda_powertools_layer_arn.format(aws_region=self.region))

        root_method = lambda_.Function(self, 'ApiRootFunction',
            code=lambda_.Code.from_asset(str(config.root_dir / 'lambdas' / 'api' / 'root')),
            handler='index.lambda_handler',
            runtime=lambda_.Runtime.PYTHON_3_10,
            layers=[powertools_layer],
        )

        api.root.add_method('GET', apigateway.LambdaIntegration(root_method))

        endpoint_resource = api.root.add_resource('api').add_resource('{api_route+}')

        pokeapi_method = lambda_.Function(self, 'ApiPokeFunction',
            code=lambda_.Code.from_asset(str(config.root_dir / 'lambdas' / 'api' / 'pokeapi')),
            handler='index.lambda_handler',
            runtime=lambda_.Runtime.PYTHON_3_10,
            environment={'DATA_BUCKET': data_bucket.bucket_name, 'DATA_KEY_BASE': config.api.pokeapi_data_s3_key},
            layers=[powertools_layer],
        )

        data_bucket.grant_read(pokeapi_method)
        
        endpoint_resource.add_method('GET', apigateway.LambdaIntegration(pokeapi_method))

