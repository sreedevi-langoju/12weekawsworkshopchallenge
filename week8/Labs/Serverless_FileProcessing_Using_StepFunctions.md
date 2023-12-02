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

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/9059eedf-35e3-431d-9cdf-dd815cc669df" height=600 width=600 >


Click on Add Trigger to add the s3 trigger to this lamda function and choose the s3 bucked you created earlier.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/aa61ce6b-9fc2-42e4-8463-1c5ec7f49652"  height=600 width=600 >

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/eefefb6e-6e83-4087-b851-6363c80ab916"  height=600 width=600 >


### b. ProcessCSVFile Lambda:

Lambda function to process CSV files, extract data, and store it in DynamoDB.
Function Name: ProcessCSVFile.
Runtime:Python 3.9.
Choose Existing role: Choose IAM role created earlier.
In General Configuration change the Time out: 3 min 0 sec.
Remove the existing code in Lambda and Copy the python code from ProcessCSVFile.py( find this file in Labs folder in this repository) and click on Deploy button.
Replace the correct Dynamodb table name in the code.
Copy the ARN of the lambda function.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/f398889a-1fde-4af6-b7e0-5608bbe53f23"  height=600 width=600 >

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/31b4eac1-2502-4dee-887c-0633e21a5d85"  height=600 width=600 >


### c. ProcessImageFile Lambda:

Lambda function to process image files using Rekognition, extract labels, and store them in DynamoDB.
Function Name: ProcessImageFile.
Runtime:Python 3.9.
Choose Existing role: Choose IAM role created earlier.
In General Configuration change the Time out: 3 min 0 sec.
Remove the existing code in Lambda and Copy the python code from ProcessImageFile.py( find this file in Labs folder in this repository) and click on Deploy button.
Replace the correct Dynamodb table name in the code.
Copy the ARN of the lambda function.


<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/71c22095-cdfa-45f5-8c9a-2e1f5220acec"  height=600 width=600 >

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/78a03114-2779-4304-87bf-e236831ce654"  height=600 width=600 >


## Step 6: AWS Step Functions - Create State Machine:

Go to the AWS Step Functions Console.
Click "Create state machine".
Copy the code from statemachinecode.json  into the {} code section and add the ARN of the lambda functions created earlier and ARN of the sns topic  accordingly. 
Design automatically display on the right side.
Click on the config tab and give name the State machine,Type:Standard and choose Create new Role.
 

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/c65e42cf-1fd8-42e9-a870-4435f393b751"  height=600 width=600 >

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/1a462821-bc3e-4255-9b02-67481d5a220d"  height=600 width=600 >

Copy the ARN of the State machine and add that in TriggerStepFunction.py code file.


## Step 7: Test Workflow:

### a. Upload Test Files:
Upload test files (CSV, image) to the configured S3 bucket.

#### 1. First upload csv (ex: students.csv find in the Labs reposiroty folder here) file to s3 bucket created earlier.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/41e29a3b-cc36-4778-a4c5-9d4f920e2f22">

Check the StepFunction console and chekc the status of the state machine created earlier.If it is succeeded, click on that link.You will see the success path.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/eb0739e9-66d1-4741-9ecb-065741ba2c9a">


Now check the DynamoDB Students table - Explore table items - It will display the csv row data that you have uploaded.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/333a1928-3e40-4c01-b8c1-da25b2ca0f8e">

Now check your email subscribed to the Notification. You will recieve the sucess notitification.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/6c12d8c9-7faf-4099-8cb7-cffbd9a329a7" height=300 width=400 >


#### 2. Upload any image(.jpeg or .jpg or .png) file (ex: city.jpg find in the Labs reposiroty folder here) file to s3 bucket created earlier.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/18dd1664-7c21-4c29-b2c4-01f5b378011f">

Check the StepFunction console and chekc the status of the state machine created earlier.If it is succeeded, click on that link.You will see the success path.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/b292fb6d-de4c-4f48-ad1c-fe0e11b840ef">

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/8b39a8f5-6075-482b-9f7d-b8e78a99cb09">

Now check the DynamoDB Images table - Explore table items - It will display the labels generated for image you have uploaded.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/f0f0fae7-242f-49ac-8c08-39f099246585">

Now check your email subscribed to the Notification. You will recieve the sucess notitification.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/f98ef9c9-4a84-48d5-9016-aae9bf0b4805" height=300 width=400>


#### 3. Upload any file other than image(.jpeg or .jpg or .png) file or csv file  (ex: city.pdf find in the Labs reposiroty folder here) file to s3 bucket created earlier.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/ff155add-d667-4dda-9747-3f69d0ebb0f1">

Check the StepFunction console and chekc the status of the state machine created earlier.If it is succeeded, click on that link.You will see the not success path.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/f90c6a96-8f4a-479b-839f-233925be173a">


Now check your email subscribed to the Notification. You will recieve the File type not support email  notitification.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/20b3b994-5eac-42a8-be50-4a3ee0798161" height=300 width=400>

### b. Monitor Execution:
Monitor executions in AWS Step Functions.
Check DynamoDB tables for stored data.
Monitor SNS for success/failure notifications.
Ensure that all resources (Lambda, Step Functions, S3, DynamoDB, SNS) have proper permissions and configurations set up. This sequence outlines a structured approach to setting up the workflow and testing its functionality. Adjustments and validations are essential to ensure the workflow functions as expected.

## Step 8: Cleanup Resources:

Delete all the resources created earlier to avoid unnecessary billing.

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/4f9d219e-eb1e-48ac-b422-4631ce66aae6">

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/1aef3844-d87f-42e2-9dc0-8b4ab49534f9">

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/8163d50b-6139-4bff-975e-e28750da333f">

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/27221687-7777-40eb-9aab-58f72f5f1f2b">

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/8df33289-4407-4213-bf20-b8c602859451">

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/93a5a625-7c8c-42c2-9044-96577b07b32f">



