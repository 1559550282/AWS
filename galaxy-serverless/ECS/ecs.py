import boto3
import os
#import time
#from botocore.exceptions import ClientError
#import urllib
import json

username = os.environ['MY_USER']
password = os.environ['MY_PASS']
tt = os.environ['MY_TASK_TOKEN']
print("Running with user: %s" % username)
print("Running with password: %s" % password)
print("Running with task token: %s" % tt)

client = boto3.client('stepfunctions',aws_access_key_id="xxxxxxx",aws_secret_access_key="xxxxxxxxx")
client.send_task_success(
        taskToken=tt,
        output=json.dumps({ "decision":"true"})
    )
