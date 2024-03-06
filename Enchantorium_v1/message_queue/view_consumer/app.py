import boto3
from boto3.dynamodb.conditions import Key
from os import getenv
from uuid import uuid4
import json

sqs = boto3.resource('sqs')
region_name = getenv('APP_REGION')
enchantorium_creatures = boto3.resource('dynamodb', region_name=region_name ).Table('Enchantorium_Views')

def lambda_handler(event, context):
    for record in event['Records']:
        body = json.loads(record['body'])
        newID = str(uuid4())
        userID = event["userID"]
        productID = event["productID"]
        enchantorium_creatures.put_item(Item ={
            "ID": newID,
            "userID": userID,
            "productID": productID
        })
        print(f"Received message: {body}")
        # Add your processing logic here
    return {
            'statusCode': 200,
            'headers': {
                "Access-Control-Allow-Headers" : "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Origin": "*", 
                "Access-Control-Allow-Methods": "GET,POST,DELETE,PUT,OPTIONS",
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
    }