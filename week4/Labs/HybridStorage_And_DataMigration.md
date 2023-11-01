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

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/15211fc1-5b7f-480c-a191-825873c02576" height="300" width="500">

4. Return to and select the link to the bucket you created in the US East (Ohio) Region.
   
5. Choose Upload to upload a file from your local computer to the bucket.( You can download the attached png file to upload )

6. Choose Add files, locate and open the file, then choose Upload 
7. Wait for the file to upload, then choose Close. 

 <img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/b8cf1e65-77f9-4707-819c-3aa00e42379d">

8. Return to the bucket you created in the <b> US West (Oregon) Region </b>.The file that you uploaded should also now have been copied to this bucket.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/b0dc64f2-451a-46ca-9fd2-79c0e9c51fae">

  Note: You may need to refresh  the console for the object to appear.



## Step 3: Configuring the File Gateway and creating an NFS file share

In this task, you will deploy the File Gateway appliance as an Amazon Elastic Compute Cloud (Amazon EC2) instance. You will then configure a cache disk, select an S3 bucket to synchronize your on-premises files to, and select an IAM policy to use. Finally, you will create an NFS file share on the File Gateway.

1. In the search box to the right of  Services, search for and choose Storage Gateway to open the Storage Gateway console.
 
2. At the top-right of the console, verify that the current Region is N. Virginia.

   Choose Create gateway then begin configuring the Step 1: Set up gateway settings:

    * Gateway name: File Gateway

    * Gateway time zone: Choose GMT -5:00 Eastern Time (US & Canada), Bogota, Lima

    * Gateway type: Amazon S3 File Gateway

    * Host platform: choose <b>Amazon EC2</b>. Choose <b>Customize your settings</b>. Then choose the <b>Launch instance</b> button.

      <img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/2814d019-8688-4b98-88f5-ca70069dcab1">
      <img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/daec1783-e274-4953-9343-169b91fded8a">
  
3. A new tab opens to the EC2 instance launch wizard. This link automatically selects the correct Amazon Machine Image (AMI) that must be used for the File Gateway appliance.
   
4. In the Launch an instance screen, begin configuring the gateway as described:

    * Name: File Gateway Appliance

    * AMI from catalog: Accept the default aws-storage-gateway AMI.
  
    * Instance type: Select the t2.xlarge instance type



