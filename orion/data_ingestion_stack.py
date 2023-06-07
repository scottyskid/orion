"""Stack for ingesting data
"""
import typing

from aws_cdk import Duration, Stack
from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecr_assets as ecr_assets
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_lambda_python_alpha as lambda_python
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_stepfunctions as sfn
from aws_cdk import aws_stepfunctions_tasks as sfn_tasks
from aws_cdk import custom_resources as cr
from constructs import Construct

from config.root import ConfigRoot


class DataIngestionStack(Stack):
    """Stack for ingesting data"""

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        config: ConfigRoot,
        vpc: ec2.IVpc,
        **kwargs: typing.Any,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        """ Data ingestion stack constructor
        """
        self.scope = scope
        self.construct_id = construct_id
        self.config = config
        self.vpc = vpc

        # ---------- Statemachine start point ----------
        self.start_state = sfn.Pass(self, "StartState")

        # ---------- Get Source Data ----------
        self.build_landing_bucket()
        sfn_task_pokeapi_source_download = self.build_sfn_task_pokeapi_download_source()

        self.start_state.next(sfn_task_pokeapi_source_download)

        # ---------- Populate DynamoDB ----------

        self.build_sfn_task_populate_dynamodb_tables()

        # ---------- Build State Machine ----------
        self.build_state_machine()

    def build_landing_bucket(self) -> None:
        """Build landing bucket"""
        # Pokeapi data landing bucket
        # S3 data landing bucket
        self.landing_bucket = s3.Bucket(
            self,
            "LandingBucket",
            removal_policy=self.config.env.removal_policy,
            auto_delete_objects=self.config.env.delete_objects,
        )

    def build_sfn_task_pokeapi_download_source(self) -> sfn_tasks.EcsRunTask:
        # ---------- Get data from Pokeapi ----------
        container_name = "pokeapi_data_upload"
        container = ecr_assets.DockerImageAsset(
            self,
            "Container",
            directory=str(self.config.root_dir / "containers" / container_name),
        )

        cluster: ecs.Cluster = ecs.Cluster(
            self, "Cluster", vpc=self.vpc, container_insights=True
        )

        task_definition: ecs.FargateTaskDefinition = ecs.FargateTaskDefinition(
            self,
            "TaskDefinition",
            cpu=self.config.data_ingestion.container_cpu,
            memory_limit_mib=self.config.data_ingestion.container_memory,
        )

        task_definition.add_container(
            "TaskDefinitionContainer",
            image=ecs.ContainerImage.from_docker_image_asset(container),
            environment={
                "S3_URI": self.landing_bucket.s3_url_for_object(
                    self.config.api.pokeapi_data_s3_key
                )
            },
            logging=ecs.LogDriver.aws_logs(
                stream_prefix=f"/ecs/data-ingestion/{container_name}"
            ),
        )

        self.landing_bucket.grant_read_write(task_definition.task_role)

        # TODO add wait for completion step
        self.sfn_task_pokeapi_source_download: sfn_tasks.EcsRunTask = (
            sfn_tasks.EcsRunTask(
                self,
                "RunTask",
                cluster=cluster,
                launch_target=sfn_tasks.EcsFargateLaunchTarget(
                    platform_version=ecs.FargatePlatformVersion.LATEST
                ),
                task_definition=task_definition,
                propagated_tag_source=ecs.PropagatedTagSource.TASK_DEFINITION,
            )
        )

        return self.sfn_task_pokeapi_source_download

    def build_sfn_task_populate_dynamodb_tables(self) -> None:
        category_table: dynamodb.Table = dynamodb.Table(
            self,
            "CategoryTable",
            partition_key=dynamodb.Attribute(
                name="category", type=dynamodb.AttributeType.STRING
            ),
            removal_policy=self.config.env.removal_policy,
        )

        item_table: dynamodb.Table = dynamodb.Table(
            self,
            "ItemTable",
            partition_key=dynamodb.Attribute(
                name="category", type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.NUMBER),
            removal_policy=self.config.env.removal_policy,
        )

        pokeapi_to_dynamodb_lambda: lambda_python.PythonFunction = (
            lambda_python.PythonFunction(
                self,
                "PokeapiToDynamodbFunction",
                entry=str(
                    self.config.root_dir
                    / "lambdas"
                    / "data_ingestion"
                    / "pokeapi_to_dynamodb"
                ),
                index="index.py",
                handler="lambda_handler",
                runtime=lambda_.Runtime.PYTHON_3_10,
                environment={
                    "DATA_BUCKET": self.landing_bucket.bucket_name,
                    "DATA_KEY_BASE": self.config.api.pokeapi_data_s3_key,
                    "TABLE_NAME_CATEGORY": category_table.table_name,
                    "TABLE_NAME_ITEMS": item_table.table_name,
                },
                timeout=Duration.minutes(1),
            )
        )

        self.landing_bucket.grant_read(pokeapi_to_dynamodb_lambda)

    def build_state_machine(self) -> sfn.StateMachine:
        """Build state machine"""
        self.state_machine = sfn.StateMachine(
            self, "StateMachine", definition=self.start_state
        )

        # Custom Resource to run Data Ingestion State Machine on deploy
        start_execution_sdk_call = cr.AwsSdkCall(
            action="startExecution",
            service="StepFunctions",
            parameters={"stateMachineArn": self.state_machine.state_machine_arn},
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

        self.state_machine.grant_start_execution(start_state_machine_cr)

        return self.state_machine
