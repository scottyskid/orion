import os
from pathlib import Path

import aws_cdk as core
import aws_cdk.assertions as assertions

from orion.api_stack import ApiStack
from config.root import Config

ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent.parent
config = Config(root_dir=ROOT_DIR)

def test_sqs_queue_created():
    app = core.App()
    stack = ApiStack(app, 'orion', config)
    template = assertions.Template.from_stack(stack)

    # template.has_resource_properties('AWS::SQS::Queue', {
    #     'VisibilityTimeout': 300
    # })


def test_sns_topic_created():
    app = core.App()
    stack = ApiStack(app, 'orion', config)
    template = assertions.Template.from_stack(stack)

    # template.resource_count_is('AWS::SNS::Topic', 1)
