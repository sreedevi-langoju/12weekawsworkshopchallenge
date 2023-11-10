# Database Migration of MariaDB data on EC2 Instance to Amazon RDS MySQL using Amazon Database Migration Service(DMS)

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/e4af4a9f-3174-4eb1-921f-1ceecad5a8bc" width=800 height=600>
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
   
<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/a9822113-716c-4397-80f0-43a16f9c5460" width=400 height=400>

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/a0268749-ad9b-4121-8d0c-bf5883b15400" width=400 height=400>

5. Click on "Create VPC".

 <img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/939d55d4-ce0a-4b8c-9077-0beb6b43635d"
width=500 height=400>


## Step 2: Create a Source Database on EC2 (Linux) Instance and Install MariaDB Server:
 
1. In this task, we are going to create a new EC2 (Linux) Instance that will serve as the source database for the migration to Amazon RDS instance

2. Make sure you are in the US East (N. Virginia) Region. 

3. Navigate to Services menu in the top, then click on EC2 in the Compute section.

4. Click on Instances from the left sidebar and then click on Launch instances.

5. Launch an EC2 instance with following details:
   
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

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/c4df809c-3f2b-4d4d-9253-a551a4f69e57" width=600 height=300>


8. Keep rest thing Default and Click on Launch Instance Button.

9. Click on View Instances. After couple of mins, Instance State will become running and is ready.

10. Note down the IPv4 Public IP address.

11. SSH into the EC2 instance with public IP address of EC2 instance and key pair .pem file downloaded before.Follow these steps  [SSh_Into_Linux_Instance.md file ](./SSH_Into_Linux_Instance.md) 
    
12. Check the MariaDB server installation and status on the EC2 instance.

    switch to root user:   
        
    
              sudo su 
    
 
<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/63a7e96c-aba9-4de7-80bc-3f7995b08e65" width=600 height=300>

 Once connected to the server, check the status of the MariaDB server
  
             sudo systemctl status mariadb  
       

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/e3ae7a1f-0ee5-46f1-a2ba-5b4f4bcb0681" width=600 height=300>

   
13. Now log into mariadb server using command :
              mysql -u root -p 

14. It prompts for passsword, the default password for root user in Mariadb is nothing , so just press enter.

15. Now, we have to set the password, for the root user. Please keep a note of this password as we will use this in upcoming steps. To set the default password,  please run the below-provided commands one by one:
    
     
             SET PASSWORD FOR 'root'@'localhost' = PASSWORD ('enter your new password here');
             FLUSH PRIVILEGES;
             exit;
     
    
    <img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/72bb0a4a-d8f7-41f8-840d-088fe9309098" width=600 height=300>

17. Now stop and start the mariadb server using below commands.
    
         
        sudo systemctl stop mariadb
        sudo systemctl start mariadb
    
        

18. Now you can only log in using the password you have set and nothing else.After successful login, you will be able to see the welcome message and mysql> prompt waiting for your command.

Note: Make sure you do not give any extra spaces while executing these commands.
    
##### 19. Create a simple custom Database on Source EC2:

we will create a simple database and create a table inside EC2 Mariadb which will be migrated using DMS.

1. SSH back to Source EC2 Instance if you are out of it.

2. Connect to Source MySQL Client using user : root and password: new password you set before
   
3. Please find the database queries in the attached [dbschema.sql file](./dbschema.sql).

4. Create a Database

5. Switch the database <b> awschallenge</b>.

6. Create a sample Table of  <b>Cohort </b>.

7. Create a sample Table of  <b>Students_Details </b>.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/f7e9e71b-699f-4dca-afdf-4bbc1e23edee" width=500 height=300>

8. Insert data into the table  <b>Cohort </b>.  

9. Insert data into the table <b>Students_Details </b>.

10. Check the items added in the Tables.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/8073feea-5297-4a67-8fff-32ddeb07e46b" width=500 height=300>


