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


### Step 2 : Deploy auto scaling web service:

#### Step 2(a): Configure Application Load Balancer:

AWS Elastic Load Balancer supports three types of load balancers: Application Load Balancer, Network Load Balancer, and Classic Load Balancer. In this lab, you will configure and set up the Application Load Balancer to handle load balancing HTTP requests.

* From the EC2 Management Console in the left navigation panel, click Load Balancers under Load Balancing. Then click Create Load Balancer. In the Select load balancer type, click the Create button under Application Load Balancer.
* Name the load balancer. In this case, name Name as Web-ALB. Leave the other settings at their default values.
* Scrolling down a little bit, there is a section for selecting availability zones. First, Select the VPC-Lab-vpc created previously. For Availability Zones select the 2 public subnets that were created previously. This should be Public Subnet for ap-northeast-2a and Public Subnet C for ap-northeast-2c.
* In the Security groups section, click the Create new security group hyperlink. Enter web-ALB-SG as the security group name and check the VPC information. Click the Add rule button and select HTTP as the Type and Anywhere-IPv4 as the Source. And create a security group.
* Return to the load balancer page again, click the refresh button, and select the web-ALB-SG you just created. Remove the default security group.
* In Listeners and routing column, click Create target group. Put Web-TG for Target group name and check all settings same with the screen below. After that click Next button.
* This is where we would register our instances. However, as we mentioned earlier, there are not instances to register at this moment. Click Create target group.
* Again, move into the Load balancers page, click refresh button and select Web-TG. And then Click Create load balancer.

#### Step 2(b): Configure launch template:

Now that ALB has been created, it's time to place the instances behind the load balancer. To configure an Amazon EC2 instance to start with Auto Scaling Group, you can use Launch Template, Launch Configuration, or EC2 Instance. In this workshop, we will use the Launch Template to create an Auto Scaling group.
The launch template configures all parameters within a resource at once, reducing the number of steps required to create an instance. Launch templates make it easier to implement best practices with support for Auto Scaling and spot fleets, as well as spot and on-demand instances. This helps you manage costs more conveniently, improve security, and minimize the risk of deployment errors.

The launch template contains information that Amazon EC2 needs to start an instance, such as AMI and instance type. The Auto Scaling group refers to this and adds new instances when a scaling out event occurs. If you need to change the configuration of the EC2 instance to start in the Auto Scaling group, you can create a new version of the launch template and assign it to the Auto Scaling group. You can also select a specific version of the launch template that you use to start an EC2 instance in the Auto Scaling group, if necessary. You can change this setting at any time.

#### Step 2(c): Create security group:
Before creating a launch template, let's create a security group for the instances created through the launch template to use.

* From the left navigation panel of the EC2 console, select Security Groups under the Network & Security heading and click Create Security Group in the upper right corner.
* Scroll down to modify the Inbound rules. First, select the Add rule button to add the Inbound rules, and select HTTP in the Type. For Source, type ALB in the search bar to search for the security group created earlier Web-ALB-SG. This will configure the security group to only receive HTTP traffic coming from ALB.
* Leave outbound rules' default settings and click Create Security Group to create a new security group. This creates a security group that allows traffic only for HTTP connections (TCP 80) that enter the instance via ALB from the Internet.

#### Step 2(d): Create launch template

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

#### Step 2(e): Set Auto Scaling Group:
  
Now, let's create the Auto Scaling Group.

* Enter the EC2 console and select Auto Scaling Groups at the bottom of the left navigation panel. Then click the Create Auto Scaling group button to create an Auto Scaling Group.
* In [Step : Choose launch template or configuration], specify the name of the Auto Scaling group. In this workshop, we will designate it as Web-ASG. Then select the launch template that you just created named Web. The default settings for the launch template will be displayed. Confirm and click the lower right Next button.

*             KEY	                    VALUE
        Auto Scaling Group name	        Web-ASG
          Launch Template                 Web

* Set the network configuration with the Purging options and instance types as default. Choose VPC-Lab-vpc for VPC, select Private subnet 1 and Private subnet 2 for Subnets. When the setup is completed, click the Next button.
* Next, proceed to set up load balancing. First, select Attach to an existing load balancer. Then in Choose a target group for your load balancer, select Web-TG created during in ALB creation. At the Monitoring, select Check box for Enable group metrics collection within CloudWatch. This allows CloudWatch to see the group metrics that can determine the status of Auto Scaling groups. Click the Next button at the bottom right.
* In the step of Configure group size and scaling policies, set scaling policy for Auto Scaling Group. In the Group size column, specify Desired capacity and Minimum capacity as 2 and Maximum capacity as 4. Keep the number of the instances to 2 as usual, and allow scaling of at least 2 and up to 4 depending on the policy.
* In the Scaling policies section, select Target tracking scaling policy and type 30 in Target value. This is a scaling policy for adjusting the number of instances based on the CPU average utilization remaining at 30% overall. Leave all other settings as default and click the Next button in the lower right corner.
* We will not Add notifications. Clcik the Next button to move to the next step. In the Add tags step, we will simply assign name tag. Click Add tag, type Name in Key, ASG-Web-Instance in Value, and then click Next.

