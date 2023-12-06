{\rtf1\ansi\ansicpg1252\cocoartf2709
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 from typing import List,Dict,Union\
#from confs import user_info, functions_configs, product_name_map, product_tax_map, product_47_to_38_map\
import requests\
import json\
import time\
import hashlib\
import os\
from cryptography.hazmat.primitives import padding\
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes\
from cryptography.hazmat.backends import default_backend\
import base64\
import random\
import datetime\
import boto3\
import os\
\
s3 = boto3.client('s3')\
bucket = os.environ.get('BUCKET_NAME')  #Name of bucket with data file and OpenAPI file\
product_name_map_file = 'product_code_name_map.txt' #Location of data file in S3\
product_name_map_v38_file = 'product_38_code_name_map.txt'\
product_v47_to_v38_file = "product_47_to_38_map.txt"\
local_product_name_map_file = '/tmp/product_code_name_map.txt' #Location of data file in S3\
local_product_name_map_v38_file = '/tmp/product_38_code_name_map.txt'\
local_product_v47_to_v38_file = "/tmp/product_47_to_38_map.txt"\
# local_db = '/tmp/csbot.db' #Location in Lambda /tmp folder where data file will be copied\
s3.download_file(bucket, product_name_map_file, local_product_name_map_file)\
s3.download_file(bucket, product_name_map_v38_file, local_product_name_map_v38_file)\
s3.download_file(bucket, product_v47_to_v38_file, local_product_v47_to_v38_file)\
\
\
# ##################### base_conf ###############################\
port = 8080\
VERSION = "1"\
# openai llm \uc0\u35774 \u32622 \
# \uc0\u29992 \u25143 \u20449 \u24687 \u35774 \u32622 \
user_info = \{\
            "id": "000001",\
            "name": "\uc0\u26446 \u26519 \u26519 ",\
            "email": "test1@163.com",\
            "drawer": "\uc0\u26446 \u26519 \u26519 ",\
            "reviewer": "\uc0\u38472 \u33251 ",\
            "payee": "\uc0\u26446 \u22797 ",\
            "phone": "0755-0000000",\
            "address": "\uc0\u21335 \u23665 \u31185 \u25216 \u22253 ",\
            "card_name": "\uc0\u25307 \u21830 \u38134 \u34892 \u39640 \u26032 \u22253 \u25903 \u34892 ",\
            "card_number": "00000000000000",\
            "company_name": "\uc0\u33322 \u20449 \u22521 \u35757 \u20225 \u19994 ",\
            "tax_number": "440301999999980"\
\}\
\
## \uc0\u20989 \u25968 \u35774 \u32622 \
## \uc0\u20989 \u25968 \u35774 \u32622 \
functions_configs = \{\
    "1":\{\
        "get_product_code":\
            \{\
                "url":"https://api-sit.piaozone.com/nlp_service/match/goodName",\
                "product_name_map_file": local_product_name_map_file,\
                "product_name_map_v38_file": local_product_name_map_v38_file,\
                "product_v47_to_v38_file": local_product_v47_to_v38_file\
            \},\
        "generate_preview_invoice_image":\
            \{\
                "url":"https://api-sit.piaozone.com/doc/full/digital/invoice/pdf/create",\
                "access_token":"7ed4131b37d4e3835f65be27b3a33b2e"\
            \},\
        "issue_invoice":\
            \{\
                "url":"http://api-sit.piaozone.com/m5/bill/invoice/create",\
                "access_token":"7c9956309309a313218a98083ef2680b",\
                "encrypt_key":"Lg1ZwCNFYg5cp7Mk"\
                # "encrypt_key":"!!king?DeE|12345"\
            \},\
        "send_invoice_email":\
            \{\
                "url":"https://api-sit.piaozone.com/m5/bill/invoice/email/and/message/send",\
                "access_token":"7c9956309309a313218a98083ef2680b",\
                "encrypt_key":"Lg1ZwCNFYg5cp7Mk"\
            \},\
        "expense_match":\
            \{\
                "url":"https://api-sit.piaozone.com/nlp_service/match/billName"\
                # "url":"http://172.21.52.48:8083/nlp_service/match/billName"\
            \}\
    \}\
\}\
\
## \uc0\u25968 \u25454 \u24211 \u35774 \u32622 \
db_configs = \{\
    "host":'kingdee.cluster-c5kzgyykhpk6.us-west-2.rds.amazonaws.com',\
    "port":3306,\
    "user":'root',\
    "passwd":'Welcome1',\
    "db":'kingdee',\
    "charset":'utf8',\
    "table_name":"test_chatbot_message_v2"\
\}\
\
\
invoice_type_map = \{\
    '1': '\uc0\u26222 \u36890 \u30005 \u23376 \u21457 \u31080 ',\
    '2': '\uc0\u30005 \u23376 \u21457 \u31080 \u19987 \u31080 ',\
    '3': '\uc0\u26222 \u36890 \u32440 \u36136 \u21457 \u31080 ',\
    '4': '\uc0\u19987 \u29992 \u32440 \u36136 \u21457 \u31080 ',\
    '5': '\uc0\u26222 \u36890 \u32440 \u36136 \u21367 \u31080 ',\
    '7': '\uc0\u36890 \u29992 \u26426 \u25171 ',\
    '8': '\uc0\u30340 \u22763 \u31080 ',\
    '9': '\uc0\u28779 \u36710 \u31080 ',\
    '10': '\uc0\u39134 \u26426 \u31080 ',\
    '11': '\uc0\u20854 \u20182 ',\
    '12': '\uc0\u26426 \u21160 \u36710 ',\
    '13': '\uc0\u20108 \u25163 \u36710 ',\
    '14': '\uc0\u23450 \u39069 \u21457 \u31080 ',\
    '15': '\uc0\u36890 \u34892 \u36153 ',\
     '16': '\uc0\u23458 \u36816 \u21457 \u31080 ',\
     '17': '\uc0\u36807 \u36335 \u36807 \u26725 \u36153 ',\
    '18': '\uc0\u36710 \u33337 \u31246 \u21457 \u31080 \u65288 \u19987 \u31080 \u65289 ',\
    '19': '\uc0\u23436 \u31246 \u35777 \u26126 ',\
    '20': '\uc0\u36718 \u33337 \u31080 ',\
    '21': '\uc0\u28023 \u20851 \u32564 \u27454 \u20070 ',\
    '22': '\uc0\u34987 \u21344 \u20301 \u20013 ',\
    '23': '\uc0\u36890 \u29992 \u26426 \u25171 \u30005 \u23376 \u21457 \u31080 ',\
     '24': '\uc0\u28779 \u36710 \u31080 \u36864 \u31080 \u20973 \u35777 ',\
     '25': '\uc0\u36130 \u25919 \u30005 \u23376 \u31080 \u25454 ',\
     '26': '\uc0\u25968 \u30005 \u31080 \u65288 \u26222 \u36890 \u21457 \u31080 \u65289 ',\
    '27': '\uc0\u25968 \u30005 \u31080 \u65288 \u22686 \u20540 \u31246 \u19987 \u29992 \u21457 \u31080 \u65289 ',\
     '28': '\uc0\u25968 \u30005 \u31080 \u65288 \u33322 \u31354 \u36816 \u36755 \u30005 \u23376 \u23458 \u31080 \u34892 \u31243 \u21333 \u65289 ',\
     '29': '\uc0\u25968 \u30005 \u31080 \u65288 \u38081 \u36335 \u30005 \u23376 \u23458 \u31080 \u65289 ',\
    '30': '\uc0\u24418 \u24335 \u21457 \u31080 '\}\
\
\
# ##################### __init__ ###############################\
\
#\uc0\u35774 \u32622 prompt\u35821 \u35328 \
# SYSTEM_PROMPT = system_prompt[VERSION]\
# \uc0\u37197 \u32622 \u26356 \u26032 \
\
functions_configs = functions_configs[VERSION]\
# \uc0\u35774 \u32622  log\u36335 \u24452 \
# logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')\
# if not os.path.exists(logs_dir):\
#     os.makedirs(logs_dir, exist_ok=True)\
# \uc0\u23548 \u20837 \u21830 \u21697 \u21517 \u31216 \u26144 \u23556 \u34920 \u20197 \u21450 \u21830 \u21697 \u31246 \u29575 \u26144 \u23556 \u34920 \
product_name_map = \{\}\
product_tax_map = \{\}\
with open(functions_configs["get_product_code"]["product_name_map_file"],encoding="utf-8") as f:\
    for line in f.readlines():\
        line = line.strip()\
        if line:\
            code,name,tax = line.split("\\t")\
            product_name_map[code] = name\
            product_tax_map[code] = min([float(tax_ins.strip('%')) / 100 for tax_ins in tax.split("\uc0\u12289 ")])\
\
# \uc0\u26144 \u23556 \u34920 \u20869 \u23481 \u26356 \u26032 ,\u25903 \u25345 38\u29256 \u32534 \u30721 \
product_name_map_38 = \{\}\
product_tax_map_38 = \{\}\
with open(functions_configs["get_product_code"]["product_name_map_v38_file"],encoding="utf-8") as f:\
    for line in f.readlines():\
        line = line.strip()\
        if line:\
            code,name,tax = line.split("\\t")\
            product_name_map_38[code] = name\
            product_tax_map_38[code] = min([float(tax_ins.strip('%')) / 100 for tax_ins in tax.split("\uc0\u12289 ")])\
#\uc0\u26356 \u26032 \u26144 \u23556 \u34920 \
product_name_map.update(product_name_map_38)\
product_tax_map.update(product_tax_map_38)\
\
product_47_to_38_map = \{\}\
with open(functions_configs["get_product_code"]["product_v47_to_v38_file"],encoding="utf-8") as f:\
    for line in f.readlines():\
        line = line.strip()\
        if line:\
            code47,code38 = line.split("\\t")\
            product_47_to_38_map[code47] = code38\
\
# temp implemetaion\
# product_name_map = \{\}\
# product_tax_map = \{\}\
# for line in product_name_map_file:\
#     line = line.strip()\
#     if line:\
#         code,name,tax = line.split("\\t")\
#         product_name_map[code] = name\
#         product_tax_map[code] = min([float(tax_ins.strip('%')) / 100 for tax_ins in tax.split("\uc0\u12289 ")])\
\
# # \uc0\u26144 \u23556 \u34920 \u20869 \u23481 \u26356 \u26032 ,\u25903 \u25345 38\u29256 \u32534 \u30721 \
# product_name_map_38 = \{\}\
# product_tax_map_38 = \{\}\
# for line in product_name_map_v38_file:\
#     line = line.strip()\
#     if line:\
#         code,name,tax = line.split("\\t")\
#         product_name_map_38[code] = name\
#         product_tax_map_38[code] = min([float(tax_ins.strip('%')) / 100 for tax_ins in tax.split("\uc0\u12289 ")])\
# #\uc0\u26356 \u26032 \u26144 \u23556 \u34920 \
# product_name_map.update(product_name_map_38)\
# product_tax_map.update(product_tax_map_38)\
\
# product_47_to_38_map = \{\}\
\
# for line in product_v47_to_v38_file:\
#     line = line.strip()\
#     if line:\
#         code47,code38 = line.split("\\t")\
#         product_47_to_38_map[code47] = code38\
\
def get_named_parameter(event, name):\
    return next(item for item in event['parameters'] if item['name'] == name)['value']\
\
def get_named_property(event, name):\
    return next(item for item in event['requestBody']['content']['application/json']['properties'] if item['name'] == name)['value']\
\
def get_random_num():\
    """\uc0\u29983 \u25104 20\u20301 \u38543 \u26426 \u23383 \u31526 \u20018 """\
    timestamp = int(time.time() * 1000)  # \uc0\u33719 \u21462 \u24403 \u21069 \u26102 \u38388 \u30340 \u26102 \u38388 \u25139 \u24182 \u23558 \u20854 \u36716 \u25442 \u20026 \u27627 \u31186 \
    data_to_hash = f"\{timestamp\}"\
    signature = hashlib.md5(data_to_hash.encode()).hexdigest()[:14]\
    random_num = "%06d" % random.randint(0, 1000000)  # 6\
    return signature+random_num\
\
\
def getInvoiceToken():\
    # data = \{"sign": "f6bec88ab57d1b96829926351216ec13", "client_id": "vc0c6hjlgnKCic", "timestamp": 1681453216930\}\
    data = \{"sign": "aa6e0e3df02bd90b53b69a3b5def3ce7", "client_id": "Ib8mNbIzLn7ePnEwHTxi",\
            "timestamp": 1681453216930\}\
    url = "https://api-sit.piaozone.com/base/oauth/token"\
    response = requests.post(url=url, json=data)\
    res = response.json()\
    return res['access_token']\
\
def encrypt(encrypt_key: str, data: dict):\
    """\uc0\u23545 \u36755 \u20837 \u30340 \u25968 \u25454 \u36827 \u34892 \u21152 \u23494 """\
    key = encrypt_key.encode()\
\
    # Serialize the data dictionary to JSON\
    data_json = json.dumps(data).encode()\
\
    # Create a PKCS7 padding object\
    padder = padding.PKCS7(128).padder()\
    padded_data = padder.update(data_json) + padder.finalize()\
\
    # Create a cipher object using AES ECB mode\
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())\
\
    # Create an encryptor\
    encryptor = cipher.encryptor()\
