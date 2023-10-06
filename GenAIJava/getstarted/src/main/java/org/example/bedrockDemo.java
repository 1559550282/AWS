package org.example;
import software.amazon.awssdk.core.SdkBytes;
import software.amazon.awssdk.services.bedrockruntime.BedrockRuntimeClient;
import software.amazon.awssdk.services.bedrockruntime.model.*;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.ExecutionException;


public class bedrockDemo {
    private final BedrockRuntimeClient demoClient = BedrockRuntimeClient.create();
    
    //private final BedrockRuntimeAsyncClient bedrockClient = BedrockRuntimeAsyncClient.create();
    public void runStream() throws ExecutionException, InterruptedException {
        //final String prompt = "{\"inputText\": \"write an essay for living on mars in1000 words\", " +"\"textGenerationConfig\": {\"maxTokenCount\": 2000}}";
        //final String prompt = "{\"prompt\": \"\n\nHuman:write an essay for living on mars in 1000 words\n\nAssistant:\", " +"\"max_tokens_to_sample\": 2000}";
        //final String prompt = "{\"prompt\": \"\n\nHuman:write an essay for living on mars in 1000 words.\n\nAssistant:\"}";
        String bodyString ="{\"prompt\": \"\\n\\nHuman:Hello\\n\\nAssistant:\", \"max_tokens_to_sample\": 100}";
        SdkBytes bodyBytes = SdkBytes.fromUtf8String(bodyString);
        //System.out.println(prompt);
      
        InvokeModelRequest request = InvokeModelRequest.builder()
                                                .accept("application/json") 
                                                //.body(SdkBytes.fromString(prompt, StandardCharsets.UTF_8)) 
                                                .body(bodyBytes)
                                                .contentType("application/json") 
                                                .modelId("anthropic.claude-v2")
                                                .build(); 
        InvokeModelResponse response = demoClient.invokeModel(request); 
        System.out.println(response.body().asUtf8String());
    }
}