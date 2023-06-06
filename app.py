#!/usr/bin/env python3
"""Root cdk app file
"""

import os
from pathlib import Path

import aws_cdk as cdk
from aws_cdk import Tags

from config.env.alpha import ConfigEnvAlpha
from config.env.pipeline import ConfigEnvPipeline
from config.root import ConfigRoot
from orion.app_stage import AppStage
from orion.deployment_pipeline_stack import DeploymentPipelineStack

ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

# TODO add project wide tags
app = cdk.App()

Tags.of(app).add("ccx:project:name", "orion")

# Build main deployment pipeline
config = ConfigRoot(env=ConfigEnvPipeline(), root_dir=ROOT_DIR)
env = cdk.Environment(account=config.env.account, region=config.env.region)
deploymen_pipeline_stack = DeploymentPipelineStack(
    app,
    f"OrionDeploymentPipeline",
    config,
    env=env,
)
for key, value in config.project_tags.items():
    Tags.of(deploymen_pipeline_stack).add(key, value)


# A Stage is used to deploy stacks to different environments
# It allows for the synthing of all cdk code at once with the ability to deploy each at different times

# Deploy Alpha stage
config = ConfigRoot(env=ConfigEnvAlpha(), root_dir=ROOT_DIR)
env = cdk.Environment(account=config.env.account, region=config.env.region)
apha_stage = AppStage(
    app,
    f"OrionApp{config.env.descriminator}",
    config,
    env=env,
)
for key, value in config.project_tags.items():
    Tags.of(apha_stage).add(key, value)
Tags.of(apha_stage).add("ccx:project:stage", "alpha")


app.synth()
