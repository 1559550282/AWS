FROM java:8 
COPY demo-0.0.1-SNAPSHOT.jar demo.jar
COPY jq-linux64 jq
COPY entrypoint.sh .
COPY hc.sh .
RUN chmod +x /entrypoint.sh
RUN chmod +x jq
RUN chmod +x hc.sh
EXPOSE 8010
ENTRYPOINT ["/entrypoint.sh"]
