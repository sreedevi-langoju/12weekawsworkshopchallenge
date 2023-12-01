import boto3
import json
import os

def lambda_handler(event, context):
    s3_bucket = event['Records'][0]['s3']['bucket']['name']
    s3_key = event['Records'][0]['s3']['object']['key']
    
    # Extract file extension
    file_extension = os.path.splitext(s3_key)[-1].lower()  # Extracts the file extension

    # Prepare input data for the Step Function
    input_data = {
        "bucket": s3_bucket,
        "key": s3_key,
        "file_extension": file_extension  # Include the file extension in the input data
    }

    # Start Step Function execution
    step_function_arn = 'StepFunction_ARN' # add your step function ARN here
    client = boto3.client('stepfunctions')

    try:
        response = client.start_execution(
            stateMachineArn=step_function_arn,
            input=json.dumps(input_data)
        )
        print("Step Function execution started:", response)
        return {
            'statusCode': 200,
            'body': json.dumps('Step Function execution started successfully')
        }
    except Exception as e:
        print("Error starting Step Function execution:", e)
        return {
            'statusCode': 500,
            'body': json.dumps('Error starting Step Function execution')
        }