#!/usr/bin/env python3
"""Root cdk app file
"""

import os

import aws_cdk as cdk

from pocket_masters.pocket_masters_api_stack import PocketMastersApiStack
from pocket_masters.devops_bootstrap_stack import DevopsBootstrapStack

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

app = cdk.App()

DevopsBootstrapStack(app, "devops-bootstrap")
PocketMastersApiStack(app, "pocket-masters-api")

app.synth()