\
    # Encrypt the padded data\
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()\
\
    # Encode the ciphertext in Base64\
    base64_cipher = base64.b64encode(encrypted_data).decode()\
    return base64_cipher\
\
def get_product_code(product_name: str):\
    """This function get top 5 possible tax codes corresponding to the product name"""\
    function_name = "get_product_code"\
    url = functions_configs[function_name]["url"]\
    data = \{"text": product_name,\
            "top_num": 5\}\
    response = requests.post(url=url, json=data)\
    res = response.json()\
    new_res = \{\}\
    new_res["input_args"] = \{\}\
    new_res["input_args"]["product_name"] = product_name\
    if "results" in res:\
        new_res["status"] = "success"\
        res_data = []\
        for ins in res["results"]:\
            res_data.append(\{"\uc0\u31246 \u25910 \u32534 \u30721 ": ins["name"], "\u31246 \u25910 \u32534 \u30721 \u21517 \u31216 ": product_name_map[ins["name"]]\})\
        new_res["results"] = res_data\
    else:\
        new_res["status"] = "fail"\
        new_res["results"] = "\uc0\u26080 \u27861 \u36827 \u34892 \u21830 \u21697 \u31246 \u25910 \u32534 \u30721 \u25512 \u33616 \u65292 \u35831 \u37325 \u26032 \u36755 \u20837 \u21830 \u21697 \u21517 \u31216 ."\
    return new_res\
