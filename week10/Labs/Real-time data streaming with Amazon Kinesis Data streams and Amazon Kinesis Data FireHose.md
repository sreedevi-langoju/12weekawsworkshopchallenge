# Real-time data streaming with Amazon Kinesis Data streams and Amazon Kinesis Data FireHose

This blog guides you through the process of deploying a sample website on an EC2 Linux instance, utilizing the Apache web server, and capturing real-time website logs. These logs are then streamed to AWS S3 for storage and analysis using a combination of Kinesis Data Streams, Kinesis Agent, Kinesis Firehose, and S3.

By following this, you will have the opportunity to practice working with these AWS services and create a comprehensive data pipeline for processing website logs.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/2e104918-f972-4cda-9240-b9b40ebe8b88">

## Case Study

1.Suppose an application is running on the EC2 Instance and it is generating continuous logs.

2.Those logs will be pushed into the Kinesis Data Streams.

3.From the Kinesis Data Streams, it gets consumed through the Kinesis Firehose.

4.The data from Kinesis Firehose is then saved into the S3 Bucket.
