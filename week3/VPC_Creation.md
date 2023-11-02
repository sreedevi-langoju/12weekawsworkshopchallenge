# Amazon VPC Creation:

Creating a Virtual Private Cloud (VPC) in Amazon Web Services (AWS) is a fundamental step in setting up your network infrastructure. A VPC allows you to launch AWS resources into a virtual network that you've defined.

For a comprehensive introduction to VPC and its fundamental components, consider checking out our dedicated blog post on 'VPC Fundamentals'.
 Here are the steps to create below architecture of VPC and its components in AWS:
 
### Step1: Create VPC

Click Deploy Pre-requisites for the steps to follow to create the necessary IAM roles, policies, and other resources before creating the VPC.
Sign in to the AWS Management Console: Open your web browser and go to the AWS Management Console. Sign in with your AWS account credentials.
Navigate to the VPC Dashboard: In the AWS Management Console, go to the "Services" menu and select "VPC" under the "Networking & Content Delivery" section.
Create a VPC: In the VPC Dashboard, click on the "Your VPCs" link on the left sidebar. Then click the "Create VPC" button.
Configure VPC Settings: You'll need to provide the following information when creating your VPC:

Enter VPC A as the Name tag
Specify 10.0.0.0/16 as IPv4 CIDR block.
Do not enable IPv6.
Leave Default selected as Tenancy.
Accept proposed Tags
Click Create VPC

5. After completing these steps, you should have a new VPC listed under Your VPC
6. Click on Actions > select Edit VPC settings from the dropdown, check the box to enable DNS hostnames, and select Save.
Congratulations, your first VPC is now built.


### Step2: Setup Subnets

A subnet is a range of IP addresses in your VPC. You can launch AWS resources into a specified subnet. Public subnets are for resources that must be connected to the Internet, and private subnets are for resources that won't be exposed to the Internet.
In this section, we will create two public and two private subnets in each of the two availability zones within your VPC.
In the VPC panel on the left click on Subnets
Click on the Create Subnet button in the top right corner.
Choose VPC A from the VPC ID dropdown.
In the Subnet settings section

Enter the name as VPC A Public Subnet AZ1
Select the Availablity Zone of us-east-1a
Enter a CIDR block of 10.0.0.0/24:
Click Create subnet

5. You should have a new subnet listed under Subnets.
6. Click on Create subnet again
7. Under Subnet settings
Select VPC A
Enter the name of VPC A Private Subnet AZ1
Select the Availablity Zone of us-east-1a
Enter a CIDR block of 10.0.1.0/24
Click Create subnet

8. Click on Create subnet again and
Select VPC A
Enter a name VPC A Public Subnet AZ2
Select the Availablity Zone of us-east-1b
Enter a CIDR block of 10.0.2.0/24

9. Click on Create subnet again and
Select VPC A
Enter the name of VPC A Private Subnet AZ2
Select an Availablity Zone of us-east-1b
Enter a CIDR block of 10.0.3.0/24:

10. After you finish the task, on the resulting Subnets screen
Confirm that four new subnets are available with names, CIDR blocks, and Availability Zones as below

### Step3: Setup Network ACLs

A network access control list (ACL) is an optional layer of security for your VPC for controlling traffic in and out of one or more subnets.
Create a new Network ACL for workload subnets in VPC A
On the VPC Dashboard click on Network ACLs
Click Create Network ACL

3. In the Network ACL settings screen
Enter the name of VPC A Workload Subnets NACL
Select VPC A from the dropdown
Click Create Network ACL

The result will be a new NACL for VPC A alongside the default NACL created when the VPC was created.
4. In the resulting Network ACLs screen
Select the checkbox for VPC A Workload Subnets NACL
Scroll down to the Subnet Associations tab
Click Edit subnet associations

The NACL should now be associated with four subnets on the following screen but because NACLs are created with only a DENY rule for inbound and outbound we will now change the default NACL rules to allow all traffic in both directions.
5. In the Network ACLs screen
Select the check box for VPC A Workload Subnets NACL for VPC A
Scroll down and select the Inbound Rules tab below
Notice that we have only DENY all rule
Click Edit inbound rules

6. In Edit inbound rules screen
Click Add new rule
Input 100 in Rule number
Choose All traffic in Type
Leave Source as 0.0.0.0/0
Click Save changes

