"""Stack for injesting data
"""
from constructs import Construct
from aws_cdk import (
    Stack,
    aws_ecr_assets as ecr_assets,
    aws_ecs as ecs,
    aws_lambda_python_alpha as lambda_python,
    aws_s3 as s3,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as sfn_tasks,
)


class DataInjestionStack(Stack):
    """Stack for injesting data
    """

    def __init__(self, scope: Construct, construct_id: str, config, vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # S3 data landing bucket
        data_bucket = s3.Bucket(self, 'LandingBucket',
            removal_policy=config.removal_policy)

        start_state = sfn.Pass(self, 'StartState')
        
        container_name = "pokeapi_data_upload"
        container = ecr_assets.DockerImageAsset(self, 'Container',
                                                directory=str(config.root_dir / 'containers' / container_name),
                                                )
        
        cluster = ecs.Cluster(self, 'Cluster',
                              vpc=vpc)

        task_definition = ecs.FargateTaskDefinition(self, 'TaskDefinition')
        task_definition.add_container('TaskDefinitionContainer',
                                      image=ecs.ContainerImage.from_docker_image_asset(container),
                                      environment={"S3_URI": data_bucket.s3_url_for_object('pokeapi_data_upload')},
                                      logging=ecs.LogDriver.aws_logs(stream_prefix=f"/ecs/data-injestion/{container_name}"))

        data_bucket.grant_read_write(task_definition.task_role)

        run_task = sfn_tasks.EcsRunTask(self, 'RunTask',
                                        cluster=cluster,
                                        launch_target=sfn_tasks.EcsFargateLaunchTarget(platform_version=ecs.FargatePlatformVersion.LATEST),
                                        task_definition=task_definition)
        
        
        start_state.next(run_task)
        state_machine = sfn.StateMachine(self, 'StateMachine', definition=start_state)