\
\
def generatePreviewInvoiceImage(event):\
    """This function generates a preview invoice image"""\
    function_name = "generate_preview_invoice_image"\
    print(f"calling method: \{function_name\}")\
    print(f"Event: \\n \{json.dumps(event)\}")\
\
    user_id = get_named_parameter(event, 'user_id') \
    product_detail = get_named_parameter(event, 'product_detail')\
    buyer_company_name = get_named_parameter(event, 'buyer_company_name')\
    buyer_tax_number = get_named_parameter(event, 'buyer_tax_number')\
    try:\
        invoice_type = get_named_parameter(event, 'invoice_type')\
    except:\
        invoice_type = "\uc0\u20840 \u30005 \u26222 \u36890 \u21457 \u31080 "\
    \
    try:\
        remark = get_named_parameter(event, 'remark')\
    except:\
        remark = ""\
\
    print ("parameters ==> ", "user_id:", user_id, "product_detail:", product_detail, "buyer_company_name:", buyer_company_name, "buyer_tax_number:", buyer_tax_number, "invoice_type:", invoice_type, "remark:", remark )\
    ## request \uc0\u35774 \u32622 \
    \
    url = functions_configs[function_name]["url"]\
    header = \{\
        "client-platform": "common",\
        "Content-Type": "application/json"\
    \}\
    print("---------generate preview invoide image---------------------")\
    #params = \{"access_token":functions_configs[function_name]["access_token"]\}\
    params=\{"access_token": getInvoiceToken()\}\
    ## \uc0\u21457 \u31080 \u22522 \u30784 \u20449 \u24687 \u35774 \u32622 \
    # assert user_id in user_info, f"user id <\{user_id\}>  does not exist."\
    seller_company_name = user_info["company_name"]\
    seller_tax_number = user_info["tax_number"]\
    drawer = user_info.get("drawer","")\
    issue_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())\
    temp_invoice_number = "00000000"\
    new_res = \{\}\
    new_res["input_args"] = \{\}\
    new_res["input_args"]["product_detail"] = product_detail\
    new_res["input_args"]["buyer_company_name"] = buyer_company_name\
    new_res["input_args"]["buyer_tax_number"] = buyer_tax_number\
    new_res["input_args"]["invoice_type"] = invoice_type\
    new_res["input_args"]["remark"] = remark\
    ## \uc0\u21457 \u31080 \u37325 \u35201 \u20449 \u24687 \u35774 \u32622 \
    ### 1. \uc0\u21457 \u31080 \u31181 \u31867 \
    invoice_type_map = \{"\uc0\u20840 \u30005 \u26222 \u36890 \u21457 \u31080 ": "26", "\u20840 \u30005 \u19987 \u29992 \u21457 \u31080 ": "27"\}\
    invoice_type_num = invoice_type_map.get(invoice_type, None)\
    if invoice_type_num is None:\
        new_res["status"] = "fail"\
        new_res["results"] = f"\uc0\u21457 \u31080 \u31181 \u31867 <\{invoice_type\}>\u22635 \u38169 \u20102 \u65292 \u30446 \u21069 \u21482 \u25903 \u25345 '\u20840 \u30005 \u26222 \u36890 \u21457 \u31080 '\u21644 '\u20840 \u30005 \u19987 \u29992 \u21457 \u31080 '\u65292 \u35831 \u36827 \u34892 \u20462 \u25913 ."\
        return new_res\
    ### 2. \uc0\u21830 \u21697 \u26126 \u32454 \u12289 \u19981 \u35745 \u31246 \u30340 \u24635 \u37329 \u39069 \u12289 \u24635 \u31246 \u39069 \u35774 \u32622 \
    itemlist = []\
    invoice_amounts = 0 #\uc0\u19981 \u35745 \u31246 \u30340 \u24635 \u37329 \u39069 \
    tax_amounts = 0 #\uc0\u24635 \u31246 \u39069 \
    if isinstance(product_detail,str):\
        product_detail = product_detail.replace('\\"', '"')\
        product_detail = product_detail.replace('["\{', '[\{')\
        product_detail = product_detail.replace('\}"]', '\}]')\
        product_detail = eval(product_detail)\
