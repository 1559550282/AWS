import boto3
import botocore
import json
import time
import logging
from flask import Flask, request, Response
from IPython.display import clear_output, display, display_markdown, Markdown

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    "%(asctime)s - %(process)d - %(levelname)s - %(filename)s:%(lineno)s - %(message)s"
)
sh = logging.StreamHandler()
sh.setFormatter(formatter)
logger.addHandler(sh)
model_name = "claude2"
app = Flask(__name__)
# print(boto3.__version__)
# print(botocore.__version__)

bedrock_client = boto3.client(service_name='bedrock-runtime', region_name='us-east-1', endpoint_url='https://bedrock-runtime.us-east-1.amazonaws.com')

def format_output(text, chat_id, create_time, is_first=False, is_last=False):
    if is_first:
        return {"id":chat_id,"object":"chat.completion.chunk","created":create_time,"model":model_name,"choices":[{"index":0,"finish_reason":None,"delta":{"role":"assitant"}}], "usage":None}
    elif is_last:
        return {"id":chat_id,"object":"chat.completion.chunk","created":create_time,"model":model_name,"choices":[{"index":0,"finish_reason":"stop","delta":{}}],"usage":None}
    return {"id":chat_id,"object":"chat.completion.chunk","created":create_time,"model":model_name,"choices":[{"index":0,"finish_reason":None,"delta":{"content": text}}],"usage":None}

@app.route('/nlpservice/{}'.format(model_name), methods=['POST'])
def index():
    instructions = request.json.get('instructions')
    inputs = request.json.get('inputs', ['']*len(instructions))
    max_tokens_to_sample = request.json.get('max_lens', [2048])
    temperature = request.json.get('temperatures', 0.5)
    top_k = request.json.get('top_k', 250)
    top_p = request.json.get('top_p', 1)
    stop_sequences = request.json.get('stop_sequences', ["\n\nHuman:"])
    trace_id = request.json.get('trace_id', "123")
    stream = request.json.get('stream', False)
    # prompt_data = app.current_request.json_body.get('prompt_data')


    # body = json.dumps({"inputText": prompt_data})
    # can switch to any model that Bedrock supports
    modelId = "anthropic.claude-v2"
    # modelId = "amazon.titan-tg1-large"
    accept = "application/json"
    # accept = "*/*"
    contentType = "application/json"
    # output_text = bedrock_client.list_foundation_models()

    chat_id = trace_id
    logger.info(f"chat_id {chat_id}")
    logger.info(f"processing {instructions}")
    logger.info(f"temperatures: {temperature}, max_lens: {max_tokens_to_sample}, stream_mode: {stream}")
    create_time = int(time.time())
    if not inputs:
        inputs = [""] * len(instructions)
    output = []
    for instructions, _input, temperature, max_tokens_to_sample in zip(instructions, inputs, temperature, max_tokens_to_sample):
        # prompt = _input + '\n\n' + 'Human:' + instructions + 'Assistant:' if _input != '' else 'Human:' + instructions + 'Assistant:'
        body = json.dumps({"prompt": _input + '\n\n' + 'Human:' + instructions + 'Assistant:' if _input != '' else 'Human:' + instructions + 'Assistant:',
                           "max_tokens_to_sample": max_tokens_to_sample,
                           "temperature": temperature,
                           "top_k": top_k,
                           "top_p": top_p,
                           "stop_sequences": stop_sequences})

        if stream == "true":
            response = bedrock_client.invoke_model_with_response_stream(
                body=body, modelId=modelId, accept=accept, contentType=contentType
            )
            stream = response.get("body")

            def stream_test():
                if stream:
                    for event in stream:
                        chunk = event.get('chunk')
                        text = " "
                        if chunk:
                            chunk_obj = json.loads(chunk.get('bytes').decode())
                            text = chunk_obj['completion']
                            # clear_output(wait=True)
                            # print(text)
                            # return {'results': output}
                        yield "data: " + json.dumps(format_output("", chat_id, create_time, is_first=True),
                                                    ensure_ascii=False) + "\n\n"
                        last_chunk = ""
                        for chunk in text:
                            yield "data: " + json.dumps(
                                format_output(chunk[0].replace(last_chunk, ""), chat_id, create_time),
                                ensure_ascii=False) + "\n\n"
                            last_chunk = chunk[0]
                        yield "data: " + json.dumps(format_output("", chat_id, create_time, is_last=True),
                                                    ensure_ascii=False) + "\n\n"
                        yield "data: [DONE]"

            logger.info("time cost: %.3fs" % (time.time() - create_time))
            return Response(stream_test(), mimetype="text/event-stream")
        else:
            response = bedrock_client.invoke_model(
                body=body, modelId=modelId, accept=accept, contentType=contentType
            )
            response_body = json.loads(response.get("body").read())
        # # response_body = json.loads(response)
        # # generated_text = response_body["completions"][0]["data"]["text"]
            output = response_body.get("completion")
            logger.info("time cost: %.3fs" % (time.time() - create_time))
            logger.info(output)
    return {'results': output}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8501)