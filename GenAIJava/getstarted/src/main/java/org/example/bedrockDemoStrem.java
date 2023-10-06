package org.example;
import software.amazon.awssdk.core.SdkBytes;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.bedrockruntime.BedrockRuntimeAsyncClient;
import software.amazon.awssdk.auth.credentials.DefaultCredentialsProvider;
import software.amazon.awssdk.services.bedrockruntime.model.*;
import java.net.URI;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.ExecutionException;


public class bedrockDemoStrem {
    
    private final BedrockRuntimeAsyncClient bedrockClient = BedrockRuntimeAsyncClient.builder()
                .endpointOverride(URI.create("https://bedrock-runtime.us-east-1.amazonaws.com"))
                .region(Region.US_EAST_1)
                .credentialsProvider(DefaultCredentialsProvider.create())
                .build();
    
    //private final BedrockRuntimeAsyncClient bedrockClient = BedrockRuntimeAsyncClient.create();
    public void runStream() throws ExecutionException, InterruptedException {
        //final String prompt = "{\"inputText\": \"write an essay for living on mars in1000 words\", " +"\"textGenerationConfig\": {\"maxTokenCount\": 2000}}";
        final String bodyString = "{\"prompt\": \"\\n\\nHuman:write an essay for living on mars in 1000 words\\n\\nAssistant:\", \"max_tokens_to_sample\": 2000}";
        SdkBytes bodyBytes = SdkBytes.fromUtf8String(bodyString);
        try {
            InvokeModelWithResponseStreamRequest request = InvokeModelWithResponseStreamRequest.builder()
                                                    .accept("application/json") 
                                                    .body(bodyBytes) 
                                                    .contentType("application/json") 
                                                    .modelId("anthropic.claude-v2")
                                                    .build(); 
            InvokeModelWithResponseStreamResponseHandler handler = InvokeModelWithResponseStreamResponseHandler.builder()
                                                    .onEventStream(publisher ->publisher.subscribe(bedrockDemoStrem::processEvent))
                                                    .build();
            bedrockClient.invokeModelWithResponseStream(request, handler).get();
            
        } 
        catch (ExecutionException e) {
                System.out.println("InvokeModelWithResponseStreamRequest ExecutionException");
            } 
        catch (InterruptedException e) {
                System.out.println("InvokeModelWithResponseStreamRequest InterruptedException");
            }
        
}
        
    
    private static void processEvent(ResponseStream event) {
            if (event instanceof PayloadPart) {
                final PayloadPart payloadPart = (PayloadPart) event;
                final String message =
                             StandardCharsets.UTF_8.decode(payloadPart.bytes().asByteBuffer()).toString();
                            System.out.println(message);
            }
} 
}


