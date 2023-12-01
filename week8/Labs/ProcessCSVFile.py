import boto3
import csv

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb')
students_table = dynamodb.Table('Students')  # Replace 'Students' with your table name

def lambda_handler(event, context):
    # Expecting event to contain the S3 bucket and object key information
    bucket = event['bucket']
    key = event['key']
    local_filename = '/tmp/students.csv'  # Local file to download CSV

    # Download the file from S3 to the local filesystem
    try:
        s3 = boto3.client('s3')
        s3.download_file(bucket, key, local_filename)
    except Exception as e:
        print(f'Error getting object {key} from bucket {bucket}: {e}')
        raise e

    # Read the CSV file
    with open(local_filename) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        # Read each row in the file
        row_count = 0
        for row in reader:
            row_count += 1
            try:
                # Insert data into the DynamoDB table
                students_table.put_item(
                    Item={
                        'StudentId': row['StudentId'],
                        'StudentName': row['StudentName'],
                        'Email': row['Email']
                    }
                )
            except Exception as e:
                print(f"Unable to insert data into DynamoDB table: {e}")

    return f"{row_count} records inserted