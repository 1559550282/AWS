# EMR Client Deploy Guide

## 1. Deploy Guide

This project is used to set up a gateway for AWS EMR.
After sshing to this gateway , you can use  command such as spark-submit, hive, beeline, hadoop, flink run etc.

How to setup ?  Tthere are several steps to set up

Prerequisit:
You already setted up an AWS EMR.Then

***1 launch an EC2 instance as a gateway instance， in the same VPC as EMR use

***2 Configure EMR Security Group inbound rules, including master, core's security group.
Let the gateway instance can send traffic to emr nodes.

***3 you need an S3 bucket(Setup a new one, or use an existing one thant you own) for temporary saving files. Copy the s3 bucket name.

***4 ssh the EMR master node, upload the emr.sh .
Modiy the emr.sh , input the correct s3 bucket name that you copied in the previous step.
Run the emr.sh

***5 configure the gateway.

ssh the gateway instance

Use command:AWS configure

Then Input the region , AKSK. (You can get acesskey secretkey in IAM user configuration)

Make sure you can use aws s3 command

Modify the gateway.sh, input the correct s3 bucket name

Run the gateway.sh

***6 Done and Test
Check the hadoop commanHow to Use command:

## 2. 视频演示

<a href="https://www.bilibili.com/video/BV1uN4y1u7Nd/" title="EMR client demo"><img src="https://github.com/1559550282/AWS/blob/main/EMRClient/image/EMRClient.png" alt="Alternate Text" /></a>