11. After database migration, this new custom tables can be used as proof of database migration.
    

## Step 2:Create an AWS RDS - MySQL Instance (Destination Database):

In the AWS Management Console, navigate to Amazon RDS.

Create an RDS MySQL instance, specifying configuration details like instance type, storage, and database credentials.

1. Click on the Services and select the RDS under the Database section.

2. In the left navigation pane, click on Databases.Make sure you are in N.Virginia Region.

3. Click on Databases from the left navigation menu and then click Create database

4. Specify DB details:

    Instance specifications:
   
         Database creation method : Standard create
         Engine options : Select MySQL
         Version : Default
         Template : Select Free tier
         DB instance identifier : mysqltarget-database
         Master username. : admin
         Master password and Confirm password: enter your password 

            Note: This is the username/password combo used to log onto your database. Please make note of them somewhere safe.
   
         DB instance class : Select Burstable classes db.t3.micro
         Storage type : Select General Purpose SSD (gp2)
         Allocated storage : Select 20 (default)
         Enable storage autoscaling : Uncheck
         Virtual Private Cloud(VPC) : migration-vpc(created in step1)
         Subnet group : Select Default
         Public Access : Select No
         VPC Security groups : Select Choose existing
         Existing VPC security group name : Remove the default security group and select MigrationSG from the dropdown list

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/2f585895-327a-4fe3-bbcf-40fe041fc17f" width=500 height=300>

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/69a11a2f-8807-4b2f-b63d-904f312c78e5" width=500 height=300 >

<br><br><br>

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/2a6308c3-743e-494c-98b8-0940eff4a672" width=500 height=300>

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/09756f6e-31d2-45fc-aa8f-0711c7ea3058" width=500 height=300> 


6. Scroll down to Additional Configuration options

         Initial database name:  awschallenge
         DB parameter group: Select default
         Option group: Select default
         Enable automated backups: uncheck
         Enable auto minor version upgrade: uncheck
         Maintenance window: Select No preference
         Enable deletion protection: uncheck

7. Leave other parameters as default. Scroll to the bottom of the page, Click Create database.

It will take around 5 minutes for the database to become available. Once the status changes from creating to available, the database is ready.

Open target-database and note down the Endpoint of RDS under Connectivity and security

Example: mydbinstance.c81x4bxxayay.us-east-1.rds.amazonaws.com


## Step 3:Create a Replication Instance:

In this task, we are going to create a replication instance in the AWS Database Migration Service (DMS). The replication instance will be used to replicate data from an EC2 MySQL database to an Amazon RDS database.Ensure that the replication instance is in the same VPC as your source and target databases, as well as the appropriate subnets and security groups.

1. Click on Services and then choose Database Migration Service under the Migration & Transfer.Make sure you are in the N.Virginia region.

2. Click on Replication instances from the left navigation menu and then click Create replication instance.

3. In the Replication instance configuration section,

      Name : dbmiration
      Description : Enter any description
      Instance class : Select dms.t3.medium
      Engine version : Default
      Allocated storage (GB) : Enter 10 GB
      High Availability : Select Dev or test workload (Single-AZ).
      VPC : migration-vpc( created in step1)
      Publicly accessible : Check

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/f5bbfbd1-2801-44db-9681-0cc13afdb82f" width=500 height=300>

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/8699893e-b0c2-4e73-81e7-1af916dd1bfa" width=500 height=300>

5. In Advanced security and network configuration section,

      Replication subnet group : Default
      Availability zone : Default
      VPC security group(s) : Enter MigrationSG
      KMS master key : Default

7. Leave other settings as default.

Click on the  Create button to create the replication instance.

      NOTE : Ignore the error and click on Create button again
      
8. It will take 5 minutes for a replication instance to be created. Once status changes to available, click on the instance and scroll down. You will find the details section of the replication instance.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/1fb3e4c5-54b3-4f73-94df-26c10193cf86">

Select dbmiration from Details section, copy the private & public IP address and note it down on the notepad.

