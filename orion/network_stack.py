

from constructs import Construct
from aws_cdk import Stack
from aws_cdk import aws_ec2 as ec2


class NetworkStack(Stack):
    """Stack for injesting data
    """

    def __init__(self, scope: Construct, construct_id: str, config, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = ec2.Vpc(self, "AppVpc",
                           ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/16"),
                           max_azs=3
                           )
        
                           


