
Create a Source Database on EC2 (Linux) Instance and Install MariaDB Server:

Launch an EC2 instance with a Linux AMI.
SSH into the EC2 instance.
Install the MariaDB server on the EC2 instance.
Create an AWS RDS - MySQL Instance (Destination Database):

In the AWS Management Console, navigate to Amazon RDS.
Create an RDS MySQL instance, specifying configuration details like instance type, storage, and database credentials.
In DMS, Create Endpoints for Your Source and Destination Databases:

In the AWS DMS console, create source and target endpoints.
For the source endpoint, specify the EC2 instance with MariaDB, including connection details.
For the target endpoint, select the RDS MySQL instance you created in step 4, and provide the necessary connection details.
Create a Replication Instance:

In the DMS console, go to "Replication instances" and create a replication instance.
Configure the replication instance with the desired instance class, VPC, and other settings.
Ensure that the replication instance is in the same VPC as your source and target databases, as well as the appropriate subnets and security groups.
Create a Database Migration Task:

In the DMS console, create a database migration task.
Associate the task with the source and target endpoints you created in step 5.
Configure the task settings, including migration type, table mappings, and any additional task settings as needed.
Start the Database Migration Task:

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
