"""Stage containing all stacks for the api app"""

from constructs import Construct
from aws_cdk import (
    Stage,
)

from orion.orion_api_stack import OrionApiStack

class OrionApiStage(Stage):
    """Stage containing all stacks for the api app

    Args:
        Stage (cdk.Stage): the stage
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        api = OrionApiStack(self, "orion-api")