\
    print(f"After process product_detail: \{product_detail\}")\
 \
    for product in product_detail:\
        if isinstance(product["money"],str):\
            product["money"] = product["money"].strip()\
            try:\
                product["money"] = int(product["money"])\
            except:\
                product["money"] = float(product["money"])\
        product_total_amount = '\{:.2f\}'.format(product["money"])  # \uc0\u27599 \u20010 \u21830 \u21697 \u30340 \u24635 \u37329 \u39069 \
        tax_rate = product_tax_map.get(product["code"], None) #\uc0\u31246 \u29575 \
        if tax_rate is None:\
            new_res["status"] = "fail"\
            new_res["results"] = f"\uc0\u24744 \u25552 \u20379 \u30340 \u21830 \u21697 <\{product['name']\}>\u30340 \u31246 \u25910 \u32534 \u30721 <\{product['code']\}>\u26159 \u38169 \u35823 \u30340 \u65292 \u35831 \u36827 \u34892 \u20462 \u25913 ."\
            return new_res\
        product_amount = '\{:.2f\}'.format(float(product_total_amount) / (1 + tax_rate))  # \uc0\u27599 \u20010 \u21830 \u21697 \u21435 \u25481 \u31246 \u39069 \u30340 \u21407 \u22987 \u37329 \u39069 \
        tax_amount = '\{:.2f\}'.format(float(product_amount) * tax_rate)#\uc0\u27599 \u20010 \u21830 \u21697 \u30340 \u31246 \u39069 \
        invoice_amounts += float(product_amount)\
        tax_amounts += float(tax_amount)\
