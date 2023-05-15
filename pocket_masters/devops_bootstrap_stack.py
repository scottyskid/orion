"""Stack for deploying Code* pipelines to an AWS Account"""

from constructs import Construct
from aws_cdk import (
    Stack,
    aws_codecommit as codecommit,
)
class DevopsBootstrapStack(Stack):
    """Stack for deploying Code* pipelines to an AWS Account

    Args:
        Stack (cdk.Stack): the stack class
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        codecommit.Repository(self, "PocketMastersRepo", repository_name="PocketMastersRepo")

