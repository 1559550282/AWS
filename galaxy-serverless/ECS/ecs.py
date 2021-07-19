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

client = boto3.client('stepfunctions',aws_access_key_id="AKIAUZIAJ42JC6FSTZ6M",aws_secret_access_key="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")
client.send_task_success(
        taskToken=tt,
        output=json.dumps({ "decision":"true"})
    )
