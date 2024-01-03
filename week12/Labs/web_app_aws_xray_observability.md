# Create a sample Web Application and monitor it in AWS X-Ray:

Let me walks you through the steps to deploy the sample web application using CloudFormation and monitor it using AWS X-Ray.

## Architecture Diagram:

<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/b1237be4-e2c2-4a78-b822-d18a21fd8b67" width=400 height=400>


<img src="https://github.com/sreedevi-langoju/12weekawsworkshopchallenge-/assets/135724041/cfd9f0ca-8730-4c88-9902-854dbd41ef7e" width=400 height=400>


## Task 1: Sign in to AWS Management Console
Click on the Open Console button, and you will get redirected to AWS Console in a new browser tab.

Once Signed In to the AWS Management Console, Make the default AWS Region as US East (N. Virginia) us-east-1.

## Task 2: Create an S3 bucket

In this task, we are going to create an S3 bucket by providing the required configurations and uploading the zip file as an object. 

Make sure you are in the US East (N. Virginia) us-east-1 Region.

Navigate to the Services menu at the top. Click on S3 in the Storage section.

On the S3 Page, click on Create bucket button and fill in the bucket details.

Bucket name: Enter mys3bucket<Random_Numbers>

Note: S3 bucket name is globally unique, choose a name which is available.

Region: Select US East (N. Virginia) us-east-1

    4. Leave other settings as default. 

    5. Click on Create bucket button.

    6. Click on the bucket name you created.

    7. Download this aws-xray-node-sample-app.zip file and save it on your local machine.

    8. To upload this zip file to our S3 bucket,

Click on Upload button.

Click on Add files button.

Select the zip file. 

Click on the Upload button.

You can watch the progress of the upload from within the transfer panel at the top of the screen.

Once your file has been uploaded, it will be displayed in the bucket.

Copy the Bucket name and Object name for later use.
         

## Task 3: Deploy a sample X-Ray application using CloudFormation

Navigate to CloudFormation by clicking on Services, and click on CloudFormation under the Management and Governance section.

Before creating CloudFormation Stack, download this template and save it on your local machine.

The CloudFormation template will create below resources:

Elastic Beanstalk application: host sample X-Ray application.

IAM Role: used by the EC2 in Elastic Beanstalk.

DynamoDB: store signup details.

S3 bucket: store the template.

SQS and SQS: decouple the application.


On the CloudFormation dashboard, click on Create stack button.

Prepare Template: Select Template is ready

Specify template: Select Upload a template file

Click on Choose file and choose the xray-cf.yml from your local machine

Click on the Next button.
       

On the Specify stack details page, provide the following details:

Stack Name: Enter a name of your choice.
NodejsPlatformVersion: Enter latest version of Amazon Linux 2 Node.js 18 (Use this link to get the latest version) 


S3BucketName : Enter S3 Bucket Name

S3ObjectKey : Enter Object Name

Subnet: Select any subnet from the dropdown (any default subnet)

VPC: Select the default VPC from the dropdown

Click on the Next button.

 

On the Configure Stack options page, leave it as default and click on Next button in the bottom right corner.

Review the Stack, Check the acknowledgment at the bottom of the page, and then click on Submit button.

Once you click on Create Stack, your stack (xray-cf.yml) will start deploying the sample application. 

Initially, the stack status will be CREATE_IN_PROGRESS and it will create all the resources.

Wait for 10 minutes till the stack status changes to CREATE_COMPLETE.

Note: It will create an additional nested stack.



## Task 4: Test the Application
Go to EC2 Console by searching EC2 in the Services, and click on the Instances from the left side.

Select the whizlabs-xray-stack instance and Copy the Elastic IP Address  ( it will be the application Public IPv4 that you will use to access the application).

Open the IP in the new tab. It will open the sample X-ray application.

Let’s generate some traffic by signing up for the application.

For this step, you can manually signup into the application. But you will automate the process by clicking on the Start button.

Wait for a few minutes and then click on the Stop button.



     7. Hence, you have successfully created a few signup accounts in the sample application.

     8. To view the signup details, navigate to DynamoDB by clicking on the Services menu at the top and search for DynamoDB in the search bar.

     9. Click on the Explore table items button from the left navigation panel and Select the table created. 

    10. You can view the signup details.



## Task 5: Monitor the traffic in AWS X-Ray
Go to the CloudWatch by clicking the Services menu at the top and search for CloudWatch in the search bar.

Now click on Service Map from left navigation menu under the X-Ray traces.

In the service map, you will get insight into the traffic that flows through our application.



Note: If you got a warning as Data not found, then click on 5 minutes at the top right corner and select 1 hour.



Now click on any of the components to view the response distribution.

It will show the traffic response status along with the graph.



Click on the Analyze Traces to view detailed information.



It will show detailed information about HTTP Method, URL, User-Agent, HTTP Method, Trace List, etc.

You can click on any of the Trace List to view the traces.

You can also filter the traces by clicking on Question mark(?) at the top right corner.

Task 6 : Validation of the Lab
Once the lab steps are completed, please click on the Validation button on the left side panel.

This will validate the resources in the AWS account and displays whether you have completed this lab successfully or not.

Sample output :



Task 7: Clean up AWS Resources
Delete CloudFormation Stack
Make sure you are in the N.Virginia Region.

Navigate to CloudFormation by clicking on the Services menu at the top and search for CloudFormation in the search bar.

Select the whizlabs-xray-stack stack and click on the Delete button.

Now click on the Delete stack button in the prompt.

Now, wait till your stack deletion is completed. It will also delete the nested stack.

Completion and Conclusion
You have successfully navigated to the X-Ray application.

You have successfully deployed a sample X-ray application.

You have successfully tested the application.

You have successfully monitored the traffic in X-Ray.

You have successfully completed the validation test.

You have successfully deleted the AWS Resources.
