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


app = cdk.App()


config = Config(env=ConfigEnvSpecificDev(), root_dir = ROOT_DIR)
env = cdk.Environment(account=config.env.account, region=config.env.region)

#TODO add project wide tags
DeploymentPipelineStack(app, f'OrionDeploymentPipeline', config, env=env)

# A Stage is used to deploy stacks to different environments
# It allows for the synthing of all cdk code at once with the ability to deploy each at different times
AppStage(app, f'OrionApp', config, env=env)

app.synth()
