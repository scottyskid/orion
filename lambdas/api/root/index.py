def lambda_handler(event, context):
    response = {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "isBase64Encoded": False,
        "multiValueHeaders": {
            "X-Custom-Header": ["My value", "My other value"],
        },
        "body": "{\n  'TotalCodeSize': 104330022,\n  'FunctionCount': 7\n}",
    }

    return response
