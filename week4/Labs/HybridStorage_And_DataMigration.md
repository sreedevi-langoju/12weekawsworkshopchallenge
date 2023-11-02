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

  
### Before you can start working on the exercises in each lab, you need to deploy the proper resources. Please check the labsetup.md file in this repository.


## Step 1: Creating Primary and Secondary S3 Buckets

Before you configure the File Gateway, you must create the primary S3 bucket (or the source) where you will replicate the data. You will also create the secondary bucket (or the destination) that will be used for cross-Region replication.

1. Open the AWS Management Console and navigate to the S3 service.
2. Create the primary S3 bucket in the US East (Ohio) region with versioning enabled.
   * Bucket name: Create a name . It must be globally unique. Ex: migrationdata-primary-bucket
   * Region: US East (Ohio) us-east-2
   * Bucket Versioning: Enable

      Note :  For cross-Region replication, you must enable versioning for both the source and destination buckets.
     
 <img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/667e40d8-652b-4505-bb7a-d5ad979e0328" height="300" width="500">

 3. Create a second bucket in the US West (Oregon) region with versioning enabled.
   * Bucket name: Create a name . It must be globally unique. Ex: migrationdata-crr-bucket
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

      <img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/2814d019-8688-4b98-88f5-ca70069dcab1" height="400" width="500">
      <img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/daec1783-e274-4953-9343-169b91fded8a" height="400" width="500">
  
3. A new tab opens to the EC2 instance launch wizard. This link automatically selects the correct Amazon Machine Image (AMI) that must be used for the File Gateway appliance.
   
