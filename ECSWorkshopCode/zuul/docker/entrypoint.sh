#!/bin/sh
export ECS_INSTANCE_IP_ADDRESS=$(curl --retry 5 --connect-timeout 3 -s  ${ECS_CONTAINER_METADATA_URI_V4} | /jq ".Networks[0].IPv4Addresses[0]")
export IP_ADDRESS=$(echo $ECS_INSTANCE_IP_ADDRESS | sed 's/\"//g')
exec java  -Deureka.instance.ip-address=${IP_ADDRESS} -Deureka.instance.instance-id=${IP_ADDRESS} -jar /zuul.jar
