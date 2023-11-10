# Database Migration of MariaDB databse from EC2 Instance to Amazon RDS MySQL using Amazon Database Migration Service(DMS)

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/e4af4a9f-3174-4eb1-921f-1ceecad5a8bc">
<br>

Migrating a MariaDB database from an Amazon EC2 instance to an Amazon RDS MySQL database using the AWS Database Migration Service (DMS) involves several steps.


Once Signed In to the AWS Management Console, make the default AWS Region as US East (N. Virginia) us-east-1 for the entire process.

## Step 1: Create VPC:

Creating a Virtual Private Cloud (VPC) with two public subnets and two private subnets, spanning two Availability Zones (AZs).

1. In the AWS Management Console, search for VPC 
2. Go to the VPC Dashboard.
3. Create a VPC: Click on "Create VPC" Choose "VPC and More" option.
4. Create VPC with following details:
    VPC Name: migration
    CIDR block:10.0.0.0/16
    No.of AZ's: 2
    No.of Public subnets: 2
    No.of Private Subnets: 2
    Select checkbox : Enable DNS hostnames and Enable DNS resolution
   
<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/a9822113-716c-4397-80f0-43a16f9c5460" width=300 height=300>

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/a0268749-ad9b-4121-8d0c-bf5883b15400" width=300 height=300>

5. Click on "Create VPC".

6. <img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/939d55d4-ce0a-4b8c-9077-0beb6b43635d"
width=300 height=300>


## Step 2: Create a Source Database on EC2 (Linux) Instance and Install MariaDB Server:
 
1. In this task, we are going to create a new EC2 (Linux) Instance that will serve as the source database for the migration to Amazon RDS instance

2. Make sure you are in the US East (N. Virginia) Region. 

3. Navigate to Services menu in the top, then click on EC2 in the Compute section.

4. Click on Instances from the left sidebar and then click on Launch instances.

5. Launch an EC2 instance with follwoing details:
   
  Name : ec2sourcedatbase
  For Amazon Machine Image (AMI): Select Linux.
  For Instance Type: select t2.micro
  For Key pair: Select Create a new key pair Button
  Key pair name: ec2sourceKP
  Key pair type: RSA
  Private key file format: .pem.

  <img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/a3afb3c1-b57b-4e67-999b-1dca08fce2ac" width=300 height=300>

   <img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/04d7a894-3aeb-4fb8-996d-ec30b36fa748" width=300 height=300>
  
<br>
6. In Network Settings, Click on Edit:
  Choose VPC: migration (vpc cretaed in step1)
  Auto-assign public IP: Enable
  Select Create a new security group
  Security group name : Enter MigrationSG
  Description : Enter MigrationSG
  
  To Choose SSH,
    Choose Type : SSH
    Source : Security best practice is : choose My IP or Custom IP

  Click on Add security group rule
    Choose Type : MYSQL/Aurora 
    Source : Anywhere

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/a827a769-ecdd-4abe-9d5d-35a3b44e9b77" width=600 height=300>

7. In the advanced setting section, copy and paste the below script in the User data.

   With this script  we are going to install and start MariaDB server on the Linux EC2 instance that was launched in the previously. MariaDB is a popular open-source relational database management system, and it needs to be installed on the EC2 instance to serve as the source database for the migration process.

  ```
    #!/bin/bash
    sudo dnf update -y
    sudo dnf install mariadb105-server -y
    sudo systemctl start mariadb
    sudo systemctl enable mariadb
   ```

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/c4df809c-3f2b-4d4d-9253-a551a4f69e57" width=300 height=300>


8. Keep rest thing Default and Click on Launch Instance Button.

9. Click on View Instances. After couple of mins, Instance State will become running and is ready.

10. Note down the IPv4 Public IP address.

11. SSH into the EC2 instance with public IP address of EC2 instance and key pair .pem file downloaded before.Follow these steps  [SSh_Into_Linux_Instance.md file ](./week4/Labs/SSH_Into_Linux_Instance.md) 
    
12. Check the MariaDB server installation and status on the EC2 instance.

    * Once connected to the server, switch to root user
    *  sudo su
   
13. Now, we have to set the password, for the root user. Please keep a note of this password as we will use this in upcoming steps. To set the default password,  please run the below-provided commands one by one:

14. Now you can only log in using the password you have set and nothing else.After successful login, you will be able to see the welcome message and mysql> prompt waiting for your command:

15. Make sure you do not give any extra spaces while executing these commands.
    
##### 16. Create a simple custom Database on Source EC2:

we will create a simple database and create a table inside which will be migrated using DMS.

1. SSH back to Source EC2 Instance if you are out of it.

2. Connect to Source MySQL Client .
   
3. Create a Database

4. Switch the database <b> awschallenge</b>.

5. Create a sample Table of  <b>Cohort </b>.

6. Create a sample Table of  <b>Students_Details </b>.

7. Insert data into the table  <b>Cohort </b>.
   

8. Insert data into the table <b>Students_Details </b>.

9. Check the items added in the Tables.

10. After database migration, this new custom tables can be used as proof of database migration.


      
    

## Step 2:Create an AWS RDS - MySQL Instance (Destination Database):

In the AWS Management Console, navigate to Amazon RDS.
Create an RDS MySQL instance, specifying configuration details like instance type, storage, and database credentials.

## Step 3:Create a Replication Instance:

In the DMS console, go to "Replication instances" and create a replication instance.
Configure the replication instance with the desired instance class, VPC, and other settings.
Ensure that the replication instance is in the same VPC as your source and target databases, as well as the appropriate subnets and security groups.


## Step 3:Create a Replication Instance:

In the DMS console, go to "Replication instances" and create a replication instance.
Configure the replication instance with the desired instance class, VPC, and other settings.
Ensure that the replication instance is in the same VPC as your source and target databases, as well as the appropriate subnets and security groups.

## Step 4: Create Endpoints for Your Source and Destination Databases:

In the AWS DMS console, create source and target endpoints.
For the source endpoint, specify the EC2 instance with MariaDB, including connection details.
For the target endpoint, select the RDS MySQL instance you created in step 4, and provide the necessary connection details.


## Step 5:Create a Database Migration Task:

In the DMS console, create a database migration task.
Associate the task with the source and target endpoints you created in step 5.
Configure the task settings, including migration type, table mappings, and any additional task settings as needed.

## Step 6: Start the Database Migration Task:

After setting up the migration task, start it from the DMS console.
DMS will begin replicating data from the source (EC2 MariaDB) to the target (RDS MySQL) as specified in your task settings.
Monitor the Migration:

Continuously monitor the DMS console to track the progress of your migration task.
Verify that data is being replicated correctly, and address any errors or issues that may arise during the migration process.
Data Validation and Cutover:

Once the migration task is complete, validate the data in the RDS MySQL instance to ensure data integrity.
Plan for a cutover by stopping any writes to the source MariaDB database on the EC2 instance and making the RDS MySQL instance the new production database.
Update Application Configuration:

Update your application's configuration to point to the new RDS MySQL database as the destination.
Test Your Application:

Thoroughly test your application with the new RDS MySQL instance to ensure it works as expected and all data is accessible.


Cleanup:

After confirming that the migration was successful and your application is functioning properly with the RDS MySQL instance, you can terminate or decommission the EC2 instance running MariaDB, as it is no longer needed.

