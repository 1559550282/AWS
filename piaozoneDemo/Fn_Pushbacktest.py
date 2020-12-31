import json
import boto3

#TODO: 将相关变量转换为Lambda环境变量或是存储在Parameter Store
apiEndPointUrl = "https://mkhp953pk8.execute-api.us-east-2.amazonaws.com/production"
apiClient = boto3.client('apigatewaymanagementapi', endpoint_url=apiEndPointUrl)

ddbTableName = 'piaozone'
ddbClient = boto3.client('dynamodb')

def lambda_handler(event, context):
    # TODO implement
    response = ddbClient.get_item(
        TableName=ddbTableName,
        Key={
            'userid' : {'S':'001'}
        }
            
        )
    connectionId = response['Item']['ERP']['M']['connectid']['S']
    print(connectionId)
    fp="{'fapiao':{'name':'sharon','amount':'79.3'}}"
    response = apiClient.post_to_connection(
        Data=f'Fapio Info: {fp}'.encode('ascii'),
        ConnectionId=connectionId
    )
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
