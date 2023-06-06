"""Stack for ingesting data
"""
from aws_cdk import Stack
from aws_cdk import aws_ecr_assets as ecr_assets
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_stepfunctions as sfn
from aws_cdk import aws_stepfunctions_tasks as sfn_tasks
from aws_cdk import custom_resources as cr
from constructs import Construct


class DataIngestionStack(Stack):
    """Stack for ingesting data"""

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        config,
        vpc,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # S3 data landing bucket
        data_bucket = s3.Bucket(
            self,
            "LandingBucket",
            removal_policy=config.env.removal_policy,
            auto_delete_objects=config.env.delete_objects,
        )

        self.landing_bucket = data_bucket

        start_state = sfn.Pass(self, "StartState")

        container_name = "pokeapi_data_upload"
        container = ecr_assets.DockerImageAsset(
            self,
            "Container",
            directory=str(config.root_dir / "containers" / container_name),
        )

        cluster = ecs.Cluster(self, "Cluster", vpc=vpc, container_insights=True)

        task_definition = ecs.FargateTaskDefinition(
            self,
            "TaskDefinition",
            cpu=16384,
            memory_limit_mib=32768,
        )

        task_definition.add_container(
            "TaskDefinitionContainer",
            image=ecs.ContainerImage.from_docker_image_asset(container),
            environment={
                "S3_URI": data_bucket.s3_url_for_object(config.api.pokeapi_data_s3_key)
            },
            logging=ecs.LogDriver.aws_logs(
                stream_prefix=f"/ecs/data-ingestion/{container_name}"
            ),
        )

        data_bucket.grant_read_write(task_definition.task_role)

        # TODO add wait for completion step
        run_task = sfn_tasks.EcsRunTask(
            self,
            "RunTask",
            cluster=cluster,
            launch_target=sfn_tasks.EcsFargateLaunchTarget(
                platform_version=ecs.FargatePlatformVersion.LATEST
            ),
            task_definition=task_definition,
            propagated_tag_source=ecs.PropagatedTagSource.TASK_DEFINITION,
        )

        start_state.next(run_task)

        state_machine = sfn.StateMachine(self, "StateMachine", definition=start_state)

        # Custom Resource to run Data Ingestion State Machine on deploy
        start_execution_sdk_call = cr.AwsSdkCall(
            action="startExecution",
            service="StepFunctions",
            parameters={"stateMachineArn": state_machine.state_machine_arn},
            physical_resource_id=cr.PhysicalResourceId.of("StartDataIngestion"),
        )

        start_state_machine_cr = cr.AwsCustomResource(
            self,
            "StartDataIngestion",
            on_create=start_execution_sdk_call,
            policy=cr.AwsCustomResourcePolicy.from_sdk_calls(
                resources=cr.AwsCustomResourcePolicy.ANY_RESOURCE
            ),
        )

        state_machine.grant_start_execution(start_state_machine_cr)
