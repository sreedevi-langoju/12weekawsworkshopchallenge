# Create an EventBridge Rule to get notified on EC2 Instance state change using Terraform

Task 1: Sign in to AWS Management Console
Click on the Open Console button, and you will get redirected to AWS Console in a new browser tab.

On the AWS sign-in page,

Leave the Account ID as default. Never edit/remove the 12 digit Account ID present in the AWS Console. otherwise, you cannot proceed with the lab.

Now copy your User Name and Password in the Lab Console to the IAM Username and Password in AWS Console and click on the Sign in button

Once Signed In to the AWS Management Console, Make the default AWS Region as US East (N. Virginia) us-east-1.
Task 2: Setup Visual Studio Code
Open the visual studio code.

If you have already installed and using Visual studio code, open a new window.

A new window will open a new file and release notes page (only if you have installed or updated Visual Studio Code recently). Close the Release notes tab.

Open Terminal by selecting View from the Menu bar and choose Terminal. 

It may take up to 2 minutes to open the terminal window.

Once the terminal is ready, let us navigate to the Desktop.

cd Desktop
Create a new folder by running the below command.

mkdir task_10102
Change your present working directory to use the newly created folder by running the below command:

cd task_10102
Get the location of the present working directory by running the below command:

pwd
Note down the location, as you will open the same in the next steps.

Now click on the first icon Explorer present on the left sidebar.

Click on the button called Open folder and navigate to the location of folder task_10102.

Visual Studio Code is now ready to use.

Task 3: Create a variable file
In this task, you will create variable files where you will declare all the global variables with a short description and a default value.

To create a variable file, expand the folder task_10102 and click on the New File icon to add the file.

Name the file as variables.tf and press Enter to save it.

Note: Don't change the location of the new file, keep it default, i.e. inside the task_10102 folder.

Paste the below contents in variables.tf file.

 variable "access_key" {
    description = "Access key to AWS console"
}

variable "secret_key" {
    description = "Secret key to AWS console"
}
variable "region" {
    description = "AWS region"
}
variable "endpoint" {
  type = string
  description = "Email endpoint for the SNS subscription"
}			
In the above content, you are declaring a variable called, access_key, secret_key, and region with a short description of all 3.

After pasting the above contents, save the file by pressing ctrl + S.

Now expand the folder task_10102 and click on the New File icon to add the file.

Name the file as terraform.tfvars and press Enter to save it.

Paste the below content into the terraform.tfvars file.

region = "us-east-1"
access_key = "<YOUR AWS CONSOLE ACCESS ID>"
secret_key = "<YOUR AWS CONSOLE SECRET KEY>"			
In the above code, you are defining the dynamic values of variables declared earlier.

Replace the values of access_key and secret_key by copying from the lab page.

After replacing the values of access_key and secret_key, save the file by pressing Ctrl + S.

        

Task 4: Create a security group in main.tf file
 In this task, you will create a main.tf file where you will add details of the provider and resources.

To create a main.tf file, expand the folder task_10102 and click on the New File icon to add the file.

Name the file as main.tf and press Enter to save it.

Paste the below content into the main.tf file.

provider "aws" {
    region     = "${var.region}"
    access_key = "${var.access_key}"
    secret_key = "${var.secret_key}"
}			
In the above code, you are defining the provider as aws.

Next, we want to tell Terraform to create a Security group for EC2 Instance

To create a security group Paste the below content into the main.tf file after the provider

