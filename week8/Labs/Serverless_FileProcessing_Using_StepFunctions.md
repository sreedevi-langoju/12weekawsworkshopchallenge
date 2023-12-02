# Serverless File Processing workflow with Step Functions, Lambda, Rekognition, SNS, and S3 Trigger

Here's a step-by-step guide on how to implement the Lambda-Initiated Step Functions Orchestrating CSV and Image  file Processing with S3 Triggers and SNS Notifications using the AWS Management Console:

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/2467e325-e5ec-4206-98bf-ad7db0e7cfe3">

## Step1 : IAM Roles and Permissions - IAM Role for Lambda Execution:

Create an IAM role for Lambda functions with policies granting access to necessary services (S3, DynamoDB, Rekognition, SNS).

Go to AWS IAM Console.
Select "Roles" and click "Create role".
For "Select type of trusted entity", choose "AWS service", then pick "Lambda" in the "Choose a use case" section.
Attach policies granting full access to S3, DynamoDB, Step Functions, Rekognition, and SNS.
Review and create the role.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/9b1f5649-a782-4e83-a84e-4ae6d8081605">

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/3f8d0e80-344b-4048-8958-a281c7b0bb0e">

## Step 2: Create S3 Bucket:

Create an S3 bucket where files will be uploaded.

Go to the AWS S3 Console.
Click on "Create bucket".
Enter a unique bucket name and select the AWS region as us-east-1.
Keep other options as default and create the bucket.
<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/d5882ee9-1de4-4761-8445-16adc0c2f094">


## Step3 :Create DynamoDB tables:

Go to the AWS DynamoDB Console.
Click "Create table".
Create two tables: "Students" and "Images" with the specified partition keys.
Keep other settings as default and create the tables.

Table 1:  Table Name :Students 
          Partition key:StudentId
          All other options default

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/d6278645-f43a-4d30-932a-ded4b4794be0" height=500 width=400>


Table 2:  Table Name :Images 
          Partition key:ImageKey
          All other options default

          
<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/4d7d84c0-e4d1-46d9-b82b-621e7c8e82cb" height=500 width=400>


## Step 4: Create SNS Topic:

Create an SNS topic for sending notifications.

Go to the AWS SNS Console.
Click "Create topic".
Enter a topic name and create the topic.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/4e25cdf0-212b-4281-878e-b1203427f347">


After creating the topic, select the newly created topic from the list.
Click on "Create subscription".
Choose the protocol for the endpoint to receive notifications (e.g., Email, SMS, HTTPS, Lambda, etc.).
Enter the necessary details based on the chosen protocol.
Confirm the subscription.(Check your email to confirm subscription for Email protocol)

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/b1396d1a-174b-4c96-9f00-b8a8231b0ddc">

## Step 5: Create Lambda Functions:

Go to the AWS Lambda Console.
Create four Lambda functions: TriggerStepFunction, ProcessCSVFile and ProcessImageFile.
Configure these functions according to their specific roles in your workflow.
Ensure TriggerStepFunction Lambda is triggered by S3 bucket events.

### a. TriggerStepFunction Lambda:

Create a Lambda function triggered by S3 bucket events.
Function Name: TriggerStepFunction
Runtime:Python 3.9
Choose Existing role: Choose IAM role created earlier
In General Configuration change the Time out: 3 min 0 sec
Remove the existing code in Lambda and Copy the python code from TriggerStepFunction.py( find this file in Labs folder in this repository)

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/abcab2f5-0578-4b88-bbdb-d16973c13192">

Click on Add Trigger to add the s3 trigger to this lamda function.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/6c45446b-841d-4080-9e84-c956a00f49ab">

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/73ecd337-4299-4057-a646-03ff5bb31543">

### b. ProcessCSVFile Lambda:

Lambda function to process CSV files, extract data, and store it in DynamoDB.
Function Name: ProcessCSVFile
Runtime:Python 3.9
Choose Existing role: Choose IAM role created earlier
In General Configuration change the Time out: 3 min 0 sec
Remove the existing code in Lambda and Copy the python code from ProcessCSVFile.py( find this file in Labs folder in this repository)

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/f52060ae-2d91-4478-8d03-bc029166f496">

### c. ProcessImageFile Lambda:

Lambda function to process image files using Rekognition, extract labels, and store them in DynamoDB.
Function Name: ProcessImageFile
Runtime:Python 3.9
Choose Existing role: Choose IAM role created earlier
In General Configuration change the Time out: 3 min 0 sec
Remove the existing code in Lambda and Copy the python code from ProcessImageFile.py( find this file in Labs folder in this repository)

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/d1e8740d-9eea-4e90-90eb-c8ce54376392">

## Step 6: AWS Step Functions:

a. Create State Machine:
Define a state machine using AWS Step Functions with:
State to check file type (CSV or image).
States to invoke ProcessCSVFile and ProcessImageFile Lambda functions based on file type.
States for sending SNS notifications.
Handle success and failure paths.




## Step 7: Test Workflow:
a. Upload Test Files:
Upload test files (CSV, image) to the configured S3 bucket.
b. Monitor Execution:
Monitor executions in AWS Step Functions.
Check DynamoDB tables for stored data.
Monitor SNS for success/failure notifications.
Ensure that all resources (Lambda, Step Functions, S3, DynamoDB, SNS) have proper permissions and configurations set up. This sequence outlines a structured approach to setting up the workflow and testing its functionality. Adjustments and validations are essential to ensure the workflow functions as expected.
