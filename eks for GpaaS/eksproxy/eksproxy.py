import json
import base64
import boto3
import re
from botocore.signers import RequestSigner
from kubernetes import client


def get_bearer_token(cluster_id, region):
    STS_TOKEN_EXPIRES_IN = 60
    session = boto3.session.Session(aws_access_key_id="Axxxxx", aws_secret_access_key="yixxxxxxxxxxxxxx")

    client = session.client('sts', region_name=region)
    service_id = client.meta.service_model.service_id

    signer = RequestSigner(
        service_id,
        region,
        'sts',
        'v4',
        session.get_credentials(),
        session.events
    )

    params = {
        'method': 'GET',
        'url': 'https://sts.{}.amazonaws.com.cn/?Action=GetCallerIdentity&Version=2011-06-15'.format(region),
        'body': {},
        'headers': {
            'x-k8s-aws-id': cluster_id
        },
        'context': {}
    }

    signed_url = signer.generate_presigned_url(
        params,
        region_name=region,
        expires_in=STS_TOKEN_EXPIRES_IN,
        operation_name=''
    )

    base64_url = base64.urlsafe_b64encode(signed_url.encode('utf-8')).decode('utf-8')
    return 'k8s-aws-v1.' + re.sub(r'=*', '', base64_url)

def lambda_handler(event, context):
    aToken = get_bearer_token('kingdee', 'cn-northwest-1')
    aConfiguration = client.Configuration()
    aConfiguration.debug = True

    # Specify the endpoint of your Kube cluster
    aConfiguration.host = "https://75058F83314822F453FC876071B20E13.gr7.cn-northwest-1.eks.amazonaws.com.cn:443"

    
    aConfiguration.verify_ssl = False
    

    aConfiguration.api_key = {"authorization": "Bearer " + aToken}

    # Create a ApiClient with our config
    aApiClient = client.ApiClient(aConfiguration)

    # Do calls
    v1 = client.CoreV1Api(aApiClient)
    print("Listing pods with their IPs:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        print("%s\t%s\t%s" %
              (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
   
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
