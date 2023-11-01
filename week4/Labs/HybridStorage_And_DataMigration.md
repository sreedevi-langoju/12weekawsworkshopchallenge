# Hybrid Storage and Data Migration with AWS Storage Gateway File Gateway

Introduction:
In this lab, I will walk you through the process of setting up an AWS Storage Gateway File Gateway to facilitate hybrid storage and data migration. This lab helps you configure a File Gateway with an NFS file share, attach it to a Linux instance, and migrate data to an Amazon S3 bucket. You will also see how to configure advanced Amazon S3 features, including lifecycle policies and cross-Region replication.

In this lab, you will :

* Configure a File Gateway with an NFS file share and attach it to a Linux instance
* Migrate a set of data from the Linux instance to an S3 bucket
* Create and configure a primary S3 bucket to migrate on-premises server data to AWS
* Create and configure a secondary S3 bucket to use for cross-Region replication
* Create an S3 lifecycle policy to automatically manage data in a bucket
  
 Let's get started:

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/b05f35f2-a9e3-4ed8-b685-5ddc5388f075" height="600" width="800">

* This lab utilizes three AWS Regions.
* A Linux EC2 instance emulating an on-premises server is deployed in the us-east-1 (N. Virginia) Region.
* The Storage Gateway virtual appliance is also deployed in the same Region as the Linux server.
* The primary S3 bucket (source) is created in the us-east-2 (Ohio) Region.
* The secondary S3 bucket (destination) is created in the us-west-2 (Oregon) Region.

## Step 1: Creating Primary and Secondary S3 Buckets

Before you configure the File Gateway, you must create the primary S3 bucket (or the source) where you will replicate the data. You will also create the secondary bucket (or the destination) that will be used for cross-Region replication.

1. Open the AWS Management Console and navigate to the S3 service.
2. Create the primary S3 bucket in the US East (Ohio) region with versioning enabled.
   * Bucket name: Create a name . It must be globally unique. Ex: 
   * Region: US East (Ohio) us-east-2
   * Bucket Versioning: Enable

     Note :  For cross-Region replication, you must enable versioning for both the source and destination buckets.
 <img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/667e40d8-652b-4505-bb7a-d5ad979e0328" height="300" width="500">

 3. Create a second bucket in the US West (Oregon) region with versioning enabled.
   * Bucket name: Create a name . It must be globally unique. Ex: 
   * Region: US West (Oregon) us-west-2
   * Bucket Versioning: Enable
  <img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/25ddff80-152d-4b36-871a-91cf5b1c6d92" height="300" width="500">


## Step 2: Enabling Cross-Region Replication

1. Select the primary (source) bucket in the US East (Ohio) Region.
2. Go to the Management tab and create a replication rule.
    * Replication rule name: crr-full-bucket
    * Status : Enabled
    * Source bucket:
       * For Choose a rule scope, select  Apply to all objects in the bucket
    * Destination:
       * Choose a bucket in this account
       * Choose Browse S3 and select the bucket you created in the US West (Oregon) Region.
       * Select Choose path
       * IAM role: S3-CRR-Role(This was pre-created IAM role with required permissions)

3. Save the rule and choose not to replicate existing objects.
   <img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/4927a0fc-706a-4033-9981-026001c3b3f9">

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/de478cfe-76de-4883-89e7-3b20f58cde35" height="300" width="500">

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/15211fc1-5b7f-480c-a191-825873c02576"height="300" width="500">

