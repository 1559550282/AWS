import json
import boto3
from botocore.exceptions import ClientError

#apiEndPointUrl = "https://mkhp953pk8.execute-api.us-east-2.amazonaws.com/production"
#apiEndPointUrl_h5 = "https://8yovrv2opk.execute-api.us-east-2.amazonaws.com/production"

def lambda_handler(event, context):
    # TODO implement
    print(event)
    print(event['body'])
    apiEndPointUrl = "https://" + event['requestContext']['domainName'] + '/' + event['requestContext']['stage']
    print(apiEndPointUrl)
    #获取连接的connectionid
    connectionId = event['requestContext']['connectionId']
    msgBody = json.loads(event['body'])  ##注意这里body是‘’的string，需要json.loads转化
    userid = msgBody['userid']
    clientType = msgBody['clientType']
   
    apiClient = boto3.client('apigatewaymanagementapi', endpoint_url=apiEndPointUrl)    
    
    print('userid: {} at ConnectionId: {} from {}'.format(userid, connectionId, clientType))
    
    #将ClientId和对应类型的ConnectionID写入DDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('piaozone')
    
    #找到对应的user即update connectionID,否则修改对应的值
    try :
        response = table.update_item(
            Key={
                    'userid':userid,
                },
            UpdateExpression="set erpconnectid = :erpconnidVal",
            ExpressionAttributeValues={':erpconnidVal' : connectionId}
        )
    except ClientError as ce : 
        if ce.response['Error']['Code'] == 'ConditionalCheckFailedException':
            table.put_item(
                Item={
                        'userid':userid,
                        'erpconnectid':erpconnid
                    })
        
    #检查是否有历史发票，如有则发回历史信息
    response = table.get_item( Key={
            'userid': userid
        }
    )
    fapiao = response['Item'].get('FapiaoInfo', 'Please upload new Fapiao')
    
    #信息回传
    print(connectionId)
    #fp="{'fapiao':{'name':'sharon','amount':'79.3'}}"
    response = apiClient.post_to_connection(
        Data=f'Fapio Info: {fapiao}'.encode('ascii'),
        ConnectionId=connectionId
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
