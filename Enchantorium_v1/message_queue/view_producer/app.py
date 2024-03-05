import boto3
import json

sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName='ViewQueue')

def lambda_handler(event, context):
    if "body" in event and event["body"] is not None:
        event = json.loads(event["body"])
        userID = event["userID"]
        productID = event["productID"]
        message = {'user': userID, 'item': productID}
        response = queue.send_message(MessageBody=json.dumps(message))
        print(response)
        return {
            'statusCode': 200,
            'body': json.dumps('Message sent successfully!')
        }
    return {
        'statusCode': 401,
        'body': json.dumps('Error in data.')
    }