\
        itemlist.append(\{\
            "goodsName": product["name"],\
            "specModel": "",\
            "unit": "",\
            "num": "",\
            "unitPrice": "",\
            "detailAmount": product_amount,\
            "taxRate": '\{:.2f\}'.format(tax_rate),\
            "taxAmount": tax_amount,\
            "zeroTaxRateFlag": ""\
        \})\
    data = \{\
        "clientId": "testClinetId",\
        "appName": "\uc0\u24320 \u31080 ",\
        "invoiceType": invoice_type_num,\
        "invoiceNo": temp_invoice_number,\
        "issueTime": issue_date,\
        "buyerName": buyer_company_name,\
        "buyerTaxNo": buyer_tax_number,\
        "salerName": seller_company_name,\
        "salerTaxNo": seller_tax_number,\
        "remark": remark,\
        "drawer": drawer,\
        "invoiceAmount": '\{:.2f\}'.format(invoice_amounts),\
        "totalTaxAmount": '\{:.2f\}'.format(tax_amounts),\
        "totalAmount": '\{:.2f\}'.format(invoice_amounts+tax_amounts),\
        "itemList": itemlist\
    \}\
    response = requests.post(url=url, data=json.dumps(data), headers=header,params=params)\
    result = response.json()\
    if "data" not in result or not result["data"]:\
        new_res["status"] = "fail"\
        new_res["results"] = f"\uc0\u38750 \u24120 \u25265 \u27465 \u65292 \u26080 \u27861 \u29983 \u25104 \u39044 \u35272 \u21457 \u31080 \u22270 \u29255 \u65292 \u35831 \u31245 \u21518 \u23581 \u35797 \u37325 \u26032 \u24320 \u31080 \u12290 "\
    else:\
        new_res["status"] = "success"\
        new_res["results"] = result["data"]\
    return new_res\
