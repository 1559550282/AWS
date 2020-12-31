import json
import boto3
from botocore.exceptions import ClientError

apiEndPointUrl_erp = "https://mkhp953pk8.execute-api.us-east-2.amazonaws.com/production"
apiEndPointUrl_h5 = "https://8yovrv2opk.execute-api.us-east-2.amazonaws.com/production"

def lambda_handler(event, context):
    # TODO implement
    print(event)
    print(event['body'])
    erpconnectid = None
    h5connectid = None
    
    #获取连接的connectionid
    connectionId = event['requestContext']['connectionId']
    msgBody = json.loads(event['body'])  ##注意这里body是‘’的string，需要json.loads转化
    userid = msgBody['userid']
    clientType = msgBody['clientType']
   
    if clientType == 'ERP':
        apiEndPointUrl = apiEndPointUrl_erp
        erpconnid = connectionId
        #h5connid = None
    if clientType == 'H5':
        apiEndPointUrl = apiEndPointUrl_h5
        #erpconnid = None
        h5connid = connectionId    
    apiClient = boto3.client('apigatewaymanagementapi', endpoint_url=apiEndPointUrl)    
    
        # TODO: write code...
    
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
            UpdateExpression="set erpconnectid = :erpconnidVal, h5connectid= :h5connidVal",
            ExpressionAttributeValues={':erpconnidVal' : erpconnid, ':h5connidVal': h5connid}
        )
    except ClientError as ce : 
        if ce.response['Error']['Code'] == 'ConditionalCheckFailedException':
            table.put_item(
                Item={
                        'userid':userid,
                        'erpconnectid':erpconnid,
                        'h5connectid':h5connid
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
