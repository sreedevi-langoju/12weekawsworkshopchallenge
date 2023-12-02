# Serverless File Processing workflow with Step Functions, Lambda, Rekognition, SNS, and S3 Trigger

Here's a step-by-step guide on how to implement the Lambda-Initiated Step Functions Orchestrating CSV and Image  file Processing with S3 Triggers and SNS Notifications using the AWS Management Console:

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/2467e325-e5ec-4206-98bf-ad7db0e7cfe3">

## Step1 : IAM Roles and Permissions - IAM Role for Lambda Execution:

Create an IAM role for Lambda functions with policies granting access to necessary services (S3, DynamoDB, Rekognition, SNS).

Role Name: Give any name
Trusted Entity: AWS Service
USecase: Lambda
Policies: Select these .
Attach Inline Policy:


<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/9b1f5649-a782-4e83-a84e-4ae6d8081605">

## Step 2: Create S3 Bucket:
Create an S3 bucket where files will be uploaded.
Bucket Name: Unique Name
AWS Region:us-east-1
All other options default



<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/d5882ee9-1de4-4761-8445-16adc0c2f094">
Enable event notifications for object creation to trigger Lambda.
3. DynamoDB:
a. Create DynamoDB Table:
Create a DynamoDB table with the necessary attributes to store processed data.
4. SNS Topic:
a. Create SNS Topic:
Create an SNS topic for sending notifications.
5. Lambda Functions:
a. TriggerStepFunction Lambda:
Create a Lambda function triggered by S3 bucket events.
The function should start the Step Functions execution using the start_execution API.
b. ProcessCSVFile Lambda:
Lambda function to process CSV files, extract data, and store it in DynamoDB.
Ensure it handles success/failure and sends appropriate SNS notifications.
c. ProcessImageFile Lambda:
Lambda function to process image files using Rekognition, extract labels, and store them in DynamoDB.
Similar to ProcessCSVFile, handle success/failure and send SNS notifications.
d. SendNotification Lambda:
Lambda function to send SNS notifications for success/failure events.
6. AWS Step Functions:
a. Create State Machine:
Define a state machine using AWS Step Functions with:
State to check file type (CSV or image).
States to invoke ProcessCSVFile and ProcessImageFile Lambda functions based on file type.
States for sending SNS notifications.
Handle success and failure paths.
7. Test Workflow:
a. Upload Test Files:
Upload test files (CSV, image) to the configured S3 bucket.
b. Monitor Execution:
Monitor executions in AWS Step Functions.
Check DynamoDB tables for stored data.
Monitor SNS for success/failure notifications.
Ensure that all resources (Lambda, Step Functions, S3, DynamoDB, SNS) have proper permissions and configurations set up. This sequence outlines a structured approach to setting up the workflow and testing its functionality. Adjustments and validations are essential to ensure the workflow functions as expected.
