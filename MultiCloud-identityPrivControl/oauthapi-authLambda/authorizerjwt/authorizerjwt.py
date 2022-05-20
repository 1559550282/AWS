import re
import json
import os
import urllib.request
import boto3
import time
import logger
from jose import jwk, jwt
from jose.utils import base64url_decode
import auth_manager
import utils
import pystache

region = os.environ['AWS_REGION']
sts_client = boto3.client("sts", region_name=region)
appclientid = "krlAAdMLTDGYIqBrJPzpnkHbubBhnmmG"

def lambda_handler(event, context):
    
    #get JWT token after Bearer from authorization
    token = event['authorizationToken'].split(" ")
    if (token[0] != 'Bearer'):
        raise Exception('Authorization header should have a format Bearer <JWT> Token')
    jwt_bearer_token = token[1]
    print("Method ARN: " + event['methodArn'])
    unauthorized_claims = jwt.get_unverified_claims(jwt_bearer_token)
    project_attri = unauthorized_claims['https://mytesttest.com/project']
    accessrole_attri = unauthorized_claims['https://mytesttest.com/role']
    logger.info("unauthorized_claims info:---------------")
    logger.info(unauthorized_claims)
    logger.info(unauthorized_claims['https://mytesttest.com/project'])
    
    keys_url = 'https://dev-gzu7esjn.us.auth0.com/.well-known/jwks.json'
    with urllib.request.urlopen(keys_url) as f:
        response = f.read()
    keys = json.loads(response.decode('utf-8'))['keys']

    #authenticate against cognito user pool using the key
    response = validateJWT(jwt_bearer_token, appclientid, keys)
    
    #get authenticated claims
    if (response == False):
        logger.error('Unauthorized')
        raise Exception('Unauthorized')
    else:
        logger.info('response_________________')
        logger.info(response)
        principal_id = response["sub"]
    
    tmp = event['methodArn'].split(':')
    api_gateway_arn_tmp = tmp[5].split('/')
    aws_account_id = tmp[4]  
   
    policy = AuthPolicy(principal_id, aws_account_id)
    policy.restApiId = api_gateway_arn_tmp[0]
    policy.region = tmp[3]
    policy.stage = api_gateway_arn_tmp[1]
    
    policy.allowAllMethods() 
    #policy.denyAllMethods()
    #有两个policy，第一个为api的policy，通过lambda的return返回给apigw
    authResponse = policy.build()
    logger.info("authResponse:+++++++++++++++++")
    logger.info(authResponse)
    #第二个为后端lambda使用的policy，通过event传给后端lambda
    
    deliverpolicy = policyGenerator(project_attri,accessrole_attri)
    
    '''
    ##向后端传递aksk+session token
    role_arn = "arn:aws:iam::{}:role/adminrole".format(aws_account_id)
    
    assumed_role = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName="tenant-aware-session",
        #Policy=json.dumps(iam_policy)
        Policy=deliverpolicy
    )
    credentials = assumed_role["Credentials"]

    #pass sts credentials to lambda
    context = {
        'accesskey': credentials['AccessKeyId'], # $context.authorizer.key -> value
        'secretkey' : credentials['SecretAccessKey'],
        'sessiontoken' : credentials["SessionToken"]
    }
    '''
    ##向后端传递policy
    context = {
        'policy': deliverpolicy
    }
    authResponse['context'] = context
    logger.info(authResponse)
    
    return authResponse
    
def policyGenerator(project, projrole):
    dynamodb = boto3.client('dynamodb')
    response = dynamodb.get_item(
        TableName="policytemplate",
        Key={
        'project': {'S': 'project1'},
        'role': {'S': 'readonly'}
        }
    )
    logger.info("response777777777777777777777")
    logger.info(response)
    #template_string = json.dumps(response)
    thecontext = {'region':'ap-southeast-1','accountid':'955513527673','project':'project1'}
    #temppolicy = pystache.render(template_string,thecontext)
    temppolicy = pystache.render(response['Item']['policy']['S'],thecontext)
    logger.info("dynamodb-----------------------")
    logger.info(temppolicy)
    return temppolicy
    
def validateJWT(token, app_client_id, keys):
    # get the kid from the headers prior to verification
    headers = jwt.get_unverified_headers(token)
    logger.info("headers info:---------------")
    logger.info(headers)
    kid = headers['kid']
    # search for the kid in the downloaded public keys
    key_index = -1
    for i in range(len(keys)):
        if kid == keys[i]['kid']:
            key_index = i
            break
    if key_index == -1:
        logger.info('Public key not found in jwks.json')
        return False
    # construct the public key
    public_key = jwk.construct(keys[key_index])
    # get the last two sections of the token,
    # message and signature (encoded in base64)
    message, encoded_signature = str(token).rsplit('.', 1)
    # decode the signature
    decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))
    # verify the signature
    if not public_key.verify(message.encode("utf8"), decoded_signature):
        logger.info('Signature verification failed')
        return False
    logger.info('Signature successfully verified')
    # since we passed the verification, we can now safely
    # use the unverified claims
    claims = jwt.get_unverified_claims(token)
    # additionally we can verify the token expiration
    if time.time() > claims['exp']:
        logger.info('Token is expired')
        return False
    # and the Audience  (use claims['client_id'] if verifying an access token)
    if claims['aud'] != app_client_id:
        logger.info('Token was not issued for this audience')
        return False
    # now we can use the claims
    logger.info(claims)
    return claims
    
class HttpVerb:
    GET     = "GET"
    POST    = "POST"
    PUT     = "PUT"
    PATCH   = "PATCH"
    HEAD    = "HEAD"
    DELETE  = "DELETE"
    OPTIONS = "OPTIONS"
    ALL     = "*"

