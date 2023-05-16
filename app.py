#!/usr/bin/env python3
"""Root cdk app file
"""

import os

import aws_cdk as cdk

from orion.app_stage import AppStage
from orion.deployment_pipeline_stack import DeploymentPipelineStack

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

app = cdk.App()

DeploymentPipelineStack(app, "OrionDeploymentPipeline")
AppStage(app, "OrionApp")

app.synth()