* 
            KEY	        VALUE
            Key	        Name
            Value	ASG-Web-Instance

* Now we are in the final stage of review. After checking the all settings, click the Create Auto Scaling Group button at the bottom right.

* Auto Scaling group has been created. You can see the Auto Scaling group created in the Auto Scaling group console as shown below.
* Instances created through the Auto Scaling group can also be viewed from the EC2 Instance menu.

  #### Architecture Configured So Far
  
Now, we've built a web service that is high available and automatically scales under load! The configuration of the services we have created so far is as follows.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge/assets/135724041/e57c57d5-d39b-4d9e-884c-ec2e346367df">


### Step : Check web service and test:

Now, let's test the service you have configured for successful operation. First, let's check whether you can access the website normally and whether the load balancer works, and then load the web server to see if Auto Scaling works.

#### Step4(a): Check web service and load balancer:

* To access through the Application Load Balancer configured for the web service, click the Load Balancers menu in the EC2 console and select the Web-ALB you created earlier. Copy DNS name from the basic configuration.
* Open a new tab in your web browser and paste the copied DNS name. You can see that web service is working as shown below. For the figure below, you can see that the web instance placed in ap-northeast-2a is running this web page.
* If you click the refresh button here, you can see that the host serving the web page has been replaced with an instance of another availability zone area (ap-northeast-2c) as shown below. This is because routing algorithms in ALB target groups behave Round Robin by default.
* Currently, in the the Auto Scaling group, scaling policy's baseline has been set to 30% CPU utilization for each instance.

If the average CPU utilization of an instance is less than 30%, Reduce the number of instances.
If the average CPU utilization of an instance is over 30%, Additional instances will be deployed, load will be distributed, and adjusted to ensure that the average CPU utilization of the instances is 30%.
* Now, let's test load to see whether Auto Scaling works well. On the web page above, click the LOAD TEST menu. The web page changes and the applied load is visible. Click on the logo at the top left of the page to see that each instance is under load.

* Before load:

* After load:


* Enter Auto Scaling Groups from the left side menu of the EC2 console and click the Monitoring tab. Under Enabled metrics, click EC2 and set the right time frame to 1 hour. If you wait for a few seconds, you'll see the CPU Utilization (Percent) graph changes.
* Wait for about 5 minutes (300 seconds) and click the Activity tab to see the additional EC2 instances deployed according to the scaling policy.
* When you click on the Instance management tab, you can see that two additional instances have sprung up and a total of four are up and running.
* If you use the ALB DNS that you copied earlier to access and refresh the web page, you can see that it is hosting the web page in two instances that were not there before. The current CPU load is 0% because it is a new instance. It can also be seen that each of them was created in a different availability zone. If it's not 0%, it can look more than 100% because it's a constant load situation.

  Note: So far, we've checked that Auto Scaling group is working through a load test on the web service. If the page that causes the CPU load is working, close the page to prevent additional load.

  ### Step3: Database – Amazon Aurora:

 ##### Final Architecture:
 
In this database lab, we will deploy RDS Aurora instance in VPC-Lab and configure the web service(Apache + PHP) in Auto Scaling Group to use RDS Aurora(MySQL). When the connection to the database is completed, create a new version of the existing custom AMI and update the Auto Scaling Group to use the new version of AMI. In addtion, we conduct a test to add/modify/delete contacts in a simple address book stored in RDS' DB through the web browser.

##### Hands-on Lab Sequence:

The order of this lab is as follows.

    1. Create VPC security group
    2. Create RDS instance
    3. Connect RDS with Web App server
    4. Access RDS from EC2
    5. (option) RDS Management Features


#### Step 3(a): Create VPC security group:

The RDS service uses the same security model as EC2. The most common usage format is to provide data as a database server to an EC2 instance operating as an applicatiojn server within the same VPC, or to configure it to be accessible to the DB Application client outside of the VPC. The VPC Security Group must be applied for proper access control.

