import os
import boto3

#TODO Add logging from lambda power tools (JSON?)
def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    print(event)
    #FIXME strip trailing '/' from path
    s3_object = s3.Object(bucket_name=os.environ['DATA_BUCKET'], 
                          key=f"{os.environ['DATA_KEY_BASE']}{event['path']}/index.json")
    body = s3_object.get()['Body'].read()

    #TODO Add environment variables json for local deployment 

    #TODO Raise 404 on missing file
    
    #TODO parse in full url at call time

    #TODO pagenation and multiple calls

    #TODO allow searching for name i can use the index in the upper level index.json to do this

    #TODO implement https://docs.aws.amazon.com/apigateway/latest/developerguide/integrating-api-with-aws-services-s3.html
    response = {
      'statusCode': 200,
      'headers': {
        'Content-Type': 'application/json'
      },
      'isBase64Encoded': False,
      'body': body
    }

    return response