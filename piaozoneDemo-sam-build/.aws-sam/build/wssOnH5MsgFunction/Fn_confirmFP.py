import json
import boto3
import base64

def lambda_handler(event, context):
    # TODO implement
    inputdata = json.loads(base64.b64decode(event['body']).decode('ascii'))
    userid = inputdata['userid']
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('piaozone')
    
    response = table.get_item(Key={'userid': userid})
    tt = response["Item"]["taskToken"]
    print(tt)
    client = boto3.client('stepfunctions')
    client.send_task_success(
        taskToken=tt,
        output=json.dumps({ "decision":inputdata["decision"] })
    )
  
    return {
        'item': userid
    }
