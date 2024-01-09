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

#### Create a custom AMI
In the AWS EC2 console, you can create an Custom AMI to meet your needs. This can then be used for future EC2 instance creation. In this page, let's create an AMI using the web server instance that we built earlier.

* In the EC2 console, select the instance that we made earlier in this lab, and click Actions > Image and templates > Create Image. ![Create Image](/static/images/advanced-module/compute/v2/gid-ec2-17.png

* In the Create Image console, type as shown below and press Create image to create the custom image.

*         KEY	                VALUE
        Image name	        Web Server v1
    Image description	    LAMP web server AMI

* Verify in the console that the image creation request in completed.

* In the left navigation panel, Click the AMIs button located under IMAGES.
* You can see that the Status of the AMI that you just created. It will show either Pending or Available.

#### Terminate the instance :

  Note:  Custom AMI (Golden Image) creation has been completed for the auto scaling by using the EC2 instance you just created. Therefore, the EC2 instance currently running is no longer needed, so let's try to terminate it.( In Deploy auto scaling web service, we will use custom AMI to create a new web server.)

* In the left navigation panel of the EC2 dashboard, select Instances. Then select the instance that should be deleted. From there, click Instance state -> Terminate instance.
* When the alert message appears, click Terminate to delete.
* The instance status changes to Shutting down. After that, the instance status turned to terminated. The instance deletion is complete. You may see the instance for a short period of time for deletion logging.

Architecture Configured So Far:

If you mark the resources that have been configured so far in conceptual terms, it is same with the picture below.
<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge/assets/135724041/bf7a6391-4ce0-485f-b55e-3e2007c21562">


### Step 3 : Deploy auto scaling web service:

#### Step 3(a): Configure Application Load Balancer:

AWS Elastic Load Balancer supports three types of load balancers: Application Load Balancer, Network Load Balancer, and Classic Load Balancer. In this lab, you will configure and set up the Application Load Balancer to handle load balancing HTTP requests.

* From the EC2 Management Console in the left navigation panel, click Load Balancers under Load Balancing. Then click Create Load Balancer. In the Select load balancer type, click the Create button under Application Load Balancer.
* Name the load balancer. In this case, name Name as Web-ALB. Leave the other settings at their default values.
* Scrolling down a little bit, there is a section for selecting availability zones. First, Select the VPC-Lab-vpc created previously. For Availability Zones select the 2 public subnets that were created previously. This should be Public Subnet for ap-northeast-2a and Public Subnet C for ap-northeast-2c.
* In the Security groups section, click the Create new security group hyperlink. Enter web-ALB-SG as the security group name and check the VPC information. Click the Add rule button and select HTTP as the Type and Anywhere-IPv4 as the Source. And create a security group.
* Return to the load balancer page again, click the refresh button, and select the web-ALB-SG you just created. Remove the default security group.
* In Listeners and routing column, click Create target group. Put Web-TG for Target group name and check all settings same with the screen below. After that click Next button.
* This is where we would register our instances. However, as we mentioned earlier, there are not instances to register at this moment. Click Create target group.
* Again, move into the Load balancers page, click refresh button and select Web-TG. And then Click Create load balancer.

#### Step 3(b): Configure launch template:

Now that ALB has been created, it's time to place the instances behind the load balancer. To configure an Amazon EC2 instance to start with Auto Scaling Group, you can use Launch Template, Launch Configuration, or EC2 Instance. In this workshop, we will use the Launch Template to create an Auto Scaling group.
The launch template configures all parameters within a resource at once, reducing the number of steps required to create an instance. Launch templates make it easier to implement best practices with support for Auto Scaling and spot fleets, as well as spot and on-demand instances. This helps you manage costs more conveniently, improve security, and minimize the risk of deployment errors.

The launch template contains information that Amazon EC2 needs to start an instance, such as AMI and instance type. The Auto Scaling group refers to this and adds new instances when a scaling out event occurs. If you need to change the configuration of the EC2 instance to start in the Auto Scaling group, you can create a new version of the launch template and assign it to the Auto Scaling group. You can also select a specific version of the launch template that you use to start an EC2 instance in the Auto Scaling group, if necessary. You can change this setting at any time.

#### Step 3(c): Create security group:
Before creating a launch template, let's create a security group for the instances created through the launch template to use.

* From the left navigation panel of the EC2 console, select Security Groups under the Network & Security heading and click Create Security Group in the upper right corner.
* Scroll down to modify the Inbound rules. First, select the Add rule button to add the Inbound rules, and select HTTP in the Type. For Source, type ALB in the search bar to search for the security group created earlier Web-ALB-SG. This will configure the security group to only receive HTTP traffic coming from ALB.
* Leave outbound rules' default settings and click Create Security Group to create a new security group. This creates a security group that allows traffic only for HTTP connections (TCP 80) that enter the instance via ALB from the Internet.

#### Step 3(d): Create launch template

* In the EC2 console, select Launch Templates from the left navigation panel. Then click Create Launch Template.

* Let's proceed with setting up the launch template step by step. First, set Launch template name and Template version description as shown below, and select Checkbox for Provide guidance in Auto Scaling guidance. Select this checkbox to enable the template you create to be utilized by Amazon EC2 Auto Scaling.

*         KEY	                                        VALUE
        Launch template name                    	            Web
        Template version description	        Immersion Day Web Instances Template – Web only
        Auto Scaling guidance	                Provide guidance to help me set up a template that I can use with EC2 Auto Scaling Click this check box

* Scroll down to set the launch template contents. In Amazon Machine Image(AMI), set the AMI to Web Server v1, which was created in the previous EC2 lab. You can find it by typing Web Server v1 in the search section, or you can scroll down to find it in the My AMI section. Next, select t2.micro for the instance type. We are not going to configure SSH access because this is only for Web service server. Therefore, we do not use key pairs.
* Leave the other parts as default. Let's take a look at the Network Settings section. First, in Networking platform select Virtual Private Cloud(VPC). In security group section, find and apply ASG-Web-Inst-SG created before.
* Follow the Storage's default values without any additional change. Go down and define the Instance tags. Click Add tag and Name for Key and Web Instance for Value. Select Resource types as Instances and Volumes.
  
*             KEY               VALUE
           Key                  Name
          Value	              Web Instance
        Resource Types	    Instances and Volumes

* Finally, in the Advanced details tab, set the IAM instance profile to SSMInstanceProfile. Leave all other settings as default, and click the Create launch template button at the bottom right to create a launch template.
* After checking the values set in Summary on the right, click Create launch template to create a template.

