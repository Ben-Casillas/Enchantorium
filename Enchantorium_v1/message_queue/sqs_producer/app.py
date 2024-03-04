import boto3
import json

def lambda_handler(event, context):
    # Initialize SQS client
    sqs = boto3.client('sqs')
    
    # Get the SQS queue URL from the event
    queue_url = 'https://sqs.us-east-2.amazonaws.com/254884408525/MailingQueue'
    
    # Example message
    message = {
        'message': 'Hello from Lambda!'
    }
    
    # Send message to SQS
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(message)
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Message sent to SQS successfully')
    }
