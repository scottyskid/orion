from dataclasses import dataclass, field

from aws_cdk import RemovalPolicy


@dataclass(frozen=True, kw_only=True)
class ConfigEnvBase:
    """A dataclass containing config for a specific environment"""

    account: str
    region: str
    name: str
    descriminator: str = field(init=False)
    removal_policy: RemovalPolicy = RemovalPolicy.RETAIN
    delete_objects: bool = False

    def __post_init__(self):
        # has to be set this way due to dataclasses.FrozenInstanceError raised if set directly
        object.__setattr__(self, "descriminator", self.name.capitalize())
