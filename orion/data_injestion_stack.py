"""Stack for injesting data
"""
from os import path

from constructs import Construct
from aws_cdk import Stack
from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_ecr as ecr
from aws_cdk import aws_ecr_assets as ecr_assets
from aws_cdk import aws_ecs as ecs
from aws_cdk.aws_lambda_python_alpha import PythonFunction
from aws_cdk import aws_s3 as s3


class DataInjestionStack(Stack):
    """Stack for injesting data
    """

    def __init__(self, scope: Construct, construct_id: str, config, vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # lambda_dir = config.root_dir / 'lambdas'
        
        # # Build python lambda function 
        # function = aws_lambda_python.PythonFunction(self, 'DataInjestionFunction',
        #     entry=lambda_dir / 'data_injestion_function',

        # )

        # S3 data landing bucket
        s3_bucket = s3.Bucket(self, 'LandingBucket',
            removal_policy=config.removal_policy)

        # container_repo = ecr.Repository(self, 'ContainerRepo',
        #                                 auto_delete_images=True,
        #                                 removal_policy=config.removal_policy,
        #                                 )
        
        container = ecr_assets.DockerImageAsset(self, 'Container',
                                                directory=str(config.root_dir / 'containers' / 'pokeapi_data_upload'))
        
        cluster = ecs.Cluster(self, 'Cluster', vpc=vpc)
        
        task_definition = ecs.FargateTaskDefinition(self, 'TaskDefinition')
        task_definition.add_container('TaskDefinitionContainer', image=ecs.ContainerImage.from_docker_image_asset(container),
                                      )
        
        
        




