#!/bin/bash
## run on gateway 节点

## please input the bucket where the emr files are saving.
export bucket=****

##
sudo rm -rf /etc/spark/conf/*
sudo rm -rf /etc/hadoop/conf/*
sudo rm -rf /etc/hadoop/hive/*
sudo rm -rf /usr/share/aws/*
sudo rm -rf /usr/lib/spark/jars/*
sudo rm -rf /usr/lib/hadoop-lzo/*
sudo rm -rf /usr/lib/hive/*
sudo rm -rf /etc/yum.repos.d/*
sudo rm -rf /var/aws/emr/repoPublicKey.txt
sudo mkdir -p /var/aws/emr/
sudo mkdir -p /etc/hadoop/conf sudo mkdir -p /etc/spark/conf
sudo mkdir -p /etc/hive/conf
sudo mkdir -p /var/log/spark/user/ sudo mkdir -p /var/log/spark/
sudo mkdir -p /var/log/hadoop/ sudo mkdir -p /var/log/hive/
sudo chmod 777 -R /var/log/spark/
sudo chmod 777 -R /var/log/hadoop/
sudo chmod 777 -R /var/log/hive/
sudo chmod 777 /mnt /mnt1
sudo aws s3 cp s3://${bucket}/path/to/copy/repo/ /etc/yum.repos.d/ --recursive
sudo aws s3 cp s3://${bucket}/path/to/copy/key/repoPublicKey.txt /var/aws/emr/repoPublicKey.txt
sudo groupadd hadoop
sudo useradd hadoop -g hadoop
sudo yum install -y java-1.8.0-openjdk sudo yum install -y hadoop-client
sudo yum install -y hadoop-hdfs
sudo yum install -y spark-core
sudo yum install -y hadoop
sudo yum install -y hive
#还需要添加 hive
sudo aws s3 cp s3://${bucket}/path/to/copy/spark/ /etc/spark/conf --recursive
sudo aws s3 cp s3://${bucket}/path/to/copy/hadoop/ /etc/hadoop/conf --recursive
sudo aws s3 cp s3://${bucket}/path/to/copy/hive/ /etc/hadoop/hive --recursive
sudo aws s3 cp s3://${bucket}/path/to/copy/usr_share_aws/ /usr/share/aws/ --recursive
sudo aws s3 cp s3://${bucket}/path/to/copy/lib_spark_jars/ /usr/lib/spark/jars/ --recursive
sudo aws s3 cp s3://${bucket}/path/to/copy/hadoop-lzo/ /usr/lib/hadoop-lzo --recursive
sudo aws s3 cp s3://${bucket}/path/to/copy/hive/ /usr/lib/hive/ --recursive
sudo aws s3 cp s3://${bucket}/path/to/copy/tez/ /usr/lib/tez/  --recursive
sudo aws s3 cp s3://${bucket}/path/to/copy/hcatalog/ /usr/lib/hive-hcatalog/share/hcatalog/ --recursive
sudo aws s3 cp  s3://${bucket}/path/to/copy/hadoop-lzo/  /usr/lib/hadoop-lzo/lib/ --recursive
sudo aws s3 cp s3://${bucket}/path/to/copy/tez-conf/ /etc/tez/conf  --recursive

sudo chmod -R 755 /usr/lib/hive
sudo mkdir -p /var/log/hive/user/hadoop/
sudo chmod -R 755 /var/log/hive/user/hadoop/
sudo chmod -R 755 /etc/hive/conf/hive-log4j2.properties
sudo mkdir -p /var/log/hive/user/hadoop/
sudo chown hadoop -R /var/log/hive/user/hadoop/
sudo chown hadoop -R /etc/hive/conf/hive-log4j2.properties

sudo rm -rf /usr/lib/flink/*
sudo rm -rf /etc/flink/conf/*
sudo chmod 777 -R /var/log/flink/
sudo chmod 777 -R /var/log/flink-cli/
sudo yum install -y flink
sudo aws s3 cp s3://${bucket}/path/to/copy/flink/ /etc/flink/conf --recursive
sudo aws s3 cp s3://${bucket}/path/to/copy/flink-lib/ /usr/lib/flink --recursive
sudo chmod -R 755 /usr/lib/flink