package org.example;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.concurrent.ExecutionException;

public class App {
    private static final Logger logger = LoggerFactory.getLogger(App.class);

    public static void main(String... args) {
        logger.info("Application starts");

        final bedrockDemoStream client = new bedrockDemoStream();
        try {
            client.runStream(); 
          } catch (ExecutionException e) {
            logger.info("runStream ExecutionException");
          } catch (InterruptedException e) {
            logger.info("runStream InterruptedException");
          }
        

        logger.info("Application ends");
    }
}