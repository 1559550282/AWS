#!/usr/bin/env python
# coding: utf-8

from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth, helpers
from requests_aws4auth import AWS4Auth
import boto3
import json
import hashlib
import datetime
import os
import itertools
import urllib.parse
import numpy as np

s3 = boto3.resource('s3')
bucket = "virginia199"
object_key = "piaozonecsv/piaozone2.faq"
QA_SEP = '====='  # args['qa_sep'] #
EXAMPLE_SEP = '\n\n'
arg_chunk_size = 384
CHUNK_SIZE = 500
CHUNK_OVERLAP = 0

EMB_MODEL_ENDPOINT = "amazon.titan-embed-text-v1"
smr_client = boto3.client("sagemaker-runtime")

AOS_ENDPOINT = "nzt62fy4b2jvs7uzw6z9.us-east-1.aoss.amazonaws.com"
#AOS_ENDPOINT = "ekwoeajjs4agj8k9godl.us-east-1.aoss.amazonaws.com"
REGION = "us-east-1"

publish_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

INDEX_NAME = 'piaozone-qa-single-03'
EMB_BATCH_SIZE = 1
Sentence_Len_Threshold = 10
Paragraph_Len_Threshold = 20

DOC_INDEX_TABLE = 'chatbot_doc_index'
dynamodb = boto3.client('dynamodb')

AOS_BENCHMARK_ENABLED = False
BEDROCK_EMBEDDING_MODELID_LIST = ["cohere.embed-multilingual-v3", "cohere.embed-english-v3",
                                  "amazon.titan-embed-text-v1"]

bedrock = boto3.client(service_name='bedrock-runtime',
                       region_name=os.environ.get('bedrock_region', REGION))


def get_embedding_bedrock(texts, model_id):
    provider = model_id.split(".")[0]
    if provider == "cohere":
        body = json.dumps({
            "texts": [texts] if isinstance(texts, str) else texts,
            "input_type": "search_document"
        })
    else:
        # includes common provider == "amazon"
        body = json.dumps({
            "inputText": texts if isinstance(texts, str) else texts[0],
        })
    bedrock_resp = bedrock.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json"
    )
    response_body = json.loads(bedrock_resp.get('body').read())
    if provider == "cohere":
        embeddings = response_body['embeddings']
    else:
        embeddings = [response_body['embedding']]
    return embeddings


def get_embedding(smr_client, text_arrs, endpoint_name=EMB_MODEL_ENDPOINT):
    if endpoint_name in BEDROCK_EMBEDDING_MODELID_LIST:
        return get_embedding_bedrock(text_arrs, endpoint_name)

    if AOS_BENCHMARK_ENABLED:
        text_len = len(text_arrs)
        return [np.random.rand(768).tolist() for i in range(text_len)]

    parameters = {
    }

    response_model = smr_client.invoke_endpoint(
        EndpointName=endpoint_name,
        Body=json.dumps(
            {
                "inputs": text_arrs,
                "parameters": parameters,
                "is_query": False,
                "instruction": None
            }
        ),
        ContentType="application/json",
    )

    json_str = response_model['Body'].read().decode('utf8')
    json_obj = json.loads(json_str)
    embeddings = json_obj["sentence_embeddings"]

    return embeddings


def batch_generator(generator, batch_size):
    while True:
        batch = list(itertools.islice(generator, batch_size))
        if not batch:
            break
        yield batch
def iterate_QA(file_content, object_key, smr_client, index_name, endpoint_name):
    print("--------interate_QA-----------")
    json_content = json.loads(file_content)
    print("after json content---------------------")
    json_arr = json_content["qa_list"]
    doc_title = object_key
    doc_category = json_content["doc_category"]
    print(json_arr)
    it = iter(json_arr)
    qa_batches = batch_generator(it, batch_size=EMB_BATCH_SIZE)

    doc_author = get_filename_from_obj_key(object_key)
    n=0
    for idx, batch in enumerate(qa_batches):
        n = n+1
        print("qa_batches----------------------------")
        print(n)
        #doc_template = "Question: {}\nAnswer: {}"
        doc_template = "Answer: {}"
        questions = [item['Question'] for item in batch]
        print(questions)
        answers = [item['Answer'] for item in batch]
        #docs = [doc_template.format(item['Question'], item['Answer']) for item in batch]
        docs = [doc_template.format(item['Answer']) for item in batch]
        authors = [item.get('Author') for item in batch]
        embeddings_q = get_embedding(smr_client, questions, endpoint_name)

        for i in range(len(embeddings_q)):
            document = {"AMAZON_BEDROCK_METADATA": """{"source":"s3://virginia199/piaozonecsv/piaozone.csv"}""",
                        "AMAZON_BEDROCK_TEXT_CHUNK": docs[i],
                        "bedrock-knowledge-base-default-vector": embeddings_q[i]}
            #yield {"_index": index_name, "_source": document,
            #       "_id": hashlib.md5(str(document).encode('utf-8')).hexdigest()}
            yield {"_index": index_name, "_source": document}

        embeddings_a = get_embedding(smr_client, answers, endpoint_name)
        for i in range(len(embeddings_a)):
            document = {"AMAZON_BEDROCK_METADATA": """{"source":"s3://virginia199/piaozonecsv/piaozone.csv"}""",
                        "AMAZON_BEDROCK_TEXT_CHUNK": docs[i],
                        "bedrock-knowledge-base-default-vector": embeddings_a[i],
                        "id": hashlib.md5(str(docs[i]).encode('utf-8')).hexdigest()}
            #yield {"_index": index_name, "_source": document,
            #       "_id": hashlib.md5(str(document).encode('utf-8')).hexdigest()}
            yield {"_index": index_name, "_source": document}
