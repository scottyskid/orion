#!/usr/bin/env python3
"""Root cdk app file
"""

import aws_cdk as cdk

from pocket_masters.pocket_masters_stack import PocketMastersStack
from pocket_masters.devops_bootstrap_stack import DevopsBootstrapStack


app = cdk.App()
PocketMastersStack(app, "pocket-masters")
DevopsBootstrapStack(app, "devops-bootstrap")

app.synth()