In the previous Compute - Amazon EC2 lab, we created web server EC2 instances using Launch Template and Auto Scaling Group. These instances use Launch Template to apply the security group ASG-Web-Inst-SG . Using this information, we will create a security group so that only web server instances within the Auto Scaling Group can access RDS instances.

* On the left side of the VPC dashboard, select Security Groups and then select Create Security Group.

* Enter Security group name and Description as shown below. Choose the VPC that was created in the first lab. It should be named VPC-Lab.
* Scroll down to the Inbound rules column. Click Add rule to create a security group policy that allows access to RDS from the EC2 Web servers that you previously created through the Auto Scaling Group. Under Type, select MySQL/Aurora The port range should default to 3306. The protocol and port ranges are automatically specified. The Source type entry can specify the IP band (CIDR) that you want to allow acces to, or other security groups that the EC2 instances to access are already using. Select the security group(named ASG-Web-Inst-SG ) that is applied to the web instances of the Auto Scaling group in the Compute - Amazon EC2.
* When settings are completed, click Create Security Group at the bottom of the list to create this security group.


#### Step 5: Create RDS instance:

Since the security group that RDS will use has been created, let's create an instance of RDS Aurora (MySQL compatible).

* In the AWS Management console, go to the RDS (Relational Database Service) .

* Select Create Database in dashboard to start creating a RDS instance.

* You want to select the RDS instances' database engine. In Amazon RDS, you can select the database engine based on open source or commercial database engine. In this lab, we will use Amazon Aurora with MySQL-compliant database engine. Select Standard Create in the choose a database creation method section. Set Engine type to Amazon Aurora, Set Edition to Amazon Aurora with MySQL compatibility, Set Capacity type to Provisioned and Version to Aurora (MySQL 5.7) 2.10.2.
In the AWS Management console, go to the RDS (Relational Database Service).

* Select Production in Template. Under Settings, we want to specify administrator information for identifying the RDS instances. Enter the information as it appears below.

* 
  KEY                        	VALUE
DB cluster identifier       rdscluster
Master username	            awsuser
Master password	            awspassword

* Under DB instance size select Memory Optimized class. Under Availability & durability select Create an Aurora Replica or reader node in a different AZ. Select db.r5.large for instance type.
* Set up network and security on the Connectivity page. Select the VPC-Lab that you created earlier in the Virtual private cloud (VPC) and specify the subnet that the RDS instance will be placed in, public access, and security groups. Enter the information as it appears below.

* 
                KEY            	        VALUE
    Virtual private cloud (VPC)	        VPC-Lab-vpc
    Subnet group                    	Create new DB subnet group
    Publicly accessible                 No
    VPC security group	                Choose existing: DB SG (In case of Default, click X button for remove it)
    Database port (Database Port)	    3306

* Scroll down and click Additional configuration. Set database options as shown below. Be aware of the uppercase and lowercase letters of Initial database name.
*                 KEY	                VALUE
    Initial database name	        immersionday
    DB cluster parameter group	    default.aurora-mysql5.7
    DB parameter group	            default.aurora-mysql5.7

* Subsequent items such as Backup, Entry, Backtrack, Monitoring, and Log exports all accept the default values, and press Create database to create a database.

* A new RDS instance is now creating. This may take more than 5 minutes. You can use an RDS instance when the DB instance's status changed to Available.
  

  <img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge/assets/135724041/a6c8ca35-484e-4e12-a9c8-0e0dd589555f">


#### Step 5(a): Connect RDS with Web App server:

The Web Server instance that you created in the previous computer lab contains code that generates a simple address book to RDS. The Endpoint URL of the RDS must be verified first in order to use the RDS on the EC2 Web Server.

##### Step5(b): Storing RDS Credentials in AWS Secrets Manager:

The web server we built includes sample code for our address book. In this lab, you specify which database to use in the sample code and how to connect it. We will store that information in AWS Secrets Manager.

In this chapter, we will create a secret containing data connection information. Later, we will give the web server the appropriate permission to retrieve the secret.