def parse_faq_to_json(file_content):
    print("--------------------parse_faq_to_json-----------------------")
    arr = file_content.split(QA_SEP)
    print(len(arr))
    json_arr = []
    for item in arr:
        #print(item)
        question, answer = item.strip().split("\n", 1)
        question = question.replace("Question: ", "")
        answer = answer.replace("Answer: ", "")
        obj = {
            "Question": question, "Answer": answer
        }
        json_arr.append(obj)
        print(len(json_arr))
        #print(json_arr)
    qa_content = {
        "doc_title": "",
        "doc_category": "FAQ",
        "qa_list": json_arr
    }

    json_content = json.dumps(qa_content, ensure_ascii=False)
    #print("--------------------------------------------")
    #print(json_content)
    return json_content


def load_content_json_from_s3(bucket, object_key, content_type, credentials):
    obj = s3.Object(bucket, object_key)
    file_content = obj.get()['Body'].read().decode('utf-8', errors='ignore').strip()
    try:
        if content_type == 'faq':
            json_content = parse_faq_to_json(file_content)
        else:
            print(f"unsupport content type...{content_type}")
            raise RuntimeError(f"unsupport content type...{content_type}")
    except Exception as e:
        raise RuntimeError(f"Exception ...{str(e)}")
    return json_content

def WriteVecIndexToAOS(bucket, object_key, content_type, smr_client, aos_endpoint=AOS_ENDPOINT, region=REGION,
                       index_name=INDEX_NAME):
    credentials = boto3.Session().get_credentials()
    service = 'aoss'
    auth = AWS4Auth(credentials.access_key, credentials.secret_key,
                       region, service, session_token=credentials.token)
    try:
        file_content = load_content_json_from_s3(bucket, object_key, content_type, credentials)
        client = OpenSearch(
            hosts=[{'host': aos_endpoint, 'port': 443}],
            http_auth=auth,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection,
            timeout=300,  # 默认超时时间是10 秒，
            max_retries=2,  # 重试次数
            retry_on_timeout=True
        )
        gen_aos_record_func = None
        if content_type in ["faq", "csv"]:
            gen_aos_record_func = iterate_QA(file_content, object_key, smr_client, index_name, EMB_MODEL_ENDPOINT)
        else:
            raise RuntimeError('No Such Content type supported')
        response = helpers.bulk(client, gen_aos_record_func, max_retries=3, initial_backoff=200, max_backoff=801,
                                max_chunk_bytes=10 * 1024 * 1024)  # , chunk_size=10000, request_timeout=60000)
        return response
    except Exception as e:
        print(f"There was an error when ingest:{object_key} to aos cluster, Exception: {str(e)}")
        return None


def process_s3_uploaded_file(bucket, object_key):
    print("********** object_key : " + object_key)

    content_type = None
    index_name = INDEX_NAME
    if object_key.endswith(".faq"):
        print("********** pre-processing faq file")
        content_type = 'faq'
    else:
        raise RuntimeError("unsupport content type")

    username = get_filename_from_obj_key(object_key)
    response = WriteVecIndexToAOS(bucket, object_key, content_type, smr_client, index_name=index_name)


##如果是从chatbot上传，则是ai-content/username/filename
def get_filename_from_obj_key(object_key):
    paths = object_key.split('/')
    return paths[1] if len(paths) > 2 else 's3_upload'


for s3_key in object_key.split(','):
    s3_key = urllib.parse.unquote(s3_key)  ##In case Chinese filename
    s3_key = s3_key.replace('+',
                            ' ')  ##replace the '+' with space. ps:if the original file name contains space, then s3 notification will replace it with '+'.
    print("processing {}".format(s3_key))
    process_s3_uploaded_file(bucket, s3_key)