Ex: Public IP address : 34.179.22.178

Ex: Private IP address : 10.0.0.22

##### Configure Replication Instance details in Source EC2 Instance:

9. Login to the MySQL:

SSH back into EC2 insatnce.
login to Mariadb server: ``` mysql -u root -p ``` ( use new passowrd)

10. Command syntax to create a new user in a MySQL Database 

           CREATE USER 'root'@<<Private IP of Replication Instance>> IDENTIFIED BY 'your-root-password'; 

Example : CREATE USER 'root'@10.0.9.95 IDENTIFIED BY 'your-root-password';

11. We need to grant root access to the replication instance to connect with the MySQL server on Source EC2. 
 
          GRANT ALL ON *.* TO root@<<Private IP of Replication Instance>>; 
    
Example:   GRANT ALL ON *.* TO root@10.0.9.95;

12. And repeat the same step now with the Public IP address of the replication instance.

         CREATE USER 'root'@<<Public IP of Replication Instance>> IDENTIFIED BY 'your-root-password';
    
         GRANT ALL ON *.* TO root@<<Public IP of Replication Instance>>;


Example : CREATE USER 'root'@44.214.111.130 IDENTIFIED BY ''your-root-password'';
Example : GRANT ALL ON *.* TO root@44.214.111.130;

 
13. Save the changes by using the following command:  

          FLUSH PRIVILEGES; 


<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/659497ed-9ad6-454d-a802-e93fd93ed098" width=500 height=300>

14. Now stop and start the mariadb server using below commands.
    
         
        sudo systemctl stop mariadb
        sudo systemctl start mariadb


## Step 4: Create Endpoints for Your Source and Destination Databases:

In the AWS DMS console, we have to create the Source and Target endpoints for EC2 and RDS Instances. These endpoints will help to connect the replication instance with both source and target machines. 

#### Source Endpoint

1.Make sure you are in N.Virginia (us-east-1) region.

2.To create an Endpoint, Click on the Endpoints (Left panel) in the DMS service console page and click on Create endpoint
Follow the below steps to complete Endpoint type:

3. Select endpoint as Source endpoint

    Select RDS DB instance: Uncheck (This is for Source, i.e. Mariadb on EC2)
    Endpoint configuration:
    Endpoint identifier : ec2source-database
    Descriptive Amazon Resource Name (ARN): sourcemysqlendpoint
    Source engine : Select MariaDB

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/c2d5749b-4754-4302-9859-c62bea7fdb66" width=500 height=400>

    Access to endpoint database: Choose Provide access information manually
    Server name : Public IP address of Source EC2 Instance (Enter your IP)
    Port : 3306
    Username :  root
    Password :  enter your root password( Which was created earlier)
    Secure Socket Layer (SSL) mode: None
    Leave other configurations as default.

    
<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/8bf7d7c1-eff6-4b89-ad0c-f7d227c36ec4" width=500 height=400>


    Test endpoint connection:
        VPC : migration (Which was created earlier)
        Replication instance : Enter dbmigration (Which was created earlier)
        
        
5. Click on Run test to test the connection. If all are working fine, you will be able to see the status as “successful” as         shown in the below screenshot.


<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/bfa82f9c-3ffa-4810-abca-93d1eebc0c56" width=500 height=400>


6. Click on Create Endpoint.
   

#### Target Endpoint:

1. To create an Endpoint, Click on the Endpoints(Left panel) in the DMS service console page and click on the Create endpoint button

2. Follow the below steps to complete Endpoint type:

        Select endpoint as Target endpoint
        Select RDS DB instance: check (This is for Target i.eRDS Instance)
        RDS insatnce details populate automatically

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/79cc3c8f-e9f9-4324-b8c1-707a24c06b41" width=600 height=400>


        Select Access to endpoint database: Choose Provide access information manually
        Server name :  DNS Endpoint of RDS database populate automatically
        Port : Enter 3306
        Secure Socket Layer (SSL) mode: None
        User name : admin
        Password : enter your admin password( which created earlier)
        Leave other settings as default.
        