\
\
def issueInvoice(event):\
    """This function is used to issue invoices"""\
    ## request\uc0\u21442 \u25968  \u35774 \u32622 \
    print("------------issue_invoice----------------")\
    function_name = "issue_invoice"\
    print(f"calling method: \{function_name\}")\
\
    user_id = get_named_parameter(event, 'user_id') \
    product_detail = get_named_parameter(event, 'product_detail')\
    buyer_company_name = get_named_parameter(event, 'buyer_company_name')\
    buyer_tax_number = get_named_parameter(event, 'buyer_tax_number')\
    \
    try:\
        invoice_type = get_named_parameter(event, 'invoice_type')\
    except:\
        invoice_type = "\uc0\u20840 \u30005 \u26222 \u36890 \u21457 \u31080 "\
    \
    try:\
        remark = get_named_parameter(event, 'remark')\
    except:\
        remark = ""\
    \
    print ("parameters ==> ", "user_id:", user_id, "product_detail:", product_detail, "buyer_company_name:", buyer_company_name, "buyer_tax_number:", buyer_tax_number, "invoice_type:", invoice_type, "remark:", remark )\
\
    url = functions_configs[function_name]["url"]\
    encrypt_key = functions_configs[function_name]["encrypt_key"]\
    params = \{"access_token": getInvoiceToken()\}\
    # params = \{"access_token":functions_configs[function_name]["access_token"]\}\
    header = \{"Content-Type": "application/json"\}\
