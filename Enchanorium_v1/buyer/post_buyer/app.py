import boto3
from boto3.dynamodb.conditions import Key
from os import getenv
from uuid import uuid4
import json

#DONE
region_name = getenv('APP_REGION')
enchantorium_buyer = boto3.resource('dynamodb', region_name=region_name ).Table('Enchantorium_Buyers')

def lambda_handler(event, context):
    if("parhParameters" in event):
        path = event["pathParameters"]
        buyer_id = str(uuid64())

        username = event["username"]
        password = event["password"]
        email = event["email"]
        #primary address
        #maybe card info
        



def response(code, body):
    return {
        "statusCode": code,
        "headers": {
            "Content-Type": "application/json"
            },
        "body": json.dumps(body),
        "isBase64Encoded": False
    }