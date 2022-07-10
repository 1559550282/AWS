#!/bin/bash
## run on master 节点

## please input the s3 bucket for temporary saving directory.
export bucket=****
##
aws s3 rm s3://${bucket}/path/to/copy/ --recursive
aws s3 cp /etc/yum.repos.d/ s3://${bucket}/path/to/copy/repo/ --recursive
aws s3 cp /var/aws/emr/repoPublicKey.txt s3://${bucket}/path/to/copy/key/
aws s3 cp /etc/spark/conf s3://${bucket}/path/to/copy/spark/ --recursive
aws s3 cp /etc/hadoop/conf s3://${bucket}/path/to/copy/hadoop/ --recursive
aws s3 cp /etc/hadoop/hive s3://${bucket}/path/to/copy/hive/ --recursive
aws s3 cp /usr/share/aws/ s3://${bucket}/path/to/copy/usr_share_aws/ --recursive
aws s3 cp /usr/lib/spark/jars s3://${bucket}/path/to/copy/lib_spark_jars/ --recursive
aws s3 cp /usr/lib/hadoop-lzo s3://${bucket}/path/to/copy/lib_hadoop_lzo/ --recursive
aws s3 cp /usr/lib/hive s3://${bucket}/path/to/copy/hive/ --recursive
aws s3 cp /usr/lib/tez s3://${bucket}/path/to/copy/tez/ --recursive
aws s3 cp /usr/lib/hive-hcatalog/share/hcatalog s3://${bucket}/path/to/copy/hcatalog/ --recursive
aws s3 cp /usr/lib/hadoop-lzo/lib/ s3://${bucket}/path/to/copy/hadoop-lzo/ --recursive
aws s3 cp /etc/tez/conf  s3://${bucket}/path/to/copy/tez-conf/ --recursive
aws s3 cp /etc/flink/conf  s3://${bucket}/path/to/copy/flink/ --recursive
aws s3 cp /usr/lib/flink  s3://${bucket}/path/to/copy/flink-lib/ --recursive