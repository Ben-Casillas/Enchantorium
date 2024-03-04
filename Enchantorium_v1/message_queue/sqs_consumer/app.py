import json

def lambda_handler(event, context):
    for message in event["Records"]:
        process_message(message)

def process_message(message):
    try:
        print(f"Here is the message body {message['body']}")
        #do stuff with it
    except Exception as err:
        print("ow")
        raise err
        
