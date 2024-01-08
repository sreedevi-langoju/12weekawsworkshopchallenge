# Building HighlyAvailable And Scalable WebApplication:

If you don't have a root AWS account yet, click  to learn how to create a new AWS account.

Create an IAM user
If you already have an AWS account or create an AWS account, create an IAM user that has access to AWS account. Log in to the AWS account, you can create a IAM user using IAM console. Create an IAM user with Administrator role. If you already have an IAM user with administrator role, continue.

I will walk you throught the steps for AWS General Immersion Day - Advanced hands-on lab introducing AWS core services(VPC, EC2, RDS, S3) enable you to build your own web application same as the architecture below.
<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge/assets/135724041/8c3b1e87-30ea-4940-8f65-6ff9b2d30008" width=600 height=600>

### Hands on Lab Configuration: 

Specifically, we will walk you through the following topics.

1. Network – Amazon VPC
2. Compute – Amazon EC2
3. Database – Amazon Aurora
4. Storage – Amazon S3
5. Clean up resource


### Step1: Network – Amazon VPC:

Fianl Architecture:

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge/assets/135724041/6507f685-b4ff-44af-a867-a4610864e9fb">

* After logging in to the AWS console, select VPC from the service menu.
* Select VPC Dashboard and click Launch VPC Wizard to create your own VPC.
* To create a space to provision AWS resources used in this lab, we will create a VPC and Subnets. Select VPC, subnets, etc in Resource to create tab and change name tag to VPC-Lab. Leave the default setting for IPv4 CIDR block.
* To design high availability architecture, we create 2 subnet space and select 2a and 2c for Customize AZs. And set the CIDR value of the public subnet that can communicate directly with the Internet as shown in the screen below. Set the CIDR value of the private subnet as:
* 
    KEY	                            VALUE
2a Public subnet’s IPv4 CIDR	  10.0.10.0/24
2c Public subnet’s IPv4 CIDR	  10.0.20.0/24
2a Private subnet’s IPv4 CIDR	  10.0.100.0/24
2c Private subnet’s IPv4 CIDR     10.0.200.0/24

* You can use a NAT gateway so that instances in your private subnets can connect to services outside your VPC, but external services cannot initiate direct connections to these instances. In this lab, we will create a NAT gateway in only one Availability Zone to save cost. Also, for DNS options, enable both DNS hostnames and DNS resolution. After confirming the setting value, click the Create VPC button.
* As the VPC is created, you can see the process of creating network-related resources as shown in the screen below. For NAT Gateway, provisioning may take longer compared to other resources.
* You can check the information of the created VPC. Check related information such as CIDR value, route table, network ACL, etc. Check that the values you just set are correct.


### (option) Create VPC Endpoint :

* In VPC Dashboard, select Endpoints. Click Create endpoint button.
* Type s3 endpoint for name and select AWS services in Service category tab. In the search bar below, type s3 and select the list at the top.
* For S3 VPC endpoints, there are gateway types and interface types. For this lab, select the gateway type. And for the deployment location, select the VPC-Lab-vpc created in this lab.
* Choose a route table to reflect the endpoint. Select the two private subnets as shown below. Additional routing information for using the endpoint is automatically added to the selected route table.
* You can also configure policies to control access to endpoints as shown below.
* Confirm that the route to access Amazon S3 through the gateway endpoint has been automatically added to the private route table specified earlier.

* NOTE : VPC endpoints are communications within the AWS network and have the security and compliance advantage of being able to control traffic through the endpoints. You can also optimize the data processing cost if you transfer your data through a VPC endpoint rather than a NAT gateway.


### Step 2: Compute – Amazon EC2

Amazon Elastic Compute Cloud (Amazon EC2) is a web service that provides secure, resizable compute capacity in the cloud. It is designed to make web-scale cloud computing easier for developers. Amazon EC2’s simple web service interface allows you to obtain and configure capacity with minimal friction. It provides you with complete control of your computing resources and lets you run on Amazon’s proven computing environment.

