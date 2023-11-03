
VPC Peering
A VPC peering connection is a networking connection between two VPCs that enables you to route traffic between them using private IPv4 addresses or IPv6 addresses.
In this lab, we will establish VPC peering connections between VPC A and VPC B and between VPC A and VPC C, and show that traffic flows between only those VPCs with direct peering links.
Note that all three VPCs have non-overlapping CIDRs. You cannot create a VPC peering connection between VPCs with matching or overlapping IPv4 CIDR blocks.
Create three VPCs with the following details( Ref: Amazon VPC Creation )
Create VPC A: 
Name: VPC A
IPv4 CIDR block: 10.0.0.0/16
Create one public subnet with CIDR block: 10.0.0.0/24 and one private subnet with CIDR block: 10.0.1.0/24in Availability Zone A
Create one public subnet with CIDR block: 10.0.2.0/24 and one private subnet with CIDR block: 10.0.3.0/24 in Availability Zone B
Setup NACL, Route tables, Internet Gateway, NAT gateway 
Launch the EC2 instance in the private subnet of AZ1 and assign primary IP:10.0.1.100 and in the public subnet of AZ2 and assign primary IP: 10.0.2.100 as per the architecture

Create VPC B:
Name: VPC B
IPv4 CIDR block: 10.1.0.0/16
Create one public subnet with CIDR block: 10.1.0.0/24 and one private subnet with CIDR block: 10.1.1.0/24in Availability Zone A
Create one public subnet with CIDR block: 10.1.2.0/24 and one private subnet with CIDR block: 10.1.3.0/24 in Availability Zone B
Setup NACL, Route tables, Internet Gateway, NAT gateway
Launch the EC2 instance in the private subnet of AZ1 as per the architecture and assign the primary IP:10.1.1.100

Create VPC C:
Name: VPC C 
IPv4 CIDR block: 10.2.0.0/16
Create one public subnet with CIDR block: 10.2.0.0/24 and one private subnet with CIDR block: 10.2.1.0/24in Availability Zone A
Create one public subnet with CIDR block: 10.2.2.0/24 and one private subnet with CIDR block: 10.2.3.0/24 in Availability Zone B
Setup NACL, Route tables, Internet Gateway, NAT gateway
Launch the EC2 instance in the private subnet of AZ1 as per the architecture and assign primary IP: 10.2.1.100

Setup VPC A and VPC B Peering

Create the Peering Connection Between VPCs A & B

In the VPC Dashboard click on Peering Connections
Click on Create a peering connection in the right-hand corner
Specify the Peering connection name as VPC A <> VPC B
Under Select a local VPC to peer with select VPC A as VPC ID (Requester)

5. Under Select another VPC to peer with ensure that My Account is selected for Account
For Region select the region for this workshop This Region (us-east-1).
For VPC ID (Accepter) select VPC B
Click on Create peering connection

6. The newly created peering connection will be in Pending Acceptance state.
7. On the resulting screen, navigate under Actions and click Accept request
8. On the following pop-select, click Accept request
9. Click on Modify my route tables now in the resulting screen
Update Route Table in VPC A
Click Edit routes
Select the check box for the VPC A Private Route Table
Scroll down and click on the Routes tab
Click Edit routes
Add route entry for "VPC B" using the CIDR range 10.1.0.0/16 and selecting Peering Connection VPC A <> VPC B for the target

5. Click Save Changes. Confirm that the new route appears in the Routes tab of the resulting screen
Update Route Table in VPC B
Click on Route tables
Select the check box for VPC B Private Route Table
Click on the Routes tab
Click Edit routes
Add a route entry for VPC A using CIDR range 10.0.0.0/16 as the Destination and VPC A <> VPC B as the target
Click Save changes
The route table will be updated with routes for the peering connection

Setup VPC A and VPC C Peering
In the VPC Dashboard click on Peering Connections
Click on Create peering connection in the right hand corner
Specify the Peering connection name as VPC A <> VPC C
Under Select a local VPC to peer with select VPC A as VPC ID (Requester)
Under Select another VPC to peer with ensure that My Account is selected for Account
For Region select the region for this workshop This Region (us-east-1).
For VPC ID (Accepter) select VPC C
Click on Create peering connection

9. The newly created peering connection will be in Pending Acceptance state.
10. On the resulting screen, navigate under Actions and click Accept request
11. On the following pop-select, click Accept request
12. Click on Modify my route tables now in the resulting screen
Update Route Table in VPC 
Select check box for VPC A Private Route Table
Scroll down and click on Routes tab
Click Edit routes
Add route entry for "VPC C" using the CIDR range 10.2.0.0/16 and selecting Peering Connection VPC A <> VPC C for the target
Click Save changes
Confirm that the new route appears in the Routes tab of the resulting screen

Update Route Table in VPC C
Navigate back to Route Tables and select check box for VPC C Private Route Table
Click on Routes tab
Click Edit routes
Add a route entry for VPC A using CIDR range 10.0.0.0/16 as the Destination and VPC A <> VPC C as the Target
Click Save changes
The route table will be updated with routes for the peering connection

Check Connectivity:

Check Connectivity from VPC A
Select the VPC A Private AZ1 Server EC2 instance and click the Connect button above
Proceed to EC2 Console .
Select the VPC A Private AZ1 Server EC2 instance and click the Connect button above
Click Connect in the Session Manager tab
Try pinging EC2 instances in VPC B and VPC C using the private addresses of the instances

ping 10.1.1.100 -c 5
ping 10.2.1.100 -c 5
If peering and routing are configured correctly, you should be able to ping both instances.
Check Connectivity from VPC B
Select VPC B Private AZ1 Server EC2 instance and connect using Session Manager.
Terminate the Session Manager connection and in the resulting screen click on Instances.
Select VPC B Private AZ1 Server EC2 instance and connect using Session Manager.
Ping the EC2 instance in VPC A using the IP address 10.0.1.100

ping 10.0.1.100 -c 5
Can you ping the instance in VPC C using the IP address 10.2.1.100?
ping 10.2.1.100 -c 5
There is no direct peering between VPC B and VPC C. VPC B and VPC C cannot communicate via VPC A because VPC peering does not permit transitive routing.
Terminate the Session Manager connection and close the browser tab.
Congratulations you've set up a peering architecture that connects VPC A to VPC B and VPC C but prevents VPC B and VPC C communicating.
While this approach can be used to interconnect many VPCs, managing many point-to-point connections can be cumbersome at scale. A more scalable approach is to utilize AWS Transit Gateway so we will now remove the point-to-point peering connections between VPCs in preparation for setting up Transit Gateway (TGW) to interconnect the three VPCs
Delete VPC Peering Connections
In the VPC Dashboard navigate to Peering Connections
Select the VPC A <> VPC B peering connection and delete it by clicking Actions and selecting Delete peering connection
Select the checkbox to Delete related route table entries to avoid traffic blackholing scenarios.
Type delete in the text box and click Delete
Repeat deletion of VPC peering for the VPC A <> VPC C connection.

Congratulations you now have now completed this section of the lab.