In the resulting screen you should have a success banner and a new Allow rule under the Inbound rules tab.
7. Now follow the same steps described above for Inbound, but work on the Outbound Rules tab of NACLs
On the Outbound Rules tab
Note that we have only DENY all rule
Click Edit outbound rules

8. In the Edit outbound rules screen
Click Add new rule
Input 100 in Rule number
Choose All traffic in Type
Leave Destination as 0.0.0.0/0
Click Save changes

On the resulting screen check that the rule has been added under the Outbound Rules tab

### Step 4: Setup Route Tables

Your VPC has an implicit router, and you use route tables to control where network traffic is directed. Each subnet in your VPC must be associated with a route table, which controls the routing for the subnet (subnet route table). You can explicitly associate a subnet with a particular route table. Otherwise, the subnet is implicitly associated with the main route table. A subnet can only be associated with one route table at a time, but you can associate multiple subnets with the same subnet route table.
Create Route Table for Public Subnets
In the left-hand panel of the VPC Dashboard click on Route Tables.
You will see the default route table that was created as part of the VPC creation, and in the Subnet Associations tab below the four subnets created earlier. We will now create a new public route table for the public subnets with a route to the internet via the Internet Gateway.
Add a new public route table by clicking on Create route table in the right-hand corner
Enter VPC A Public Route Table as the name and select VPC A from the VPC dropdown. Click Create route table and a new route table will be created

 We need to associate this public route table with the public subnets we created earlier.
3. Scroll down and click on the Subnet Associations tab.
4. Click on Edit subnet associations
Select VPC A Public Subnet AZ1 and VPC A Public Subnet AZ2 and click Save association
5. The two public subnets will now be associated with the public route table under Explicit Subnet Associations within the Subnet Associations tab.
Create Route Table for Private Subnets:
6. In the left-hand panel of the VPC Dashboard click on Route Tables and click on the Create route table button in the top right corner
7. In the Create route table screen * Enter VPC A Private Route Table as the Name * Select VPC A from the dropdown for VPC ID * Click on Create route table
we need to associate the private subnets to the route table.
8. In the Subnet Associations tab click on Edit Subnet associations
9. Select the two private subnets VPC A Private Subnet AZ1 and VPC A Private Subnet AZ2 and click Save associations
10. In the resulting screen click on Route tables and confirm that there are three route tables under VPC A: main/default, Public, and Private.


### Step 5: Internet Connectivity

In this section, we will deploy an Internet Gateway (IGW) and NAT Gateway into our VPC.
An Internet Gateway establishes outside connectivity for EC2 instances that will be deployed into the VPC and provides both inbound and outbound connectivity to workloads running in public subnets whereas a NAT Gateway provides outbound connectivity for workloads running in private subnets.
Deploy an Internet Gateway
In the left-hand panel click on Internet Gateways and click on Create Internet Gateway
Enter VPC A IGW as the name and click Create Internet Gateway in the bottom right corner

3. On the success screen for the newly created IGW, click on Attach to VPC:
4. Select VPC A from the dropdown list for Available VPCs and click Attach Internet gateway. The Internet Gateway should attach successfully.
5. We now have an internet access point for our VPC, but in order to utilize the newly created Internet Gateway, we need to update VPC routing tables to point the default routes for our public subnets to this Internet Gateway.
Update Route Table for Public Subnets:

In left hand panel of the VPC Dashboard click on Route Tables and select VPC A Public Route Table
In left hand panel of the VPC Dashboard click on Route Tables and select VPC A Public Route Table
Scroll down to the Routes tab
As you can see there is only a local route, so we're going to enable internet access by adding a route to the Internet Gateway
Click on Edit Routes
In the resulting screen

Click on Add route
Enter 0.0.0.0/0 in the Destination

6. Select Internet Gateway from the Target dropdown.Choose VPC A IGW.Click Save changes and confirm that a new route has been added to the Routes tab
Next we will add outbound connectivity from the private subnets by deploying a NAT Gateway in a public subnet for use by workloads that should not be directly exposed to the internet.
Create NAT Gateway

In the left-hand panel of the VPC Dashboard click on NAT Gateways and click on Create NAT gateway.
In the Create NAT gateway screen * Enter VPC A NATGW as the name * Choose VPC A Public Subnet AZ1 * Click Allocate Elastic IP * Click Create NAT gateway