This compute lab uses Auto Scaling Group to deploy web service instances to private subnets in your VPC that you created earlier in this network lab. This configures the highly available web services so that external users can access the Sample Web Page through the web

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge/assets/135724041/043003dc-bbae-4e09-b647-20e755aa4068">

* The following items are contained in this chapter.

    1. Launch web server instances and execute user data
    2. Set up a security group
    3. Create a custom Amazon Machine Image (AMI)
    4. Launch an Application Load Balancer (ALB)
    5. Configure a Launch Template
    6. Configure an Auto Scaling Group
    7. Test auto scaling and change manual settings


* The order of this lab is as follows:

    1. Launch a web server instance
    2. Deploy auto scaling web service
    3. Check web service and test

#### Step 2(a) : Launch a web server instance:

* In the AWS console search bar, type EC2  and select it. Then click EC2 Dashboard at the top of the left menu. Press the Launch instance button and select Launch instance from the menu.
* In Name, put the value Web server for custom AMI. And check the default setting in Amazon Machine Image below.
* Select t2.micro in Instance Type.
* For Key pair, choose Proceed without a key pair.
* Click the Edit button in Network settings to set the space where EC2 will be located.
* And choose the VPC-Lab-vpc created in the previous lab, and for the subnet, choose public subnet. Auto-assign public IP is set to Enable.
* Right below it, create Security groups to act as a network firewall. Security groups will specify the protocols and addresses you want to allow in your firewall policy. For the security group you are currently creating, this is the rule that applies to the EC2 that will be created. After entering Immersion Day - Web Server in Security group name and Description, select Add Security group rule and set HTTP to Type. Also allow TCP/80 for Web Service by specifying it. Select My IP in the source.
* All other values accept the default values, expand by clicking on the Advanced Details tab at the bottom of the screen.
* Enter the following values in the User data field and select Launch instance.

```
#!/bin/sh
​
#Install a LAMP stack
dnf install -y httpd wget php-fpm php-mysqli php-json php php-devel
dnf install -y mariadb105-server
dnf install -y httpd php-mbstring
​
#Start the web server
chkconfig httpd on
systemctl start httpd
​
#Install the web pages for our lab
if [ ! -f /var/www/html/immersion-day-app-php7.zip ]; then
   cd /var/www/html
   wget -O 'immersion-day-app-php7.zip' 'https://static.us-east-1.prod.workshops.aws/public/dd38a0a0-ae47-43f1-9065-f0bbcb15f684/assets/immersion-day-app-php7.zip'
   unzip immersion-day-app-php7.zip
fi
​
#Install the AWS SDK for PHP
if [ ! -f /var/www/html/aws.zip ]; then
   cd /var/www/html
   mkdir vendor
   cd vendor
   wget https://docs.aws.amazon.com/aws-sdk-php/v3/download/aws.zip
   unzip aws.zip
fi
​
# Update existing packages
dnf update -y

```

* Information indicating that the instance creation is in progress is displayed on the screen. You can view the list of EC2 instances by selecting View Instances in the lower right corner.

* After the instance configuration is complete, you can check the Availability Zone in which the instance is running, and externally accessible IP and DNS information.
* Wait for the instance's Instance state result to be Running. Open a new web browser tab and enter the Public DNS or IPv4 Public IP of your EC2 instance in the URL address field. If the page is displayed as shown below, the web server instance is configured normally.

#### Access the web service:

Go to the EC2 instance console. Select the instance you want to connect to and click the Connect button in the center.

* In the Connect your instance window, select the EC2 Instance Connect tab, then click the Connect button in the lower right corner.
* After a while, you can use the browser-based SSH console as shown below. Just close the window after the CLI test.

#### Connect to the Linux instance using Session Manager:

You must click the Access your Linux instance using Session Manager link below to proceed with the exercise.

In the database lab to be followed, connect to RDS using the IAM role granted to the web server. Therefore, refer to Accessing Linux instance using Session Manager: https://catalog.workshops.aws/general-immersionday/ko-KR/basic-modules/10-ec2/ec2-linux/3-ec2-1  to assign IAM role to EC2 instance. grant.

