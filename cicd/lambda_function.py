import json

def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 208,
        'body': json.dumps('Hello from Lambda!')
    }