Upon creation, the NAT Gateway details are displayed.
Update Route Table for Private Subnets

Now that we have a NAT Gateway in a public subnet we need to create a route to it from the private subnets and we will do that by adding an entry to the Route Table for the private subnets.
In the left-hand panel of the VPC Dashboard click on Route Tables
Select VPC A Private Route Table, scroll down to the Routes tab, and click on Edit routes
In the Edit routes screen * Click on Add route * Enter 0.0.0.0/0 in the Destination * Select NAT Gateway from the Target dropdown. Choose VPC A NATGW and click on Save Changes.

4. Confirm the new route appears in the Routes tab of the resulting screen

   
### Step 6: EC2 instances

In this section, you will spin up EC2 instances in your VPC and protect them with a security group only allowing ICMP traffic to reach the hosts.
Launch an EC2 Instance into a Public Subnet
In the Instances section of the EC2 console click Launch Instances.
In the resulting Launch an instance screen

Enter VPC A Public AZ2 Server for the Name
Ensure that Amazon Linux 2023 AMI will be selected, and the instance type is t2.micro.
Under Key pair (login) select Proceed without a key pair. A key pair is not needed since we will be using Systems Manager to connect to the instances.

2. Under Network settings click Edit and
Select VPC A from the dropdown for the VPC field
Select VPC A Public subnet AZ2 from the dropdown for the Subnet field
Select Enable for the Auto-assign Public IP field

3. Select Create security group with the name VPC A Security Group, description of Open-up ports for ICMP
4. In Inbound security groups rules under Type select All ICMP - IPv4 and enter 0.0.0.0/0 as the Source
Since security groups are stateful, you don't need to edit the outbound rules. The security group will allow the instance to respond to the ping since it saw the ping arrive at the instance.
5. Expand the Advanced network configuration and under Primary IP enter 10.0.2.100.
6. At the bottom of the section
Expand Advanced details
Under the IAM Instance profile select NetworkWorkshopInstanceProfile which was created in the pre-requisites section.
Click Launch Instance

Congratulations! You have just launched a virtual server in your public subnet in AZ2.
Launch Instance in Private Subnet

In the Instances section of the EC2 console
Select the running public instance VPC A Public AZ2 Server.
You could follow the same process in the last two sections in order to deploy an EC2 instance into a private subnet, however, it is also possible to launch a new instance using the same settings as previously.
In the Instances section of the EC2 console

Select the running public instance VPC A Public AZ2 Server
Click Actions then Image and Templates then Launch more like this

4. In the settings screen
Update the Name to VPC A Private AZ1 Server
Under Key pair (login) select Proceed without a key pair.
Update the Subnet to be VPC A Private Subnet AZ1
Set the Auto-Assign Public IP setting to Disable.
Expand the Advanced network configuration and under Primary IP enter 10.0.1.100.
Click Launch Instance

Congratulations, you now have an EC2 instance running in both a public and private subnet.


### Step 7: Test Connectivity

In this section, you will use the EC2 instances in the public and private subnets of your VPC to test the connectivity for the network foundations you created in the previous section.
In the Instances section of the EC2 console

Select the VPC A Public AZ2 Server instance
Scroll down to the Details tab
Copy the Public IPv4 address field by clicking the copy icon to the left of it.

2. To ping the instance, you need to open your CLI. On Windows, open the Command Prompt. On Mac, open the Terminal.
3. Type ping then a space, then paste the Elastic IP from above, then space then -c 5 and enter.
If the instance is reachable, we expect to see lines appearing such as
Good job! You have successfully confirmed connectivity between the public EC2 instance and the internet.
Test Private Instance Connectivity
In the Instances section of the EC2 console

Select the VPC A Private AZ1 Server instance
Click on the Connect button

In the following screen, select the Session Manager tab and click Connect
This will open a terminal from which you can test connectivity to both the public instance at 10.0.2.100 and external connectivity to example.com via the NAT Gateway.
2. Copy the following ping commands and paste in the Session Manager console
ping 10.0.2.100 -c 5
ping example.com -c 5
You should receive responses both from the public EC2 instance and example.com.
Congratulations you have now confirmed outbound connectivity from both instances
