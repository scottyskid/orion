"""Stage containing all stacks for the api app"""

from constructs import Construct
from aws_cdk import Stage

from orion.api_stack import ApiStack
from orion.data_injestion_stack import DataInjestionStack
from orion.network_stack import NetworkStack



class AppStage(Stage):
    """Stage containing all stacks for the api app

    Args:
        Stage (cdk.Stage): the stage
    """

    def __init__(self, scope: Construct, construct_id: str, config, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        network = NetworkStack(self, "Network", config)
        data_injestion = DataInjestionStack(self, "DataInjestion", config, network.vpc)
        api = ApiStack(self, "Api", config)


