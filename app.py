#!/usr/bin/env python3
"""Root cdk app file
"""

import os
from pathlib import Path

import aws_cdk as cdk

from orion.app_stage import AppStage
from orion.deployment_pipeline_stack import DeploymentPipelineStack
from config.config_dataclass import Config, ConfigEnvSpecificDev

ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

config = Config(env=ConfigEnvSpecificDev(), root_dir = ROOT_DIR)

app = cdk.App()

env = cdk.Environment(account=config.env.account, region=config.env.region)

DeploymentPipelineStack(app, f'OrionDeploymentPipeline{config.env.descriminator}', config, env=env)
AppStage(app, f'OrionApp{config.env.descriminator}', config, env=env)

app.synth()
