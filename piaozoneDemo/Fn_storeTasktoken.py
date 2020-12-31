import json
import boto3
def lambda_handler(event, context):
    # TODO implement
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('piaozone')
    #table.put_item(Item=event)
    table.update_item(
        Key={
            'userid': event["userid"]
        },
        UpdateExpression='SET taskToken = :val1',
        ExpressionAttributeValues={
            ':val1': event["taskToken"]
        }
    )
    
   # event["userid"]
    #event["id"]
    #event["taskToken"]
    return {
        "message":event
    }
