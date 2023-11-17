# AWS CloudFormation: Create a VPC with EC2 Instance using Nested Stacks

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/7fc97788-e6b7-40be-88fb-38d85661446c" width=900 height=500>

Here's a step-by-step guide:

## Step 1: Create an S3 Bucket:

  * Log in to the AWS Management Console.
  * Navigate to the S3 service.
  * Create a new bucket: mycfcuket1116( bucket name should be unique)  to store your CloudFormation templates.
  
## Step2 :Upload Template Files to S3:

  * Upload three files ( parentstack.yaml, vpctsack.yaml and ec2instancestack.yaml) required for your nested stacks (VPC and EC2       
    templates) into the created S3 bucket. Please find the template files here.
  * Retrieve the Object URLs of each uploaded file.
  * Download Parent Stack Template:

Download the parentstack.yaml CloudFormation template to your local environment.
Edit the Parent Stack Template:

Open parentstack.yaml using a text editor.
Locate the Resources section in the template.
Add the Object URLs of the VPC and EC2 files in the appropriate sections of the Resources using AWS::CloudFormation::Stack.
Upload Edited Template to S3:

Save the edited parentstack.yaml.
Upload the updated parentstack.yaml to the same S3 bucket, replacing the old file.
Create CloudFormation Stack:

Go to the CloudFormation service in the AWS Management Console.
Click on "Create Stack" and select "With new resources (standard)".
Choose the updated parentstack.yaml in the S3 location as the template source.
Fill in the required parameters:
Provide CIDR blocks for VPC, public and private subnets.
Specify the EC2 key pair name.
Enter your IP address for SSH port access.
Click "Next" and then "Create Stack".
Monitor Stack Creation:

Wait for the CloudFormation stack to be created. Monitor the progress in the CloudFormation console.
Once successfully created, check the resources created:
VPC with public and private subnets.
Internet Gateway attached to the VPC.
Route tables configured for subnets.
EC2 instance launched in the public subnet with a security group configured.
Post-Stack Creation Actions:

Test connectivity to the EC2 instance using SSH based on the security group settings.
Ensure that the VPC, subnets, and EC2 instance are functioning as expected.
This process involves setting up a nested CloudFormation stack where the parent stack references the URLs of the VPC and EC2 templates stored in an S3 bucket, enabling the creation of VPC resources, subnets, and an EC2 instance within the defined VPC. Adjust parameters and configurations according to your specific requirements and AWS environment.
