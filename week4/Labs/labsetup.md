## Lab Kickstart: Prerequisites and Resource Setup Guide

Before diving into our Hybrid Storage and Data Migration lab, it's crucial to lay the groundwork and set up the essential resources that will pave the way for a successful and seamless hands-on experience. In this guide, we'll walk you through the prerequisites and resources you need to have in place before you can embark on the lab. Please create the following resources to ensure a smooth journey:

### 1. IAM Roles:
IAM (Identity and Access Management) roles are integral to securely managing access to AWS resources. We'll create two specific IAM roles tailored to the lab's requirements.

### 2. VPC Configuration:

We need to set up a Virtual Private Cloud (VPC) with a public subnet and other VPC components. These form the foundation for our lab. Don't worry; we'll guide you through the process step by step.

### 3. Security Groups:
Security is paramount, and for that, we'll configure security groups to control inbound and outbound traffic to your instances.

### 4. EC2 Instance in the Created VPC:
Additionally, you'll need to launch an EC2 instance within the created VPC, which will be a core component of our lab exercises.


These are the prerequisites that you should have in place before proceeding with the lab. 

### 1 : IAM Roles and Permissions Creation:

   You need to create two IAM roles one for S3 Cross-Region Replication and another for S3 File Gateway

   #### To create an IAM role for S3 Cross-Region Replication:

      * Go to IAM in the AWS Console.
      * Create a role with the use case "S3 - Cross-Region Replication."
      * Attach a custom policy with the required S3 CRR permissions.
      * Review and create the role, naming it "S3-CRR-Role"

   This policy grants the required permissions for S3 CRR:
   
     {
        "Version": "2012-10-17",
        "Statement": [
          {
            "Effect": "Allow",
            "Action": [
              "s3:GetReplicationConfiguration",
              "s3:ListBucket",
              "s3:GetObjectVersionForReplication",
              "s3:GetReplicationConfiguration",
              "s3:GetObjectVersion",
              "s3:GetObjectVersionTagging"
            ],
            "Resource": [
              "arn:aws:s3:::your-source-bucket-name",
              "arn:aws:s3:::your-destination-bucket-name"
            ]
          }
        ]
      }


 #### To create an IAM role for an S3 Storage Gateway:

    * Go to the IAM Console in AWS.
    * Create a role with the use case "Storage Gateway."
    * Attach a custom policy with JSON permissions that grant access to specific S3 buckets.
    * Review and create the role, naming it "FgwIamPolicy" and save the ARN of IAM role.
    
 This policy grants the required permissions for S3 Storage Gateway:
 
      {
        "Version": "2012-10-17",
        "Statement": [
          {
            "Effect": "Allow",
            "Action": [
              "s3:ListBucket",
              "s3:GetObject",
              "s3:PutObject",
              "s3:DeleteObject"
            ],
            "Resource": [
             "arn:aws:s3:::*"
            ]
          }
        ]
      }
      
Note : Make sure to replace "your-s3-bucket-name" with the actual name of your S3 bucket.


#### 2: VPC Configuration: 

   1. Log In to AWS Console:
   Log in to your AWS console using your AWS account credentials.

   2. Create a VPC:

      a. Go to the VPC Dashboard.
      b. Click on "Your VPCs" in the left navigation pane.
      c. Click the "Create VPC" button.
      d. Provide a VPC name: On-Prem-VPC and specify the IPv4 CIDR block : 10.10.0.0/16 .
      e. Region: us-east-1
      f. Leave the other settings as default, unless you have specific requirements.

   4. Create a Public Subnet:

      a. In the VPC Dashboard, select your newly created VPC.
      b. Click on "Subnets" in the left navigation pane.
      c. Click the "Create Subnet" button.
      d. Provide a subnet name : On-Prem-Subnet.
      e. Select the VPC you created earlier.
      f. Specify the IPv4 CIDR block for the public subnet 10.10.0.0/24.
      g. Ensure that you choose an Availability Zone: us-east-1c.

   5. Create an Internet Gateway (IGW):

      a. In the VPC Dashboard, select "Internet Gateways" in the left navigation pane.
      b. Click the "Create Internet Gateway" button.
      c. Give it a name and create the IGW.
      d. Select the IGW, click "Actions," and choose "Attach to VPC." Attach it to your VPC.

   6. Configure the Route Table:

      a. Go to the "Route Tables" section in the VPC Dashboard.
      b. Find the route table associated with your public subnet (usually the main one).
      c. Edit the route table and add a route with destination 0.0.0.0/0 and target as the Internet Gateway you created.








   7. Create or Use an Existing Key Pair:

      If you don't have an existing EC2 key pair, you can create one. You will need this key pair to SSH into your EC2 instance. You can manage key        pairs in the "Key Pairs" section of the EC2 Dashboard.

   5. Create Security Groups:

a. Go to the EC2 Dashboard.

b. In the left navigation pane, under "Network & Security," click on "Security Groups."

c. Click the "Create Security Group" button.

d. Create the first security group for your EC2 instance, which we'll call "WebServerSG." This security group will control inbound traffic to your instance. Configure the following rules:

Inbound Rules:
SSH (Secure Shell): Allow inbound traffic on port 22 (for SSH access) from your IP or IP range.
HTTP: Allow inbound traffic on port 80 (for web traffic) from anywhere.
HTTPS: Allow inbound traffic on port 443 (for secure web traffic) from anywhere.
e. Create the second security group, which we'll call "DatabaseSG." This security group will control outbound traffic from your EC2 instance. Configure the following rule:

Outbound Rules:
All traffic: Allow all outbound traffic to anywhere.

7. Launch an EC2 Instance:

a. Go to the EC2 Dashboard.
b. Click the "Launch Instances" button.
c. Choose an Amazon Machine Image (AMI) for your Linux instance.
d. Select an instance type.
e. Configure the instance details. In the "Subnet" section, select the public subnet you created.
f. Configure the instance details, including security groups, IAM roles, and user data if needed.
g. On the "Review" page, review your settings, and then click "Launch."






