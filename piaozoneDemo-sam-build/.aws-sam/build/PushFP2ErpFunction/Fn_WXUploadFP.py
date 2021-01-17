import json
import boto3
import uuid
import base64
import os

theStateMachineArn = os.environ['APPLICATION_PROCESSING_STEP_FUNCTION_ARN']
print(theStateMachineArn)
def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('piaozone')
    print(event)
    
    inputdata =json.loads(base64.b64decode(event['body']).decode('ascii')) 
    print(inputdata)
    
    response = table.update_item(
        Key={
            'userid': inputdata['userid']
        },
        UpdateExpression="set FapiaoInfo = :r",
        ExpressionAttributeValues={
            ':r': inputdata['FapiaoInfo']
        }
    )
    
    
    appname="appid_" + str(uuid.uuid1())
    inputdata["appid"]=appname
    inputparam = inputdata
    
    sfn = boto3.client('stepfunctions')
    response = sfn.start_execution(
    stateMachineArn=theStateMachineArn,
    name=appname ,
    input=json.dumps(inputparam)
    )
    
    return {
        'message' : {'result':'OK'}
    }
