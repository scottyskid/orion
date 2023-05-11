#!/usr/bin/env python3

import aws_cdk as cdk

from pocket_masters.pocket_masters_stack import PocketMastersStack


app = cdk.App()
PocketMastersStack(app, "pocket-masters")

app.synth()