############ Creating Security Group for EC2 ############
resource "aws_security_group" "web-server" {
    name        = "web-server"
    description = "Allow incoming HTTP Connections"
    ingress {
        from_port   = 22
        to_port     = 22
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }
    egress {
        from_port   = 0
        to_port     = 0
        protocol    = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
}			
       
Task 5: Create a Key pair in main.tf file
 In this task, you will create a key pair for EC2 Instance

To create a Key pair add another block of code just below the security group code into the main.tf file

############ Creating Key pair for EC2 ############
resource "tls_private_key" "example" {
  algorithm = "RSA"
  rsa_bits  = 4096
}
resource "aws_key_pair" "whiz_key" {
  key_name   = "WhizKey"
  public_key = tls_private_key.example.public_key_openssh
}			


Save the file by pressing Ctrl + S. 

Task 6: Launch an EC2 Instance in main.tf file
 In this task, you will Launch an EC2 Instance that  will be used for checking various features in CloudWatch.

To Launch an EC2 Instance add another block of code just below the key pair code into the main.tf file

################## Launching EC2 Instance ##################
resource "aws_instance" "web-server" {
    ami             = "ami-01cc34ab2709337aa"
    instance_type   = "t2.micro"
    key_name        = aws_key_pair.whiz_key.key_name
    security_groups = ["${aws_security_group.web-server.name}"]
    tags = {
        Name = "MyEC2Server"
    }
}			
   

Save the file by pressing Ctrl + S. 

Task 7: Create SNS Topic in main.tf file
 In this task, you will create an SNS Topic in main.tf file

To create an SNS Topic add another block of code just below the EC2 code into the main.tf file

############ Creating an SNS Topic ############
resource "aws_sns_topic" "topic" {
  name = "MyServerMonitor"
}			


Save the file by pressing Ctrl + S.

Task 8: Create SNS Topic Subscription in main.tf file
 In this task, you will create an SNS Topic Subscription 

To create an SNS Topic Subscription add another block of code just below the SNS Topic code into the main.tf file

############ Creating SNS Topic Subscription ############
resource "aws_sns_topic_subscription" "topic-subscription" {
  topic_arn = aws_sns_topic.topic.arn
  protocol  = "email"
  endpoint= var.endpoint
}			
    

Save the file by pressing Ctrl + S.

Task 9: Create a CloudWatch Event in main.tf file
 In this task, you will create a CloudWatch Event rule in main.tf.file. Using CloudWatch Events we will trigger SNS Notifications by stopping and starting an EC2 instance.

To create a CloudWatch Event rule add another block of code just below the subscription code into the main.tf file

############ Creating CloudWatch Event ############
resource "aws_cloudwatch_event_rule" "event" {
  name        = "MyEC2StateChangeEvent"
  description = "MyEC2StateChangeEvent"
  event_pattern = <<EOF
{
  "source": [
    "aws.ec2"
  ],
  "detail-type": [
    "EC2 Instance State-change Notification"
  ]
}
EOF
}
resource "aws_cloudwatch_event_target" "sns" {
  rule      = aws_cloudwatch_event_rule.event.name
  target_id = "SendToSNS"
  arn       = aws_sns_topic.topic.arn
}
resource "aws_sns_topic_policy" "default" {
  arn    = aws_sns_topic.topic.arn
  policy = data.aws_iam_policy_document.sns_topic_policy.json
}
data "aws_iam_policy_document" "sns_topic_policy" {
  statement {
    effect  = "Allow"
    actions = ["SNS:Publish"]
    principals {
      type        = "Service"
      identifiers = ["events.amazonaws.com"]
    }
    resources = [aws_sns_topic.topic.arn]
  }
}			
In above code we are creating a CloudWatch event rule that triggers when an Amazon Elastic Compute Cloud (Amazon EC2) instance changes state. When the event is triggered, it sends a notification to an Amazon Simple Notification Service (SNS) topic. The SNS topic is also given permission to publish messages by an Amazon Identity and Access Management (IAM) policy.

Save the file by pressing Ctrl + S.
Task 10: Create an Output file
In this task, you will create an output.tf file where you will add details of the provider and resources.

To create an output.tf file, expand the folder task_10102 and click on the New File icon to add the file.

Name the file as output.tf and press Enter to save it.

Paste the below content into the output.tf file.

output "instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.web-server.id
}
output "topic_arn" {
  description = "ARN of SNS tpoic"
  value       = aws_sns_topic.topic.arn
}
output "event_name" {
  description = "ARN of CloudWatch Rule"
  value       = aws_cloudwatch_event_rule.event.arn
}			
In the above code, we will extract details of resources created to confirm that they are created.

Task 11: Confirm the installation of Terraform by checking the version
In the Visual Studio Code, open Terminal by selecting View from the Menu bar and choose Terminal.

If you are not in the newly created folder change your present working directory by running the below command.

cd task_10102
To confirm the installation of Terraform, run the below command to check the version:

terraform version
If you are getting output as command not found: terraform, this means that terraform is not installed on your system, To install terraform follow the official guide link provided in the Prerequisite section above.

Task 12: Apply terraform configurations
Initialize Terraform by running the below command,

terraform init


Note: terraform init will check for all the plugin dependencies and download them if required, this will be used for creating a deployment plan

To generate the action plans run the below command,

terraform plan
 Enter the value as your email-id and review the whole generated plan.



To create all the resources declared in main.tf configuration file, run the below command:

terraform apply
 Enter the value as your email-id and you will be able to see the resources which will be created, approve the creation of all the resources by entering yes.

 It may take up to 2 minutes for the terraform apply command to create the resources.

Id’s of all the resources created by terraform will be visible there.



Task 13: Confirm the subscription on your email id
You will receive an email in your mailbox from SNS.

     

Click on Confirm subscription.



Your email address is now subscribed to SNS Topic MyServerMonitor.

You can unsubscribe to the SNS Topic at any time.

Task 14: Check the resources in AWS Console
Make sure you are in the US East (N. Virginia) us-east-1 Region.

Navigate to EC2 by clicking on Services on the top, then click on EC2 in the Compute section.

Click on the Instances on the left navigation panel. You can see the instance created successfully.

         

To Check SNS Topic Creation Select Simple Notification Service under Application Integration section.

Click on the Topics on the left navigation panel and select the topic created. You can see that the topic is created successfully.



Select the topic created and Scroll down you can see the subscription being created and confirmed successfully.



To Check CloudWatch Event rule Creation click on Cloudwatch under Management & Governance

Navigate to Events in the left panel of the CloudWatch page. Click on Rules under Events.

You can see that the rule is created successfully.



Task 15: Test Cloudwatch Event 
Navigate to the EC2 Page in the AWS Management Console.

Click on Instances in the Left Panel.

Select the MyEC2Server. Click on Instance state and Click on Stop instance.



Click on Stop in the pop up box.

Go back to your email address. You should have received some mail.

Two CloudWatch Event emails have been sent due to the MyEC2Server State changes. (stopping and stopped).

         

Navigate back to the EC2 Page and Start the EC2 instance. You will receive another two emails for the state changes. (pending and running).

            

Note: If you can't find the emails, check in the SPAM folder of your email.

You have successfully triggered CloudWatch Event SNS notification emails.

You can also create Cloudwatch Event Notification for other AWS resources as well.
