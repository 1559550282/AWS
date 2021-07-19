import json
import boto3
import base64
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    print(event)
    uuid = event["key1"]
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('galaxydb')
    
    #检查处理状态
    response = table.get_item( Key={
            'uuid': uuid
        }
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps(response['Item'].get('userid'))
    }

