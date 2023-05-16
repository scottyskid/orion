"""Stage containing all stacks for the api app"""

from constructs import Construct
from aws_cdk import Stage

from orion.api_stack import ApiStack

class AppStage(Stage):
    """Stage containing all stacks for the api app

    Args:
        Stage (cdk.Stage): the stage
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        api = ApiStack(self, "Api")



