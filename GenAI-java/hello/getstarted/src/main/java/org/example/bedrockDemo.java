package org.example;
import software.amazon.awssdk.core.SdkBytes;
import software.amazon.awssdk.services.bedrockruntime.BedrockRuntimeClient;
import software.amazon.awssdk.services.bedrockruntime.model.*;
import java.util.concurrent.ExecutionException;


public class bedrockDemo {
    private final BedrockRuntimeClient demoClient = BedrockRuntimeClient.create();
    public void runStream() throws ExecutionException, InterruptedException {
        String bodyString ="{\"prompt\": \"\\n\\nHuman:Hello\\n\\nAssistant:\", \"max_tokens_to_sample\": 100}";
        SdkBytes bodyBytes = SdkBytes.fromUtf8String(bodyString);
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