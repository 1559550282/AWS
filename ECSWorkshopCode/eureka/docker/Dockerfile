FROM java:8 
COPY eureka-0.0.1-SNAPSHOT.jar eureka.jar
COPY entrypoint.sh .
RUN chmod +x /entrypoint.sh
EXPOSE 8761
ENTRYPOINT ["/entrypoint.sh"]
