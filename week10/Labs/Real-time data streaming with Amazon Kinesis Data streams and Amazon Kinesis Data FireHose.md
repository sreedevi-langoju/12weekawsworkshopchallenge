# Real-time data streaming with Amazon Kinesis Data streams and Amazon Kinesis Data FireHose

This blog guides you through the process of deploying a sample website on an EC2 Linux instance, utilizing the Apache web server, and capturing real-time website logs. These logs are then streamed to AWS S3 for storage and analysis using a combination of Kinesis Data Streams, Kinesis Agent, Kinesis Firehose, and S3.

By following this, you will have the opportunity to practice working with these AWS services and create a comprehensive data pipeline for processing website logs.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/2e104918-f972-4cda-9240-b9b40ebe8b88">

## Case Study

1.Suppose an application is running on the EC2 Instance and it is generating continuous logs.

2.Those logs will be pushed into the Kinesis Data Streams.

3.From the Kinesis Data Streams, it gets consumed through the Kinesis Firehose.

4.The data from Kinesis Firehose is then saved into the S3 Bucket.



## Task 1: Sign in to AWS Management Console

Once Signed In to the AWS Management Console, Make the default AWS Region as US East (N. Virginia) us-east-1.

## Task 2: Launching an EC2 Instance

Make sure you are in US East (N. Virginia) us-east-1 Region. 

Navigate to EC2 by clicking on the Services menu at the top, then click on EC2 in the Compute section.

Navigate to Instances on the left panel and click on Launch Instance button.

 Enter Name as Demo_Instance

 Select Amazon Linux from the Quick Start.

Choose an Amazon Machine Image (AMI): Choose Amazon Linux 2 AMI(HVM) from the drop-down.

Choose an Instance Type: Select t2.micro 

For Key pair : Choose Create a new key pair

Key Pair name :  Enter  WhizKey
Key pair type : Choose RSA
Private key file format: Choose .pem
Click on Create key pair button.
In Network Settings Click on Edit Button:

Auto-assign public IP: Select Enable
Select Create new Security group
Security group name : Enter kinesis_demo_SG
Description : Enter Security Group to allow traffic to EC2
SSH rule will already be present for you. To add HTTP:
 
Select Add Security rule Button
Choose Type: HTTP 
Source:  Select Anywhere
Under Advanced Details,
IAM Instance profile : Select EC2_Role_<RANDOM_NUMBER>
