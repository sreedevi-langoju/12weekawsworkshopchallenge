Lab Steps
Task 1: Sign in to AWS Management Console
Click on the open console button, and you will get redirected to AWS Console in a new browser tab.

On the AWS sign-in page,

Leave the Account ID as default. Never edit/remove the 12 digit Account ID present in the AWS Console. otherwise, you cannot proceed with the lab.

Now copy your User Name and Password in the Lab Console to the IAM Username and Password in AWS Console and click on the Sign in button.

Once Signed In to the AWS Management Console, Make the default AWS Region as US East (N. Virginia) us-east-1.

There is no Validation feature for this lab.

Task 2: Creating a Kinesis data stream
In this task , we will create a Kinesis data stream by providing the name, capacity and other configuration.

Make sure you are in the US East (N. Virginia) us-east-1 Region.

Navigate to Kinesis by clicking on the Services menu, under the Analytics section.

Under Get Started, select Kinesis Data Streams and click on Create data stream button.



Under Data stream name, enter the name whiz-data-stream.

Under Capacity mode : select Provisioned

Under Provisioned shards, enter 1.



Click on Create data stream button.



Once the data stream is created, click to open it.

Click on the Configuration tab.

Scroll down to Encryption and click on Edit.

Check Enable server-side encryption and use the default encryption key type, i.e Use AWS managed CMK.

Click on Save changes.



You have used AWS KMS to encrypt your data.



Task 3: Creating an S3 Bucket
In this task, we are going to create an S3 bucket by providing details about name, versioning and encryption.

Make sure you are in the US East (N. Virginia) us-east-1 Region.

Navigate to S3 by clicking on the Services menu, under the Storage section.

Click on Create bucket button.

In the General Configuration,

Bucket name : Enter whiz-datasource<RANDOM-NUMBER>.

Note: S3 Bucket names are globally unique, choose a name that is available.

Region: Select US East (N. Virginia) us-east-1 (i.e same region as the Kinesis data stream).

In the Bucket Versioning, Check the option Enable.

In the Default encryption,

Server-side encryption: Select Enable

Encryption key type: Leave the key type as Amazon S3-managed key (SSE-S3).

Click on Create bucket button.



Task 4: Creating producer Lambda function
Let us create 3 lambda functions. One function for the producer and the other two for consumers.

Make sure you are in the US East (N. Virginia) us-east-1 Region.

Navigate to Lambda by clicking on the Services menu, under the Compute section.

Click on the Create function button.

Choose Author from scratch

Function name: Enter producer

Runtime: Select Node.js 14.x

Under the Permissions section, click on Change default execution role and then choose use an existing role.

Existing role: Select lambda_Role_<RANDOM_NUMBER>



Click on Create function button.

Configuration Page: On this page, we need to configure our lambda function.

If you scroll down a little bit, you can see the Code source section. Here we need to write a NodeJs function which reads the file in S3 and sends the data to kinesis data stream.

Remove the existing code in AWS lambda index.js. Copy the below code and paste it into your lambda index.js file.

const AWS = require('aws-sdk');         
AWS.config.update({             
    region: 'us-east-1'                     
})                      
const s3 = new AWS.S3();                    
const kinesis = new AWS.Kinesis();                      
exports.handler = async (event) => {                
    console.log(JSON.stringify(event));                 
    const bucketName = event.Records[0].s3.bucket.name;             
    const keyName = event.Records[0].s3.object.key;             
    const params = {        
        Bucket: bucketName,             
        Key: keyName                
    }   
    await s3.getObject(params).promise().then(async (data) => {     
        const dataString = data.Body.toString();                
        const payload = {   
            data: dataString    
        }
        await sendToKinesis(payload, keyName);              
    }, error => {       
        console.error(error);                   
    })              
};                  
async function sendToKinesis(payload, partitionKey) {                   
    const params = {        
        Data: JSON.stringify(payload),              
        PartitionKey: partitionKey, 
        StreamName: 'whiz-data-stream'      
    }           
    await kinesis.putRecord(params).promise().then(response => {        
        console.log(response);      
    }, error => {       
        console.error(error);               
    })                  
}
You need to change the StreamName in the index.js file based on your Kinesis data stream name under the function sendToKinesis.



Save the function by clicking on the Deploy button.

Task 5: Creating an event notification
Navigate to S3 by clicking on the Services menu, under the Storage section.

Click on the created S3 bucket and navigate to the Properties tab.

Scroll down to Event notifications and click on Create event notification.

Under Create event notification,

Event name : Enter upload-event

Leave the prefix as it is.

Suffix : Enter .txt

Under Event types, select All object create events.

Under Destination, select Lambda function.

Under Specify Lambda function, select Choose from your Lambda functions and choose the producer from the list and click on Save changes button.



That means whenever an object is created, producer lambda function is triggered.



Task 6: Creating consumer Lambda functions
Let us create lambda functions for consumers.

Make sure you are in the US East (N. Virginia) us-east-1 Region.

Navigate to Lambda by clicking on the Services menu, under the Compute section.

Consumer -1
Click on the Create function button.

Choose Author from scratch

Function name: Enter consumer1

Runtime: Select Node.js 14.x

Under the Permissions section, click on Change default execution role and then choose Use an existing role.

Existing role: Select lambda_Role_<RANDOM_NUMBER>

Click on Create function button.

Configuration Page: On this page, we need to configure our lambda function.

If you scroll down a little bit, you can see the Code source section. Here we need to write a NodeJs function which reads the file in the data stream and processes the data, here we are logging out the data.

Remove the existing code in AWS lambda index.js. Copy the below code and paste it into your lambda index.js file. Save the function by clicking on the Deploy button.

