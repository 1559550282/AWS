import boto3
import os
import time
from botocore.exceptions import ClientError
import urllib
import json

print('Loading function')
#sfnArn = os.environ['sfnarn']
sfnArn = "arn:aws:states:eu-west-1:955513527673:activity:ageCheck"
    
sfClient = boto3.client('stepfunctions')

outputstring = "{\"type\":\"adult\",\"message\":\"allowed\"}"

while 0<1:
  response = sfClient.get_activity_task(activityArn=sfnArn, workerName='abc')
  task_token, input_ = response['taskToken'], response['input']
  params = json.loads(input_) 
  if task_token is None: 
    time.sleep(5)
  else:
    age = params.get('age')
    workflow = params.get('workflow')
    if age<18:
      print("%s: age %d is under 18, forbidden!" % (workflow, age))
      sfClient.send_task_failure(
        taskToken=task_token,
        error='age check failed',
        cause='child under 18 is not allowed!') 
    else:
      print("%s: age %d is more than 18, allowed!" % (workflow, age))
      sfClient.send_task_success(
        taskToken=task_token,
        output=outputstring)

