#!/bin/sh
#export ECS_INSTANCE_IP_ADDRESS=$(curl ${ECS_CONTAINER_METADATA_URI_V4} | jq ".Networks[0].IPv4Addresses[0]")
exec java  -jar /eureka.jar
