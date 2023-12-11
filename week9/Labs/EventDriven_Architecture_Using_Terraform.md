# Create an EventBridge Rule to get notified on EC2 Instance state change using Terraform -whizlabs journey


<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/86cd56c4-e056-416d-afa6-e58955b1a920">


## Prerequisites

Install Terraform in your local machine using this official guide by Hashicorp.

To install Terraform using CLI, use this guide https://learn.hashicorp.com/tutorials/terraform/install-cli

To install Terraform by downloading, use this guide https://www.terraform.io/downloads.html 

Download and Install Visual Studio Code editor using this guide https://code.visualstudio.com/download



## Task 1: Setup Visual Studio Code

Open the visual studio code.

If you have already installed and using Visual studio code, open a new window.

A new window will open a new file and release notes page (only if you have installed or updated Visual Studio Code recently). Close the Release notes tab.

Open Terminal by selecting View from the Menu bar and choose Terminal. 

It may take up to 2 minutes to open the terminal window.

Once the terminal is ready, let us navigate to the Desktop.
                
``` cd Desktop ```

Create a new folder by running the below command.

``` mkdir task_10102 ```

Change your present working directory to use the newly created folder by running the below command:

``` cd task_10102 ```

Get the location of the present working directory by running the below command:

 ``` pwd ```

Note down the location, as you will open the same in the next steps.

Now click on the first icon Explorer present on the left sidebar.

Click on the button called Open folder and navigate to the location of folder task_10102.

Visual Studio Code is now ready to use.

## Task 2: Create a variable file

In this task, you will create variable files where you will declare all the global variables with a short description and a default value.

To create a variable file, expand the folder task_10102 and click on the New File icon to add the file.

Name the file as variables.tf and press Enter to save it.

Note: Don't change the location of the new file, keep it default, i.e. inside the task_10102 folder.

Paste the below contents in variables.tf file. You can find the same file week9/Labs repository.

```
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
```

In the above content, you are declaring a variable called, access_key, secret_key, and region with a short description of all 3.
<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/e4e2d37d-6734-430e-ad4e-12fe4c5e90ad">

After pasting the above contents, save the file by pressing ctrl + S.

Now expand the folder task_10102 and click on the New File icon to add the file.

Name the file as terraform.tfvars and press Enter to save it.

Paste the below content into the terraform.tfvars file.You can find the same file week9/Labs repository.

```
region = "us-east-1"
access_key = "<YOUR AWS CONSOLE ACCESS ID>"
secret_key = "<YOUR AWS CONSOLE SECRET KEY>"

```
In the above code, you are defining the dynamic values of variables declared earlier.

Replace the values of access_key and secret_key with your credentials.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/0baa5bf1-cbac-48a3-9054-c272139488e2">

After replacing the values of access_key and secret_key, save the file by pressing Ctrl + S.
    

## Task 3: Create a security group in main.tf file

 In this task, you will create a main.tf file where you will add details of the provider and resources.

To create a main.tf file, expand the folder task_10102 and click on the New File icon to add the file.

Name the file as main.tf and press Enter to save it.

Paste the below content into the main.tf file.You can find the same file week9/Labs repository.

```
provider "aws" {
    region     = "${var.region}"
    access_key = "${var.access_key}"
    secret_key = "${var.secret_key}"
}
```		
In the above code, you are defining the provider as aws.

Next, we want to tell Terraform to create a Security group for EC2 Instance

To create a security group Paste the below content into the main.tf file after the provider
```
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
```
    
## Task 4: Create a Key pair in main.tf file
 In this task, you will create a key pair for EC2 Instance

To create a Key pair add another block of code just below the security group code into the main.tf file

```
############ Creating Key pair for EC2 ############
resource "tls_private_key" "example" {
  algorithm = "RSA"
  rsa_bits  = 4096
}
resource "aws_key_pair" "whiz_key" {
  key_name   = "WhizKey"
  public_key = tls_private_key.example.public_key_openssh
}			

```
Save the file by pressing Ctrl + S. 

## Task 5: Launch an EC2 Instance in main.tf file
 In this task, you will Launch an EC2 Instance that  will be used for checking various features in CloudWatch.

To Launch an EC2 Instance add another block of code just below the key pair code into the main.tf file

```
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
```   

Save the file by pressing Ctrl + S. 

## Task 6: Create SNS Topic in main.tf file

 In this task, you will create an SNS Topic in main.tf file

To create an SNS Topic add another block of code just below the EC2 code into the main.tf file
```
############ Creating an SNS Topic ############
resource "aws_sns_topic" "topic" {
  name = "MyServerMonitor"
}			
```

Save the file by pressing Ctrl + S.

## Task 7: Create SNS Topic Subscription in main.tf file

 In this task, you will create an SNS Topic Subscription 

To create an SNS Topic Subscription add another block of code just below the SNS Topic code into the main.tf file

```
############ Creating SNS Topic Subscription ############
resource "aws_sns_topic_subscription" "topic-subscription" {
  topic_arn = aws_sns_topic.topic.arn
  protocol  = "email"
  endpoint= var.endpoint
}			
```  