<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/f51218eb-7620-4d1d-8a22-6dd7b3a3804f" width=600 height=400>


4. Test endpoint connection:

        VPC : Default
        Replication instance : Enter dbmigration (Which we created earlier)

5. Click on Run test to test the connection.If all are working fine, you will be able to see the status as “successful” as shown in the below screenshot.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/b047e071-c2a3-4ea1-9060-240f13c971ba" width=600 height=400>

   
6. Click on the Create endpoint  button.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/9d6c5da0-1a0d-4973-a1a3-60da6b3ea3ec">

## Step 5:Create a Database Migration Task:


In the DMS console, create a database migration task.
Associate the task with the source and target endpoints you created in step 4.

An AWS Database Migration Service task is where all the migration process happens. We will specify the tables and schemas to use for the migration and any special processing, such as logging requirements, control table data, and error handling.

1. Navigate to AWS DMS console and click on the Database migration tasks.Make sure you are in N.Virginia (us east-1) Region.

2. Click on Database migration tasks from the left navigation menu and then click Create task

3. Create a database migration task:

    Task configuration:

        Task identifier : Database-Migration-Task
        Replication instance : Select dbmigration
        Source database endpoint : Enter mysqlsource-database
        Target database endpoint : Enter target-database
        Migration type : Migrate existing data

    Task settings:

        Editing mode: Wizard
        Target table preparation mode: Do nothing
        LOB column settings: Limited LOB mode
        Maximum LOB size (KB): 32 KB
        Validation: Uncheck Turn on
        Task logs: Uncheck Turn on cloudwatch logs
        Leave Advance tasks settings as default.

  Table mappings:

        Editing mode : Wizard
        Selection rules : Click on Add new Selection rule button
        Schema : Select Enter a Schema
        Source name : Enter %awschallenge (Database name)
        Source table name : Enter % (all tables)
        Action : Include

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/9353c24d-463d-4199-b7ba-28a852cd6f33" width=400 height=400>


<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/45dfc980-2f21-4b5c-a03a-22b941b2c2bd" width=400 height=400>

4. Leave other settings as default.

5. Click on Create task.

Now the migration of Database will occur. Usually it will take around 1 minute.

## Step 6:Status of AWS Database Migration Tasks:

Continuously monitor the DMS console to track the progress of your migration task.
Verify that data is being replicated correctly, and address any errors or issues that may arise during the migration process.

1. Navigate to Database migration tasks in left panel of DMS page.

   
2. If you followed all the previous steps correctly, it will show the migration task status as Load complete, replication ongoing
Now the Migration of database to Amazon RDS is completed.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/6b177ac1-259d-4513-bb18-f1fcd20a689c">

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/cf9d953b-a375-49c4-9c67-6a5af3982b17">


<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/43e0f91c-50bd-46a4-b548-c77b6de7a0ba">



3.To check the migration status and details, we need to connect to the destination MySQL database which is in AWS RDS Instance.

4. SSH back into Source EC2 Instance.

5. Connect to AWS RDS instance using below command :use user: admin paddword: your password( created earlier)

               mysql -h < RDS endpoint > -u admin -p

   
   <img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/e8d0afaa-5e42-414c-87ce-d0fb90eeb139">

6. Once inside MySQL Client, check the databases available.


   <img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/d6e4d693-3ef5-465d-8155-c7bb06393455">


7. Now we can see the awschallenge and its tables Cohort and Students_Details, which were available in Source EC2 Linux Server migrated to Amazon RDS Instance Database.

#### Congratuations, you successfully migrated MariaDB databse data from EC2 Instance to Amazon RDS MySQL using Amazon Database Migration Service(DMS)!!!

## Cleanup:
Don't forget to delete the configured resources when they are no longer needed to avoid unnecessary billing.

