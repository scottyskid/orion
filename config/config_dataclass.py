from dataclasses import dataclass, field
from pathlib import Path

from aws_cdk import RemovalPolicy

#TODO split into seperate files
@dataclass(frozen=True, kw_only=True)
class ConfigEnvSpecificBase:
    """A dataclass containing config for a specific environment
    """
    account: str
    region: str
    name: str
    descriminator: str = field(init=False)
    removal_policy: RemovalPolicy = RemovalPolicy.RETAIN

    def __post_init__(self):
        # has to be set this way due to dataclasses.FrozenInstanceError raised if set directly
        object.__setattr__(self, 'descriminator', self.name.capitalize())

@dataclass(frozen=True, kw_only=True)
class ConfigEnvSpecificDev(ConfigEnvSpecificBase):
    """A dataclass containing config for a specific environment
    """
    account: str = '578994453819'
    region: str = 'ap-southeast-2'
    name: str = 'dev'
    removal_policy: RemovalPolicy = RemovalPolicy.DESTROY


@dataclass(frozen=True, kw_only=True)
class ConfigApi:
    """A dataclass containing config for the cdk app
    """
    pokeapi_data_s3_key: str = 'pokeapi_data_upload'

@dataclass(frozen=True, kw_only=True)
class Config:
    """A dataclass containing config for the cdk app
    """
    env: ConfigEnvSpecificBase
    api: ConfigApi = ConfigApi()
    root_dir: Path
    repo_name: str = 'scottyskid/orion' # 'OWNER/REPO'
    repo_branch: str = 'main'
    



