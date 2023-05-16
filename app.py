#!/usr/bin/env python3
"""Root cdk app file
"""

import os

import aws_cdk as cdk

from orion.orion_api_stack import OrionApiStack
from orion.orion_devops_bootstrap_stack import OrionDevopsBootstrapStack

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

app = cdk.App()

OrionDevopsBootstrapStack(app, "orion-devops-bootstrap")
OrionApiStack(app, "orion-api")

app.synth()
