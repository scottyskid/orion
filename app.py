#!/usr/bin/env python3
"""Root cdk app file
"""

import os

import aws_cdk as cdk

from orion.orion_api_stage import OrionApiStage
from orion.orion_devops_bootstrap_stack import OrionDevopsBootstrapStack

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

app = cdk.App()

OrionDevopsBootstrapStack(app, "orion-devops-bootstrap")
OrionApiStage(app, "orion-api-stage")

app.synth()