\
    ## \uc0\u21457 \u31080 \u22522 \u30784 \u20449 \u24687 \u35774 \u32622 \
    serial_id = get_random_num()\
    drawer = user_info.get("drawer", "")\
    reviewer = user_info.get("reviewer", "")\
    payee = user_info.get("payee", "")\
    seller_address = user_info.get("address", "")\
    seller_phone = user_info.get("phone", "")\
    seller_account = user_info.get("card_name", "") + user_info.get("card_number", "")\
    seller_cardname = user_info.get("card_name", "")\
    seller_cardnumber = user_info.get("card_number", "")\
    # seller_company_name = user_info["company_name"]\
    seller_tax_number = user_info["tax_number"]\
    #\uc0\u21021 \u22987 \u21270 \u36755 \u20986 \
    \
    res = \{\}\
    res["input_args"] = \{\}\
    res["input_args"]["product_detail"] = product_detail\
    res["input_args"]["buyer_company_name"] = buyer_company_name\
    res["input_args"]["buyer_tax_number"] = buyer_tax_number\
    res["input_args"]["invoice_type"] = invoice_type\
    res["input_args"]["remark"] = remark\
    ## \uc0\u21457 \u31080 \u37325 \u35201 \u20449 \u24687 \u35774 \u32622 \
    ### 1. \uc0\u21457 \u31080 \u31181 \u31867 \
    invoice_type_map = \{"\uc0\u20840 \u30005 \u26222 \u36890 \u21457 \u31080 ": "1", "\u20840 \u30005 \u19987 \u29992 \u21457 \u31080 ": "2"\}\
    invoice_type_num = invoice_type_map.get(invoice_type, None)\
    if invoice_type_num is None:\
        res["status"] = "fail"\
        res["results"] = f"\uc0\u21457 \u31080 \u31181 \u31867 <\{invoice_type\}>\u22635 \u38169 \u20102 \u65292 \u30446 \u21069 \u21482 \u25903 \u25345 '\u20840 \u30005 \u26222 \u36890 \u21457 \u31080 '\u21644 '\u20840 \u30005 \u19987 \u29992 \u21457 \u31080 '\u65292 \u35831 \u36827 \u34892 \u20462 \u25913 ."\
        return res\
    ### 2. \uc0\u21830 \u21697 \u26126 \u32454 \u12289 \u19981 \u35745 \u31246 \u30340 \u24635 \u37329 \u39069 \u12289 \u24635 \u31246 \u39069 \u35774 \u32622 \
    itemlist = []\
    invoice_amounts = 0 #\uc0\u19981 \u35745 \u31246 \u30340 \u24635 \u37329 \u39069 \
    tax_amounts = 0 #\uc0\u24635 \u31246 \u39069 \
    \
    if isinstance(product_detail,str):\
        product_detail = product_detail.replace('\\"', '"')\
        product_detail = product_detail.replace('["\{', '[\{')\
        product_detail = product_detail.replace('\}"]', '\}]')\
        product_detail = eval(product_detail)\
        \
    print(f"After process product_detail: \{product_detail\}")\
    \
    for product in product_detail:\
        if isinstance(product["money"], str):\
            product["money"] = product["money"].strip()\
            try:\
                product["money"] = int(product["money"])\
            except:\
                product["money"] = float(product["money"])\
        product["code"] = product_47_to_38_map[product["code"]] \\\
            if product["code"] in product_47_to_38_map \\\
            else product["code"]\
        product_total_amount = '\{:.2f\}'.format(product["money"])  # \uc0\u27599 \u20010 \u21830 \u21697 \u30340 \u24635 \u37329 \u39069 \
        tax_rate = product_tax_map.get(product["code"], None) #\uc0\u31246 \u29575 \
        if tax_rate is None:\
            res["status"] = "fail"\
            res["results"] = f"\uc0\u24744 \u25552 \u20379 \u30340 \u21830 \u21697 <\{product['name']\}>\u30340 \u31246 \u25910 \u32534 \u30721 <\{product['code']\}>\u26159 \u38169 \u35823 \u30340 \u65292 \u35831 \u36827 \u34892 \u20462 \u25913 ."\
            return res\
        product_amount = '\{:.2f\}'.format(float(product_total_amount) / (1 + tax_rate))  # \uc0\u27599 \u20010 \u21830 \u21697 \u21435 \u25481 \u31246 \u30340 \u21407 \u22987 \u37329 \u39069 \
        tax_amount = '\{:.2f\}'.format(float(product_amount) * tax_rate) #\uc0\u27599 \u20010 \u21830 \u21697 \u30340 \u31246 \u39069 \
        invoice_amounts += float(product_amount)\
        tax_amounts += float(tax_amount)\
        itemlist.append(\{\
            "specModel": "",\
            "zeroTaxRateFlag": "",\
            "taxAmount": tax_amount,\
            "taxRate": '\{:.2f\}'.format(tax_rate),\
            "goodsCode": product["code"],\
            "detailAmount": product_amount,\
            "discountType": "0",\
            "goodsName": product["name"],\
            "preferentialPolicy": "0",\
            "vatException": ""\
        \})\
    ## \uc0\u21019 \u24314 invoice_info\
    invoice_info = \{\
        "serialNo": serial_id,\
        "taxFlag": "0",\
        "inventoryFlag": "0",\
        "inventoryProjectName": "0",\
        "salerAddress": seller_address,\
        "salerPhone": seller_phone,\
        "salerAccount": seller_account,\
        "salerCardName": seller_cardname,\
        "salerCardNumber": seller_cardnumber,\
        "salerTaxNo": seller_tax_number,\
        "buyerName": buyer_company_name,\
        "buyerTaxNo": buyer_tax_number,\
        "invoiceAmount": '\{:.2f\}'.format(invoice_amounts),\
        "totalAmount": '\{:.2f\}'.format(invoice_amounts + tax_amounts),\
        "totalTaxAmount": '\{:.2f\}'.format(tax_amounts),\
        "type": "0",\
        "drawer": drawer,\
        "reviewer": reviewer,\
        "payee": payee,\
        "originalInvoiceCode": "",\
        "originalInvoiceNo": "",\
        "invoiceType": invoice_type_num,\
        "remark": remark,\
        "items": itemlist\
    \}\
    #\uc0\u21152 \u23494 'inventoryProjectName' = \{str\} '0'\
    base64_cipher = encrypt(encrypt_key=encrypt_key,data=invoice_info)\
    response = requests.post(\
        url=url,\
        data=json.dumps(base64_cipher),\
        headers=header,\
        params=params\
    )\
    result = response.json()\
    if result["description"] == "\uc0\u35813 \u27969 \u27700 \u21495 \u24050 \u32463 \u23384 \u22312 ":\
        res["status"] = "fail"\
        res["results"] = f"\uc0\u38750 \u24120 \u25265 \u27465 \u65292 \u21457 \u31080 \u24320 \u20855 \u22833 \u36133 \u65292 \u29983 \u25104 \u30340 \u27969 \u27700 \u21495 \u24050 \u32463 \u23384 \u22312 \u65292 \u35831 \u31245 \u21518 \u23581 \u35797 \u37325 \u26032 \u24320 \u31080 \u12290 "\
        return res\
    if "data" not in result or not result["data"]:\
        res["status"] = "fail"\
        res["results"] = f"\uc0\u38750 \u24120 \u25265 \u27465 \u65292 \u21457 \u31080 \u24320 \u20855 \u22833 \u36133 \u65292 \u35831 \u31245 \u21518 \u23581 \u35797 \u37325 \u26032 \u24320 \u31080 \u12290 "\
    else:\
        res["status"] = "success"\
        res["results"] = result["data"]\
    return res\
