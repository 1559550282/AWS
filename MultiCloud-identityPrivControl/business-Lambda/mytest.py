import json
import boto3
import logger
import urllib, sys
import requests

aws_account_id = "955513527673"

def lambda_handler(event, context):
    # TODO implement
    logger.info(event)
    session = boto3.session.Session(aws_access_key_id="xxx", aws_secret_access_key="xxx")
    sts_connection = session.client('sts')
    thepolicy = event['requestContext']['authorizer']['policy']
    
    role_arn = "arn:aws:iam::{}:role/adminrole".format(aws_account_id)
    
    assumed_role = sts_connection.assume_role(
        RoleArn=role_arn,
        RoleSessionName="console-session",
        Policy=thepolicy
    )
    credentials = assumed_role["Credentials"]
    
    '''
    accesskey = event['requestContext']['authorizer']['accesskey']
    secretkey = event['requestContext']['authorizer']['secretkey']
    sessiontoken = event['requestContext']['authorizer']['sessiontoken']
    '''
    
    
    # Step 3: Format resulting temporary credentials into JSON
    url_credentials = {}
    url_credentials['sessionId'] = credentials['AccessKeyId']
    url_credentials['sessionKey'] = credentials['SecretAccessKey']
    url_credentials['sessionToken'] = credentials["SessionToken"]
    json_string_with_temp_credentials = json.dumps(url_credentials)
    
    # Step 4. Make request to AWS federation endpoint to get sign-in token. Construct the parameter string with
    # the sign-in action request, a 12-hour session duration, and the JSON document with temporary credentials
    # as parameters.
    request_parameters = "?Action=getSigninToken"
    request_parameters += "&SessionDuration=43200"
    logger.info("------------------------")
    logger.info(sys.version_info[0])
    if sys.version_info[0] < 3:
        def quote_plus_function(s):
            return urllib.quote_plus(s)
    else:
        def quote_plus_function(s):
            return urllib.parse.quote_plus(s)
    
    request_parameters += "&Session=" + quote_plus_function(json_string_with_temp_credentials)
    request_url = "https://signin.aws.amazon.com/federation" + request_parameters
    logger.info("request url ????????????????????????????????")
    logger.info(request_url)
    r = requests.get(request_url)
    logger.info(r.request)
    logger.info(r)
    # Returns a JSON document with a single element named SigninToken.
    signin_token = json.loads(r.text)

    # Step 5: Create URL where users can use the sign-in token to sign in to
    # the console. This URL must be used within 15 minutes after the
    # sign-in token was issued.
    request_parameters = "?Action=login"
    request_parameters += "&Issuer=Example.org"
    request_parameters += "&Destination=" + quote_plus_function("https://console.aws.amazon.com/")
    request_parameters += "&SigninToken=" + signin_token["SigninToken"]
    request_url = "https://signin.aws.amazon.com/federation" + request_parameters

    # Send final URL to stdout
    logger.info (request_url)
            
    return {
        'statusCode': 200,
        'body': json.dumps(request_url)
    }
    
