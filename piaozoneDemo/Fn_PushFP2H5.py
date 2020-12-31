import json
import boto3

apiEndPointUrl = "https://8yovrv2opk.execute-api.us-east-2.amazonaws.com/production"
apiClient = boto3.client('apigatewaymanagementapi', endpoint_url=apiEndPointUrl)

def lambda_handler(event, context):
    # TODO implement
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('piaozone')
    print(event)
    userid = event["userid"]
    response = table.get_item( Key={
            'userid': userid
        }
    )
    print(response)
    fapiao = response['Item'].get('FapiaoInfo', 'Please upload new Fapiao')
    print(fapiao)
    connectionId = response['Item']['h5connectid']
    #信息回传
    print(connectionId)
    #fp="{'fapiao':{'name':'sharon','amount':'79.3'}}"
    response = apiClient.post_to_connection(
        Data=f'Fapio Info: {fapiao}'.encode('ascii'),
        ConnectionId=connectionId
    )
    
    
    return {
        "userid":userid
    }
