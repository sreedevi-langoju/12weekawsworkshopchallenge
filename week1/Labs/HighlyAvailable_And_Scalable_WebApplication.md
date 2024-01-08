# HighlyAvailable_And_Scalable_WebApplication:

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

