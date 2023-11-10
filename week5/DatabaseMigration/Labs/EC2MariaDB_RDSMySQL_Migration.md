# Database Migration of MariaDB databse from EC2 Instance to Amazon RDS MySQL using Amazon Database Migration Service(DMS)

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/e4af4a9f-3174-4eb1-921f-1ceecad5a8bc">
<br>

Migrating a MariaDB database from an Amazon EC2 instance to an Amazon RDS MySQL database using the AWS Database Migration Service (DMS) involves several steps.


Once Signed In to the AWS Management Console, make the default AWS Region as US East (N. Virginia) us-east-1 for the entire process.

## Step 1: Create a Source Database on EC2 (Linux) Instance and Install MariaDB Server:
 
1. In this task, we are going to create a new EC2 (Linux) Instance that will serve as the source database for the migration to Amazon RDS instance

2. Make sure you are in the US East (N. Virginia) Region. 

3. Navigate to Services menu in the top, then click on EC2 in the Compute section.

4. Click on Instances from the left sidebar and then click on Launch instances.

5. Launch an EC2 instance with follwoing details:
   
  Name : Enter SourceEC2Instance
  For Amazon Machine Image (AMI): Select Ubuntu in quickstart and in the drop box.
  For Instance Type: select t2.micro
  For Key pair: Select Create a new key pair Button
  Key pair name: WhizKey
  Key pair type: RSA
  Private key file format: .pem.

6. In Network Settings, Click on Edit:

  Auto-assign public IP: Enable
  Select Create a new security group
  Security group name : Enter MigrationSG
  Description : Enter MigrationSG

   














SSH into the EC2 instance.
Install the MariaDB server on the EC2 instance.

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

