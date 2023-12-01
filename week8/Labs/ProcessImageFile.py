import boto3

rekognition = boto3.client('rekognition')
dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    bucket_name = event['bucket']
    object_key = event['key']

    rekognition_params = {
        'Image': {
            'S3Object': {
                'Bucket': bucket_name,
                'Name': object_key
            }
        }
    }

    try:
        rekognition_response = rekognition.detect_labels(**rekognition_params)
        labels = [label['Name'] for label in rekognition_response['Labels']]

        dynamo_params = {
            'TableName': 'Images', # your dynamodbtable
            'Item': {
                'ImageId': {'S': object_key},
                'Labels': {'SS': labels}
            }
        }

        dynamodb.put_item(**dynamo_params)

        return {
            'statusCode': 200,
            'body': 'Labels processed and saved to DynamoDB'
        }
    except Exception as e:
        print('Error:', e)
        return {
            'statusCode': 500,
            'body': 'Error processing image and saving to DynamoDB'
        }
