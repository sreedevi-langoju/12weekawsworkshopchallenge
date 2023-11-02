
1. Log In to AWS Console:
Log in to your AWS console using your AWS account credentials.

2. Create a VPC:

a. Go to the VPC Dashboard.
b. Click on "Your VPCs" in the left navigation pane.
c. Click the "Create VPC" button.
d. Provide a name for your VPC and specify the IPv4 CIDR block (e.g., 10.0.0.0/16).
e. Leave the other settings as default, unless you have specific requirements.

3. Create a Public Subnet:

a. In the VPC Dashboard, select your newly created VPC.
b. Click on "Subnets" in the left navigation pane.
c. Click the "Create Subnet" button.
d. Provide a name for your subnet.
e. Select the VPC you created earlier.
f. Specify the IPv4 CIDR block for the public subnet (e.g., 10.0.0.0/24).
g. Ensure that you choose an Availability Zone in the same region as your VPC.
h. For the "Route table," select the default route table, or create a new one if needed.

4. Create an Internet Gateway (IGW):

a. In the VPC Dashboard, select "Internet Gateways" in the left navigation pane.
b. Click the "Create Internet Gateway" button.
c. Give it a name and create the IGW.
d. Select the IGW, click "Actions," and choose "Attach to VPC." Attach it to your VPC.

5. Configure the Route Table:

a. Go to the "Route Tables" section in the VPC Dashboard.
b. Find the route table associated with your public subnet (usually the main one).
c. Edit the route table and add a route with destination 0.0.0.0/0 and target as the Internet Gateway you created.

6. Create or Use an Existing Key Pair:

If you don't have an existing EC2 key pair, you can create one. You will need this key pair to SSH into your EC2 instance. You can manage key pairs in the "Key Pairs" section of the EC2 Dashboard.

7. Launch an EC2 Instance:

a. Go to the EC2 Dashboard.
b. Click the "Launch Instances" button.
c. Choose an Amazon Machine Image (AMI) for your Linux instance.
d. Select an instance type.
e. Configure the instance details. In the "Subnet" section, select the public subnet you created.
f. Configure the instance details, including security groups, IAM roles, and user data if needed.
g. On the "Review" page, review your settings, and then click "Launch."
