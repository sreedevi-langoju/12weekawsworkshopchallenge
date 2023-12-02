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

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/7f0807bc-ae0e-49ad-a8ca-5d0ff0b51d28">


## Step 2: Create S3 Bucket:

Create an S3 bucket where files will be uploaded.

Go to the AWS S3 Console.
Click on "Create bucket".
Enter a unique bucket name and select the AWS region as us-east-1.
Keep other options as default and create the bucket.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/081bae5d-c29c-4216-a681-c2cbafed7f6c">


## Step3: Create DynamoDB tables:

Go to the AWS DynamoDB Console.
Click "Create table".
Create two tables: "Students" and "Images" with the specified partition keys.
Keep other settings as default and create the tables.

Table 1:  Table Name :Students 
          Partition key:StudentId
          All other options default

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/0007685a-b26d-4db9-8303-3aa6f8e74058" height=500 width=400>


Table 2:  Table Name :Images 
          Partition key:ImageKey
          All other options default

          
<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/9a1421d8-c81e-4403-bc55-779471c663b3" height=500 width=400>


<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/8f79f789-a39a-40f3-bf2c-2bee34a165f2">

## Step 4: Create SNS Topic:

Create an SNS topic for sending notifications.

Go to the AWS SNS Console.
Click "Create topic".
Choose: Standard type and Enter a topic name and create the topic.
Copy ARN of the SNS topic created.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/aefc6413-720d-448b-9673-8c96fd7257b1">


After creating the topic, select the newly created topic from the list.
Click on "Create subscription".
Choose the protocol for the endpoint to receive notifications (e.g., Email, SMS, HTTPS, Lambda, etc.).
Enter the necessary details based on the chosen protocol.
Confirm the subscription.(Check your email to confirm subscription for Email protocol)

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/beb6c3e0-27ec-4bfe-ae65-62a3e141b854">

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
Remove the existing code in Lambda and Copy the python code from TriggerStepFunction.py( find this file in Labs folder in this repository) and click on Deploy button.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/abcab2f5-0578-4b88-bbdb-d16973c13192">


Click on Add Trigger to add the s3 trigger to this lamda function and choose the s3 bucked you created earlier.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/6c45446b-841d-4080-9e84-c956a00f49ab">

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/73ecd337-4299-4057-a646-03ff5bb31543">

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/12b43b26-9cb3-473b-9964-e6068ed7b0cf">



### b. ProcessCSVFile Lambda:

Lambda function to process CSV files, extract data, and store it in DynamoDB.
Function Name: ProcessCSVFile.
Runtime:Python 3.9.
Choose Existing role: Choose IAM role created earlier.
In General Configuration change the Time out: 3 min 0 sec.
Remove the existing code in Lambda and Copy the python code from ProcessCSVFile.py( find this file in Labs folder in this repository) and click on Deploy button.
Replace the correct Dynamodb table name in the code.
Copy the ARN of the lambda function.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/f52060ae-2d91-4478-8d03-bc029166f496">


### c. ProcessImageFile Lambda:

Lambda function to process image files using Rekognition, extract labels, and store them in DynamoDB.
Function Name: ProcessImageFile.
Runtime:Python 3.9.
Choose Existing role: Choose IAM role created earlier.
In General Configuration change the Time out: 3 min 0 sec.
Remove the existing code in Lambda and Copy the python code from ProcessImageFile.py( find this file in Labs folder in this repository) and click on Deploy button.
Replace the correct Dynamodb table name in the code.
Copy the ARN of the lambda function
.
<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/d1e8740d-9eea-4e90-90eb-c8ce54376392">



## Step 6: AWS Step Functions - Create State Machine:

Go to the AWS Step Functions Console.
Click "Create state machine".
Copy the code from statemachinecode.json  into the {} code section and add the ARN of the lambda functions created earlier and ARN of the sns topic  accordingly. 
Design automatically display on the right side.
Click on the config tab and give name the State machine,Type:Standard and choose Create new Role.
 

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/4fd9b589-6d1e-40e3-8e4a-58fc6cc28d1b">

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/ed9d75c7-8fc9-439d-a245-1bbd7d140d8b">

Copy the ARN of the State machine and add that in TriggerStepFunction.py code file.


## Step 7: Test Workflow:

### a. Upload Test Files:
Upload test files (CSV, image) to the configured S3 bucket.

First upload csv (ex: students.csv find in the Labs reposiroty folder here) file to s3 bucket created earlier.

<img src=https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/eb43fbf9-fbe5-4072-ac0e-1eadda61be47">

b. Monitor Execution:
Monitor executions in AWS Step Functions.
Check DynamoDB tables for stored data.
Monitor SNS for success/failure notifications.
Ensure that all resources (Lambda, Step Functions, S3, DynamoDB, SNS) have proper permissions and configurations set up. This sequence outlines a structured approach to setting up the workflow and testing its functionality. Adjustments and validations are essential to ensure the workflow functions as expected.