* In the console window, open AWS Secrets Manager (https://console.aws.amazon.com/secretsmanager/ ) and click the Store a new secret button.

* Under Secret Type, choose Credentials for Amazon RDS database. Write down the user name and password you entered when creating the database. And under Database select the database you just created. Then click the Next button.

* 
        KEY	            VALUE
    User name	        awsuser
    Password	        awspassword

* Name your secret, mysecret. The sample code is written to ask for the secret by this specific name. Click Next.
* Leave Secret rotation at default values. Click Next.
* Review your choices. Click Store.
* You can check the list of secret values with the name mysecret as shown below.
* Click mysecret hyperlink and find Secret value tab. And click Retrieve secret value button.
* Click Edit button, and check whether there is dbname and immersionday in key/value section. If they were not, click Add button, fill out the value and click save button.

##### Step 5(c):Access RDS from EC2:

<b>Allow the web server to access the secret</b>

* Sign in to the AWS Management Console and open the IAM console  . In the navigation pane, choose Policies, and then choose Create Policy.
* Click Choose a service.
* Type Secrets Manager into the search box. Click Secrets Manager.
* Under Access level, click on the carat next to Read and then check the box by GetSecretValue.
* Click on the carat next to Resources. For this lab, select All resources. Click Next: Tags.
* Click Next: Review.
* On the Review Policy screen, give your new policy the name ReadSecrets. Click Create policy.
* In the navigation pane, choose Roles and type SSMInstanceProfile into the search box. This is the role you created previously in Connect to your Linux instance using Session Manager. Click SSMInstanceProfile.
* Under Permissions policies, click Attach policies.
* Search for the policy you created called ReadSecrets. Check the box and click Attach policy.
* Under Permissions policies, verify that AmazonSSMManagedInstanceCore and ReadSecrets are both listed.

##### Try the Address Book:

* Access the [EC2 Console] (https://console.aws.amazon.com/ec2/v2/home?instanceState=running ) window and click load balancer. After copying the DNS name of the load balancer created in the compute lab, open a new tab in your browser and paste it.

* After connecting to the web server, go to the RDS tab.
* Now you can check the data in the database you created.
* This is a very basic exercise in interacting with a MySQL database managed by AWS. RDS can support much more complex relational database scenarios, but hopefully this simple example will make the point clear. You are free to add/edit/delete content from the RDS database using the Add Contact, Edit and Remove links in the address book.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge/assets/135724041/af934568-3a77-4b19-bf82-b23cd0c3e7a3">



### Step6: Create Bucket on S3:

All objects in Amazon S3 are stored within a bucket. You must create a Bucket before storing data on Amazon S3.

#### Create Bucket:

* From the AWS Management Console, connect to S3 . Press Create bucket to create a bucket.
* Enter a unique bucket name in the Bucket name field. For this lab, type immersion-day-user_name, substituiting user-name with your name. All bucket names in Amazon S3 have to be unique and cannot be duplicated. In the Region drop-down box, specify the region to create the bucket. In this lab, select the region closest to you. The images will show the Asia Pacific (Seoul) region. Object Ownership change to ACLs enabled. Bucket settings for Block Public Access use default values, and select Create bucket in the lower right corner.
* A bucket has been created on Amazon S3.

#### Adding objects to buckets:

If the bucket has been created successfully, you are ready to add the object. Objects can be any kind of file, including text files, image files, and video files. When you add a file to Amazon S3, you can include information about the permissions and access settings for that file in the metadata.
Adding objects for static Web hosting

This lab hosts static websites through S3. The static website serves as a redirect to an instance created by the VPC Lab when you click on a particular image. Therefore, prepare one image file, one HTML file, and an ALB DNS name.

* Download the image file aws.png  and save it as aws.png: https://static.us-east-1.prod.workshops.aws/public/dd38a0a0-ae47-43f1-9065-f0bbcb15f684/static/common/s3_advanced_lab/aws.png

* Write index.html using the source code below.

  ```
<html>
    <head>
        <meta charset="utf-8">
        <title> AWS General Immersion Day S3 HoL </title>
    </head>
    <body>
        <center>
        <br>
        <h2> Click image to be redirected to the EC2 instance that you created </h2>
        <img src="{{Replace with your S3 URL Address}}" onclick="window.location='DNS Name'"/>
        </center>
    </body>
</html>

  ```
* Upload the aws.png file to S3. Click S3 Bucket that you just created.
* Click the Upload button. Then click the Add files button. Select the pre-downloaded aws.png file through File Explorer. Alternatively, place the file in Drag and Drop to the screen.
* Check the file information named aws.png to upload, then click the Upload button at the bottom.
* Check the URL information to fill in the image URL in index.html file. Select the uploaded aws.png file and copy the Object URL information from the details on the right.
* Paste Object URL into the image URL part of the index.html. Then specify the ALB DNS Name of the load balancer created by Deploy auto scaling web service to redirect to ALB when you click on the image.
* Upload the index.html file to S3 following the same instructions as you did to upload the image.
* If you check the objects in your S3 bucket, you should see 2 files.




