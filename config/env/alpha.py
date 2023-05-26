
from dataclasses import dataclass

from aws_cdk import RemovalPolicy

from config.env import base

@dataclass(frozen=True, kw_only=True)
class ConfigEnvAlpha(base.ConfigEnvBase):
    """A dataclass containing config for a specific environment
    """
    account: str = '578994453819'
    region: str = 'ap-southeast-2'
    name: str = 'alpha'
    removal_policy: RemovalPolicy = RemovalPolicy.DESTROY
    delete_objects: bool = True