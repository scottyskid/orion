from dataclasses import dataclass, field
from pathlib import Path

from config.env.base import ConfigEnvBase


@dataclass(frozen=True, kw_only=True)
class ConfigApi:
    """A dataclass containing config for the cdk app
    """
    pokeapi_data_s3_key: str = 'pokeapi_data_upload'
    lambda_powertools_layer_arn: str = 'arn:aws:lambda:{aws_region}:017000801446:layer:AWSLambdaPowertoolsPythonV2:32'


@dataclass(frozen=True, kw_only=True)
class ConfigRoot:
    """A dataclass containing config for the cdk app
    """
    env: ConfigEnvBase
    api: ConfigApi = ConfigApi()
    root_dir: Path
    repo_name: str = 'scottyskid/orion' # 'OWNER/REPO'
    repo_branch: str = 'main'
    project_tags: dict = field(default_factory=lambda: {'ccx:project:name': 'orion'})