Save the file by pressing Ctrl + S.

## Task 8: Create a CloudWatch Event in main.tf file

 In this task, you will create a CloudWatch Event rule in main.tf.file. Using CloudWatch Events we will trigger SNS Notifications by stopping and starting an EC2 instance.

To create a CloudWatch Event rule add another block of code just below the subscription code into the main.tf file

```
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

```
<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/a1c7c763-604d-4532-9c0a-9e08605eb211">
 
In above code we are creating a CloudWatch event rule that triggers when an Amazon Elastic Compute Cloud (Amazon EC2) instance changes state. When the event is triggered, it sends a notification to an Amazon Simple Notification Service (SNS) topic. The SNS topic is also given permission to publish messages by an Amazon Identity and Access Management (IAM) policy.

Save the file by pressing Ctrl + S.

## Task 9: Create an Output file

In this task, you will create an output.tf file where you will add details of the provider and resources.

To create an output.tf file, expand the folder task_10102 and click on the New File icon to add the file.

Name the file as output.tf and press Enter to save it.

Paste the below content into the output.tf file.You can find the same file week9/Labs repository.

```
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
```
		
In the above code, we will extract details of resources created to confirm that they are created.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/46408365-8adf-43b4-91a8-02aaefaf991a">

## Task 10: Confirm the installation of Terraform by checking the version

In the Visual Studio Code, open Terminal by selecting View from the Menu bar and choose Terminal.

If you are not in the newly created folder change your present working directory by running the below command.

``` cd task_10102 ```

To confirm the installation of Terraform, run the below command to check the version:

``` terraform version ```

If you are getting output as command not found: terraform, this means that terraform is not installed on your system, To install terraform follow the official guide link provided in the Prerequisite section above.

## Task 11: Apply terraform configurations

Initialize Terraform by running the below command,

``` terraform init ```

Note: terraform init will check for all the plugin dependencies and download them if required, this will be used for creating a deployment plan

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/c9cab2e9-15ee-41b6-92a7-4ecab7a2271f">

To generate the action plans run the below command,

``` terraform plan ```

Enter the value as your email-id and review the whole generated plan.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/4afebe10-a7ab-4cdd-bbcf-b95f7799ef86">

To create all the resources declared in main.tf configuration file, run the below command:

``` terraform apply ```

Enter the value as your email-id and you will be able to see the resources which will be created, approve the creation of all the resources by entering yes.

 It may take up to 2 minutes for the terraform apply command to create the resources.

Id’s of all the resources created by terraform will be visible there.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/c0aef952-f277-4152-bf39-3626ea499b75">

## Task 12: Confirm the subscription on your email id

You will receive an email in your mailbox from SNS.  

Click on Confirm subscription.

<img src="![image](https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/0f2c1e4c-e94e-48fe-aebb-ef877d8ec8a7)
">

Your email address is now subscribed to SNS Topic MyServerMonitor.

You can unsubscribe to the SNS Topic at any time.

## Task 13: Open AWS management Console

Make sure you are in the US East (N. Virginia) us-east-1 Region.

Navigate to EC2 by clicking on Services on the top, then click on EC2 in the Compute section.

Click on the Instances on the left navigation panel. You can see the instance created successfully.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/d410ff0b-a3d7-4e19-a171-25c16215afa8">
     

To Check SNS Topic Creation Select Simple Notification Service under Application Integration section.

Click on the Topics on the left navigation panel and select the topic created. You can see that the topic is created successfully.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/d7e6d55b-0c59-47b1-af56-41e61f433bfc">

Select the topic created and Scroll down you can see the subscription being created and confirmed successfully.

To Check CloudWatch Event rule Creation click on Cloudwatch under Management & Governance

Navigate to Events in the left panel of the CloudWatch page. Click on Rules under Events.

You can see that the rule is created successfully.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/147a2ef0-c3ae-4e8a-8ee7-76d4409eec4c">

## Task 14: Test Cloudwatch Event 

Navigate to the EC2 Page in the AWS Management Console.

Click on Instances in the Left Panel.

Select the MyEC2Server. Click on Instance state and Click on Stop instance.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/59d347a0-aa5e-4aae-ad10-0fe69012ac14">

Click on Stop in the pop up box.

Go back to your email address. You should have received some mail.

Two CloudWatch Event emails have been sent due to the MyEC2Server State changes. (stopping and stopped).

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/07f6ac58-e259-4b24-a461-80fbd5ecacad">      

Navigate back to the EC2 Page and Start the EC2 instance. You will receive another two emails for the state changes. (pending and running).

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/7f8a2890-9686-454b-8233-afcfb1ca847a">

Note: If you can't find the emails, check in the SPAM folder of your email.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/483ed6ff-c113-40da-ab59-64d08003f6e4">

You have successfully triggered CloudWatch Event SNS notification emails.

You can also create Cloudwatch Event Notification for other AWS resources as well.