exports.handler = async (event) => {
console.log(JSON.stringify(event));
for (const record of event.Records) {
const data = JSON.parse(Buffer.from(record.kinesis.data, 'base64'));
console.log('consumer #1', data);
}
};
On the same page, go to Configuration tab and click on Triggers

Under Triggers,  Kinesis trigger will be in a Disabled state, select the trigger and click on Edit button.(If trigger is not present , Move to Step 11)

Check the Activate trigger and click on the Save button

Now you can see the Kinesis: whiz-data-stream (Enabled).

In case the trigger is not present already , click on Add Trigger button.

Select a source dropdown: Select Kinesis
Kinesis stream : Select whiz-data-stream
Check the Activate trigger checkbox.
Click on Add button.

Consumer - 2
Click on the Create function button.

Choose Author from scratch

Function name: Enter consumer2

Runtime: Select Node.js 14.x

Under the Permissions section, click on Change default execution role and then choose use an existing role.

Existing role: Select lambda_Role_<RANDOM_NUMBER>

Click on Create function button.

Configuration Page: On this page, we need to configure our lambda function.

If you scroll down a little bit, you can see the Code source section. Here we need to write a NodeJs function which reads the file in the data stream and processes the data, here we are logging out the data.

Remove the existing code in AWS lambda index.js. Copy the below code and paste it into your lambda index.js file. 

exports.handler = async (event) => {
console.log(JSON.stringify(event));
for (const record of event.Records) {
const data = JSON.parse(Buffer.from(record.kinesis.data, 'base64'));
console.log('consumer #2', data);
}
};
Save the function by clicking on the Deploy button.

On the same page, go to Configuration tab and click on Triggers

Under Triggers,  Kinesis trigger will be in Disabled state select the trigger and click on Edit button,( If trigger is not present, move to Step 21.)

Check the Activate trigger and click on save button

Now you can see the Kinesis: whiz-data-stream (Enabled).

In case the trigger is not present already , click on Add Trigger button.

Select a source dropdown: Select Kinesis
Kinesis stream : Select whiz-data-stream
Check the Activate trigger checkbox.
Click on Add button.

Task 7: Creating and uploading a test file to S3 bucket
Open any text editor on your computer.

Copy and paste the following data and save the file in txt, in my case test.txt

Hello
This is Whizlabs...
Check out our courses
Bye bye!!!
Navigate to S3 by clicking on the Services menu, under the Storage section.

Click on the bucket we created earlier.

Under the Objects tab, click on Upload.

In the Files and folders, click Add files.

Navigate and select the test.txt file created earlier in the task.



Once you select the file, click on Upload button.

Now, click Close to close the Upload: status page.

Task 8: Testing the configuration
Now, we have uploaded the file to the S3 bucket. Since we have configured the event notification, the producer lambda function should get triggered.

Let us test the configuration by checking the logs of lambda functions.

Make sure you are in the US East (N. Virginia) us-east-1 Region.

Navigate to CloudWatch by clicking on the Services menu, under the Management & Governance section.

On the left panel, click on Logs and select Log groups.

 Here you can see all 3 functions logs.



Producer
In the filter log groups, search for the producer.



Click and open the log group.

In the Log streams, you will find the latest event, in our case we’ll have only 1 log event.

Click and open the log stream. This means our lambda function is triggered successfully.



Click and expand the event. We can see the event that triggers the lambda function from our S3 bucket.



Then the lambda function sends the data to Kinesis and returns a successful message.



In the producer lambda function, we can see that the S3 is configured as a trigger for the producer lambda function.



Consumer 1
Now return to the log groups main menu.

In the filter log groups, search for the consumer1.



Click and open the log group.

In the Log streams, you will find the latest event, in our case we’ll have only 1 log event.

Click and open the log stream. This means the lambda function got executed.



We can see the event object from the Kinesis.



We can see from the event that the data is encrypted and encoded.

Our lambda function has extracted the data and read it out.



Consumer 2
Now return to the log groups main menu.

In the filter log groups, search for the consumer2.



Click and open the log group.

In the Log streams, you will find the latest event, in our case we’ll have only 1 log event.

Click and open the log stream. This means the lambda function got executed.



We can see the event object from the Kinesis.



We can see from the event that the data is encrypted and encoded.

Our lambda function has extracted the data and read it out.



Do you know?
This feature of Amazon Kinesis Data Streams is particularly beneficial for use cases that require real-time analytics, real-time monitoring, or building event-driven architectures where multiple applications or services need to consume the same data stream concurrently.

Task 9: Validation of the Lab
Once the lab steps are completed, please click on the Validation button on the left side panel.

This will validate the resources in the AWS account and displays whether you have completed this lab successfully or not.

Sample Output:



Task 10: Delete AWS Resources
Deleting Kinesis Data Streams
Make sure you are in the US East (N.Virginia) us-east-1 Region.

Navigate to Kinesis by clicking on the Services menu, under the Analytics section.

On the left panel, click on the Data streams.

Select the created data stream and click on the Actions button.

Select Delete from the drop-down.

Confirm by typing Delete and click Delete. 

Completion and Conclusion
You have created an IAM Role for the Lambda functions.

You have created a S3 Bucket and created an event notification.

You have created lambda functions for a producer and two consumers.

You have added the triggers for the consumer lambda functions.

You have uploaded a text file to the S3 bucket.

You have tested the configuration by checking the cloudwatch logs of all the 3 lambda functions.

End Lab
Sign out of the AWS Account.

You have successfully completed the lab.

Once you have completed the steps, click on End Lab from your whizlabs lab console and wait till the process gets completed.