class AuthPolicy(object):
    awsAccountId = ""
    """The AWS account id the policy will be generated for. This is used to create the method ARNs."""
    principalId = ""
    """The principal used for the policy, this should be a unique identifier for the end user."""
    version = "2012-10-17"
    """The policy version used for the evaluation. This should always be '2012-10-17'"""
    pathRegex = "^[/.a-zA-Z0-9-\*]+$"
    """The regular expression used to validate resource paths for the policy"""

    """these are the internal lists of allowed and denied methods. These are lists
    of objects and each object has 2 properties: A resource ARN and a nullable
    conditions statement.
    the build method processes these lists and generates the approriate
    statements for the final policy"""
    allowMethods = []
    denyMethods = []

    restApiId = "*"
    """The API Gateway API id. By default this is set to '*'"""
    region = "*"
    """The region where the API is deployed. By default this is set to '*'"""
    stage = "*"
    """The name of the stage used in the policy. By default this is set to '*'"""

    def __init__(self, principal, awsAccountId):
        self.awsAccountId = awsAccountId
        self.principalId = principal
        self.allowMethods = []
        self.denyMethods = []

    def _addMethod(self, effect, verb, resource, conditions):
        """Adds a method to the internal lists of allowed or denied methods. Each object in
        the internal list contains a resource ARN and a condition statement. The condition
        statement can be null."""
        if verb != "*" and not hasattr(HttpVerb, verb):
            raise NameError("Invalid HTTP verb " + verb + ". Allowed verbs in HttpVerb class")
        resourcePattern = re.compile(self.pathRegex)
        if not resourcePattern.match(resource):
            raise NameError("Invalid resource path: " + resource + ". Path should match " + self.pathRegex)

        if resource[:1] == "/":
            resource = resource[1:]

        resourceArn = ("arn:aws:execute-api:" +
            self.region + ":" +
            self.awsAccountId + ":" +
            self.restApiId + "/" +
            self.stage + "/" +
            verb + "/" +
            resource)
      
        if effect.lower() == "allow":
            self.allowMethods.append({
                'resourceArn' : resourceArn,
                'conditions' : conditions
            })
            logger.info(self.allowMethods)

        elif effect.lower() == "deny":
            self.denyMethods.append({
                'resourceArn' : resourceArn,
                'conditions' : conditions
            })
            logger.info(self.denyMethods)
            
    def _getEmptyStatement(self, effect):
        """Returns an empty statement object prepopulated with the correct action and the
        desired effect."""
        statement = {
            'Action': 'execute-api:Invoke',
            'Effect': effect[:1].upper() + effect[1:].lower(),
            'Resource': []
        }

        return statement

    def _getStatementForEffect(self, effect, methods):
        """This function loops over an array of objects containing a resourceArn and
        conditions statement and generates the array of statements for the policy."""
        statements = []

        if len(methods) > 0:
            statement = self._getEmptyStatement(effect)

            for curMethod in methods:
                if curMethod['conditions'] is None or len(curMethod['conditions']) == 0:
                    statement['Resource'].append(curMethod['resourceArn'])
                else:
                    conditionalStatement = self._getEmptyStatement(effect)
                    conditionalStatement['Resource'].append(curMethod['resourceArn'])
                    conditionalStatement['Condition'] = curMethod['conditions']
                    statements.append(conditionalStatement)

            statements.append(statement)

        return statements

    def allowAllMethods(self):
        """Adds a '*' allow to the policy to authorize access to all methods of an API"""
        logger.info("call allowAllMethods")
        self._addMethod("Allow", HttpVerb.ALL, "*", [])

    def denyAllMethods(self):
        """Adds a '*' allow to the policy to deny access to all methods of an API"""
        self._addMethod("Deny", HttpVerb.ALL, "*", [])

    def allowMethod(self, verb, resource):
        """Adds an API Gateway method (Http verb + Resource path) to the list of allowed
        methods for the policy"""
        self._addMethod("Allow", verb, resource, [])

    def denyMethod(self, verb, resource):
        """Adds an API Gateway method (Http verb + Resource path) to the list of denied
        methods for the policy"""
        self._addMethod("Deny", verb, resource, [])

    def allowMethodWithConditions(self, verb, resource, conditions):
        """Adds an API Gateway method (Http verb + Resource path) to the list of allowed
        methods and includes a condition for the policy statement. More on AWS policy
        conditions here: http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements.html#Condition"""
        self._addMethod("Allow", verb, resource, conditions)

    def denyMethodWithConditions(self, verb, resource, conditions):
        """Adds an API Gateway method (Http verb + Resource path) to the list of denied
        methods and includes a condition for the policy statement. More on AWS policy
        conditions here: http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements.html#Condition"""
        self._addMethod("Deny", verb, resource, conditions)

    def build(self):
        """Generates the policy document based on the internal lists of allowed and denied
        conditions. This will generate a policy with two main statements for the effect:
        one statement for Allow and one statement for Deny.
        Methods that includes conditions will have their own statement in the policy."""
        if ((self.allowMethods is None or len(self.allowMethods) == 0) and
            (self.denyMethods is None or len(self.denyMethods) == 0)):
            raise NameError("No statements defined for the policy")
        logger.info("build***************")
        logger.info(self.allowMethods)
        
        policy = {
            'principalId' : self.principalId,
            'policyDocument' : {
                'Version' : self.version,
                'Statement' : []
            }
        }
        logger.info("build***************01")
        policy['policyDocument']['Statement'].extend(self._getStatementForEffect("Allow", self.allowMethods))
        policy['policyDocument']['Statement'].extend(self._getStatementForEffect("Deny", self.denyMethods))
        logger.info(policy)
        return policy