4. In the Launch an instance screen, begin configuring the gateway as described:

    * Name: File Gateway Appliance

    * AMI from catalog: Accept the default aws-storage-gateway AMI.
  
    * Instance type: Select the t2.xlarge instance type
      
    * Key pair name - required: choose the existing vockey key pair.
      
    * Configure the network and security group settings for the gateway.

        Next to Network settings, choose Edit, then configure: 

        * VPC: On-Prem-VPC
        * Subnet: On-Prem-Subnet
        * Auto-assign public IP: Enable
        * Under Firewall (security groups), choose  Select an existing security group.
          
             * Select the security group with <b> FileGatewayAccess </b> in the name

          Note: This security group is configured to allow traffic through ports 80 (HTTP), 443 (HTTPS), 53 (DNS), 123 (NTP), and 2049 (NFS). These ports                   enable the activation of the File Gateway appliance. They also enable connectivity from the Linux server to the NFS share that you will create on                the File Gateway.
          
             * Also select the security group with OnPremSshAccess in the name

          Note: This security group is configured to allow Secure Shell (SSH) connections on port 22.

            Verify that both security group now appear as selected (details on each will appear in boxes             in the console). 

          Tip: You may need to choose Show all selected to see them both.
          
          <img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/2c29455f-d0b7-4144-85bc-324f277eb14b"  height="500" width="500">

          
    * Configure the storage settings for the gateway.In the Configure storage panel, notice there is already an entry to create one 80GiB root volume.
      Choose Add new volume. Set the size of the EBS volume to 150GiB.

    * Finish creating the gateway.

    * In the Summary panel on the right, keep the number of instances set to 1, and choose Launch instance

    * A Success message displays.Choose View all instances

    * Your File Gateway Appliance instance will take a few minutes to initialize.
      
    * Monitor the status of the deployment and wait for Status Checks to complete.

       Tip: Choose the refresh  button to more quickly learn the status of the instance.
      
    * Select your File Gateway instance, then in the Details tab below, locate the Public IPv4 address and copy it. 

    * You will use this IP address when you complete the File Gateway deployment.

 5. Return to the AWS Storage Gateway tab in your browser. It should still be at the Set up gateway on Amazon EC2 screen.
    
 6. Check the box next to I completed all the steps above and launched the EC2 instance, then choose Next

 7. Configure the Step 2: Connect to AWS settings:

    * In the Gateway connection options:

    * For IP address, paste in the IPv4 Public IP address that you copied from your File Gateway Appliance instance
    * For the Service endpoint, select Publicly accessible. Choose Next
      
 8.  In the Step 3: Review and activate settings screen choose Activate gateway
    
     <img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/b4bc50f1-8a75-42b6-bb61-701d064a1dad"  height="500" width="500">
 
 10. Configure the Step 4: Configure gateway settings:

     * CloudWatch log group: Deactivate logging

     * CloudWatch alarms: No Alarm

  <img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/3161f3a5-d588-4f28-908f-860fa75ed9d9"  height="500" width="500">

 11. A Successfully activated gateway File Gateway Appliance message displays.
     
 12. In the Configure cache storage panel, you will see that a message the local disks are loading. Wait for the local disks status to show that it finished processing (approximately 1 minute).Choose Configure


 13. Start creating a file share. Wait for File Gateway status to change to Running.
     * From the left side panel, choose File shares.
     * Choose Create file share.
       
     <img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/9b1fc5fd-f313-4668-995b-2a941bb39b6a">

     
 14. On the Create file share screen, configure these settings:

     * Gateway: Select the name of the File Gateway that you just created (which should be File Gateway Appliance)
     * File share protocol: NFS
     * Amazon S3 bucket name: Choose the name of the source bucket that you created in the US East (Ohio) us-east-2 Region in Task 1.
     * Choose Customize configuration
     * For File share name use share and choose Next.
    
  <img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/c5b0a24a-ba94-4bb9-9c6b-ac1fed564cbe"  height="500" width="500" >
    
 15. On the Amazon S3 storage settings screen, configure these settings:

     * Storage class for new objects: S3 Standard
     * Select checkbox Object metadata: Guess MIME type
     * Select checkbox Gateway files acccessible to S3 bucket owner

     * Access your S3 bucket: Use an existing IAM role

     * IAM role: Paste the FgwIamPolicyARN, which you previously created  – Choose Next
       
 <img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/4d4dd7cf-d297-4c4d-b86e-bb1b16c85e3a"  height="500" width="500">

 16. In the File access settings screen, accept the default settings.

      Note: You might get a warning message that the file share is accessible from anywhere. For this lab, you can          safely disregard this warning.
     
 17. Scroll to the bottom of the Review and create screen, then select Create 

     Monitor the status of the deployment and wait for Status to change to Available, which takes less than a minute.

 18. At the bottom of the screen, note the command to mount the file share on Linux. You will need it for the next 
     task.

  <img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/5c8da6ba-d058-431f-b16c-2d59708ee0d6">


  ## Step 4 :Mounting the file share to the Linux instance and migrating the data
  
  Before you can migrate data to the NFS share that you created, you must first mount the share. In this task, you will mount the NFS share on a Linux server, then copy data to the share.

  1. SSH into the On-Prem Linux Server instance.(Pre created Linux Ec2 instance)
     
      Note : Refer to <b> SSH_Into_Linux_Instance.md</b> file in this repository on how to ssh into Linux EC2 instance
     
  3. On the Linux instance, to view the data that exists on this server, enter the following command:

         ls /media/data
     
     You should see 20 image files in the .png format.

     
  4. Create the directory that will be used to synchronize data with your S3 bucket by using the following command:

         sudo mkdir -p /mnt/nfs/s3

     <img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/6e4c798e-477a-40db-90c1-1eb43b47108b"  height="500" width="500">

  5. Mount the file share on the Linux instance by using the command that you located in the Storage Gateway file shares details screen at the end of the last task.

         sudo mount -t nfs -o nolock,hard <File-Gateway-appliance-private-IP-address>:/share /mnt/nfs/s3

     Ex: sudo mount -t nfs -o nolock,hard 10.10.1.33:/share /mnt/nfs/s3
     
  6. Verify that the share was mounted correctly by entering the following command:
    
         df -h

  7. Now that you created the mount point, you can copy the data that you want to migrate to Amazon S3 into the share by using this command:

          cp -v /media/data/*.png /mnt/nfs/s3

    
 <img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/d4d11415-709a-4e37-8078-caf8be216e02" height="400" width="400">


 ## Step 5: Verifying that the data is migrated
 
You have finished configuring the gateway and copying data into the NFS share. Now, you will verify that the configuration works as intended.

In the  Services search box, search for and choose S3 to open the S3 console.

Select the bucket that you created in the US East (Ohio) Region.

Verify that the 20 image files are listed.

Note: You might need to choose the refresh  icon in the S3 console.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/8b6dd39d-592c-4667-9749-9993ecea2240" >


Return to the Buckets page and select the bucket that you created in the US West (Oregon) Region. 

Verify that the images files were replicated to this bucket, based on the policy that you created earlier.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/3445ce58-48c6-479f-bb38-461778eed19e">


Note: S3 Object replication can take up to 15 minutes to complete. Keep refreshing until you see the replicated objects. 

 

Congratuations, you successfully migrated data to Amazon S3 by using AWS Storage Gateway in File Gateway mode! After your data is stored in Amazon S3, you can act on it like native Amazon S3 data. In this lab, you created a replication policy to copy the data to a secondary Region. You could also perform other operations, such as configuring a lifecycle policy. For example, you could migrate infrequently used data automatically from S3 Standard to Amazon Simple Storage Service Glacier for long-term storage, which can reduce costs. Don't forget to delete the configured resources when they are no longer needed to avoid unnecessary billing.


   


