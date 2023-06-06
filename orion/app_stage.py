"""Stage containing all stacks for the api app"""

from aws_cdk import Stage
from constructs import Construct

from orion.api_stack import ApiStack
from orion.data_ingestion_stack import DataIngestionStack
from orion.network_stack import NetworkStack


class AppStage(Stage):
    """Stage containing all stacks for the api app

    Args:
        Stage (cdk.Stage): the stage
    """

    def __init__(self, scope: Construct, construct_id: str, config, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        network = NetworkStack(self, "Network", config)
        data_ingestion = DataIngestionStack(self, "DataIngestion", config, network.vpc)
        ApiStack(self, "Api", config, data_ingestion.landing_bucket)
