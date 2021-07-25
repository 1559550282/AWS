#!/bin/sh
export ECS_INSTANCE_IP_ADDRESS=$(curl --retry 5 --connect-timeout 3 -s  ${ECS_CONTAINER_METADATA_URI_V4} | /jq ".Networks[0].IPv4Addresses[0]")
export IP_ADDRESS=$(echo $ECS_INSTANCE_IP_ADDRESS | sed 's/\"//g')
curl -H "Accept: text/html, application/xhtml+xml, application/json;q=0.9, */*;q=0.8" http://springdemo-946701722.cn-northwest-1.elb.amazonaws.com.cn/eureka/apps/PROVIDER/$IP_ADDRESS | /jq -e '.instance.status=="UP"'