\
\
def sendInvoiceEmail(event):\
    """This function send the issued invoice file link to a specified email address"""\
    ## request\uc0\u21442 \u25968  \u35774 \u32622 \
    print("------------send email----------------")\
    function_name = "send_invoice_email"\
    print(f"calling method: \{function_name\}")\
    print(f"Event: \\n \{json.dumps(event)\}")\
\
    invoice_code = get_named_parameter(event, 'invoice_code') \
    invoice_number = get_named_parameter(event, 'invoice_number')\
    email_address = get_named_parameter(event, 'email_address')\
\
    print ("parameters ==> ", "invoice_code:", invoice_code, "invoice_number:", invoice_number, "email_address:", email_address)\
    reqid = str(int(round(time.time() * 1000))) + "%03d" % random.randint(0, 999)\
    url = functions_configs[function_name]["url"]\
    params = \{"access_token" : getInvoiceToken(),"reqid" : reqid\}\
    header = \{\
        "Content-Type": "application/json"\
    \}\
    encrypt_key = functions_configs[function_name]["encrypt_key"]\
\
    data = \{\
        "invoiceCode":invoice_code,\
        "invoiceNo":invoice_number,\
        "email":email_address\
    \}\
\
    # \uc0\u25968 \u25454 \u21152 \u23494 \
    base64_cipher = encrypt(encrypt_key=encrypt_key, data=data)\
\
    response = requests.post(\
        url=url,\
        data=json.dumps(base64_cipher),\
        headers=header,\
        params=params\
    )\
    \
    result = response.json()\
\
    #\uc0\u23450 \u20041 \u36755 \u20986 \
    res = \{\}\
    res["input_args"] = \{\}\
    res["input_args"]["invoice_code"] = invoice_code\
    res["input_args"]["invoice_number"] = invoice_number\
    res["input_args"]["email_address"] = email_address\
    if result["errcode"] == "0000":\
        res["status"] = "success"\
        res["results"] = "\uc0\u37038 \u20214 \u21457 \u36865 \u25104 \u21151 "\
    else:\
        res["status"] = "fail"\
        res["results"] = "\uc0\u37038 \u20214 \u21457 \u36865 \u22833 \u36133 ,\u35831 \u31245 \u21518 \u23581 \u35797 \u37325 \u26032 \u21457 \u36865 ."\
    return res\
\
\
def lambda_handler(event, context):\
    \
    result = ''\
    response_code = 200\
    action_group = event['actionGroup']\
    api_path = event['apiPath']\
    \
    print ("lambda_handler == > api_path: ",api_path)\
    \
    if api_path == '/generatePreviewInvoiceImage':\
        result = generatePreviewInvoiceImage(event)\
    elif api_path == '/issueInvoice':\
        result = issueInvoice(event)\
    elif api_path == '/sendInvoiceEmail':\
        result = sendInvoiceEmail(event) \
    else:\
        response_code = 404\
        result = f"Unrecognized api path: \{action_group\}::\{api_path\}"\
\
    response_body = \{\
        'application/json': \{\
            'body': json.dumps(result)\
        \}\
    \}\
    \
    session_attributes = event['sessionAttributes']\
    prompt_session_attributes = event['promptSessionAttributes']\
    \
    print ("Event:", event)\
    action_response = \{\
        'actionGroup': event['actionGroup'],\
        'apiPath': event['apiPath'],\
        # 'httpMethod': event['HTTPMETHOD'], \
        'httpMethod': event['httpMethod'], \
        'httpStatusCode': response_code,\
        'responseBody': response_body,\
        'sessionAttributes': session_attributes,\
        'promptSessionAttributes': prompt_session_attributes\
    \}\
\
    api_response = \{'messageVersion': '1.0', 'response': action_response\}\
        \
    return api_response}