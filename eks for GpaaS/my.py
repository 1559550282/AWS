import base64
import boto3
import re
from botocore.signers import RequestSigner
from kubernetes import client, config
import os


def get_bearer_token(cluster_id, region):
    STS_TOKEN_EXPIRES_IN = 60
    session = boto3.session.Session(aws_access_key_id="Axxxx", aws_secret_access_key="yxxxxxx")

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

    

    # remove any base64 encoding padding:
    return 'k8s-aws-v1.' + re.sub(r'=*', '', base64_url)

# If making a HTTP request you would create the authorization headers as follows::

#headers = {'Authorization': 'Bearer ' + get_bearer_token('', 'us-east-2')}
#print(headers)
#osoutput = os.system('curl -H %headers -k https://D97FC3093E01DB8977D79FCD6E300FED.sk1.cn-northwest-1.eks.amazonaws.com.cn/api/v1/namespaces/default/pods')
#print(osoutput)



#api_token = get_bearer_token('eksworkshop-eksctl', 'us-east-1')
api_token = get_bearer_token('kingdee', 'cn-northwest-1')

configuration = client.Configuration()
configuration.host = "https://75058F83314822F453FC876071B20E13.gr7.cn-northwest-1.eks.amazonaws.com.cn:443"
configuration.verify_ssl = False
configuration.debug = True
#configuration.api_key['authorization'] = "Bearer " + api_token
configuration.api_key = {"authorization": "Bearer " + api_token}
#configuration.assert_hostname = True
configuration.verify_ssl = False
#client.Configuration.set_default(configuration)
aApiClient = client.ApiClient(configuration)

v1 = client.CoreV1Api(aApiClient)
#ret = v1.list_pod_for_all_namespaces(watch=False)
ret=v1.list_node()
print(ret)
