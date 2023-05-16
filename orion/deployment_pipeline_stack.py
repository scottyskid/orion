"""Stack for deploying Code* pipelines to an AWS Account"""

from constructs import Construct
from aws_cdk import Stack
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep
from aws_cdk.aws_codestarconnections import CfnConnection

from orion.app_stage import AppStage


class DeploymentPipelineStack(Stack):
    """Stack for deploying Code* pipelines to an AWS Account

    Args:
        Stack (cdk.Stack): the stack class
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        connection = CfnConnection(self, "RepoConnection", connection_name="OrionRepoConnection", provider_type="GitHub")

        pipeline =  CodePipeline(self, "CdkPipeline",
                        pipeline_name="OrionCdkPipeline",
                        synth=ShellStep("Synth",
                            input=CodePipelineSource.connection("scottyskid/orion", "main", connection_arn=connection.attr_connection_arn),
                            commands=["npm install -g aws-cdk",
                                "python -m pip install -r requirements.txt",
                                "cdk synth"]
                        )
                    )
        
        pipeline.add_stage(AppStage(self, "OrionApp"))
