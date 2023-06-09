"""Stack for deploying Code* pipelines to an AWS Account"""
import typing

from aws_cdk import Stack
from aws_cdk import aws_s3 as s3
from aws_cdk.aws_codestarconnections import CfnConnection
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep
from constructs import Construct

from config.root import ConfigRoot
from orion.app_stage import AppStage


class DeploymentPipelineStack(Stack):
    """Stack for deploying Code* pipelines to an AWS Account

    Args:
        Stack (cdk.Stack): the stack class
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        config: ConfigRoot,
        **kwargs: typing.Any,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        artifact_bucket = s3.Bucket(
            self,
            "PipelineArtifactBucket",
            removal_policy=config.env.removal_policy,
            auto_delete_objects=config.env.delete_objects,
        )

        connection = CfnConnection(
            self,
            "RepoConnection",
            connection_name="OrionRepoConnection",
            provider_type="GitHub",
        )

        pipeline = CodePipeline(
            self,
            "CdkPipeline",
            pipeline_name="OrionCdkPipeline",
            synth=ShellStep(
                "Synth",
                input=CodePipelineSource.connection(
                    config.repo_name,
                    config.repo_branch,
                    connection_arn=connection.attr_connection_arn,
                ),
                commands=[
                    "npm install -g aws-cdk",
                    "python -m pip install -r requirements.txt",
                    "cdk synth",
                ],
            ),
            artifact_bucket=artifact_bucket,
        )

        pipeline.add_stage(AppStage(self, "OrionApp", config))
