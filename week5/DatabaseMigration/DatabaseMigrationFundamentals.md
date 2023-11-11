# Database Migration

Database Migration is the process of transferring data, schema, and configuration from one database system to another. It is a critical operation for businesses and organizations looking to change database platforms, upgrade versions, move to the cloud, or consolidate data.

## Amazon DMS (Database Migration Service) :
Amazon Database Migration Service (DMS) is a fully managed database migration service provided by Amazon Web Services (AWS). It simplifies the process of migrating databases, making it easier for organizations to move data between different database platforms and locations. DMS supports various source and target database engines, including but not limited to MySQL, PostgreSQL, Oracle, SQL Server, and Amazon RDS.
Its advantages include a managed service, low downtime, heterogeneous support, data transformation, real-time replication, and schema conversion

<img src=https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/6fc07d7c-53ee-4f8c-8617-4201dd9a0ab1">


### Why We Need Amazon DMS:

Database migration is essential for various reasons:

#### Platform Migration: 
When you need to move data from one database platform to another, such as migrating from an on-premises SQL Server to an Amazon RDS MySQL instance.

#### Version Upgrades: 
Upgrading to a newer version of a database engine often requires data migration to ensure compatibility and to take advantage of new features.

#### Cloud Adoption:
As organizations transition to the cloud, they often need to move their databases from on-premises or other cloud providers to AWS services like Amazon RDS.

#### Data Center Relocation: 
Data center migrations, including consolidations, often involve moving databases to new infrastructure.


### Advantages of Amazon DMS:

Amazon DMS offers several advantages for database migration:

#### Managed Service: 
DMS is a fully managed service, eliminating the need for complex infrastructure setup and management. AWS handles maintenance, backups, and scaling.

#### Low Downtime: 
DMS supports near-zero downtime migrations, allowing businesses to minimize disruption during the migration process.

#### Heterogeneous Support: 
DMS can migrate data between different database engines, allowing you to switch between database platforms seamlessly.

#### Data Transformation: 
DMS can transform data during the migration, making it possible to adapt data structures and schemas as needed.

#### Real-time Replication: 
DMS supports ongoing replication from a source database to a target database, ensuring that the data remains up-to-date.

#### Schema Conversion: 
DMS can automatically convert schemas from the source to the target database, making it easier to migrate without manual intervention.


### Tasks in Using Amazon DMS for Database Migration:

#### Setup Endpoints: 
Define source and target endpoints in AWS DMS console.

#### Create Replication Instance: 
Configure the replication engine with capacity and network settings.

#### Migration Task:
Specify source, target, migration type, settings, table mappings, and transformations.

#### Start Migration:
Initiate the task to copy data from source to target database.

#### Monitor and Validate:
Continuously oversee migration progress and validate data integrity in the target database.

#### Cutover and App Update:
Execute cutover to switch to the new target database and update application configurations.

#### Testing and Cleanup: 
Rigorously test the application with the new database and then decommission the source, remove the migration task, and clean up resources.




In summary, Amazon DMS is a valuable service for simplifying and automating database migration tasks, offering numerous advantages and supporting a wide range of use cases to meet the diverse needs of organizations transitioning their data between different platforms and environments.
