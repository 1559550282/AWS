FROM java:8 
COPY zuul-0.0.1-SNAPSHOT.jar zuul.jar
COPY jq-linux64 jq
COPY entrypoint.sh .
RUN chmod +x /entrypoint.sh
RUN chmod +x /jq
EXPOSE 8030
ENTRYPOINT ["/entrypoint.sh"]
