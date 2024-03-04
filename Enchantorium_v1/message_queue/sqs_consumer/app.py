import json

def lambda_handler(event, context):
    for message in event["Records"]:
        process_message(message)

def process_message(message):
    try:
        print(f"Payment for item:{message['body']} has been accepted")
        return(f"Payment for item:{message['body']} has been accepted")
        #do stuff with it
    except Exception as err:
        print("ow")
        raise err
        
