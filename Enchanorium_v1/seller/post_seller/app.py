import boto3
from boto3.dynamodb.conditions import Key
from os import getenv
from uuid import uuid4
import json

#DONE
region_name = getenv('APP_REGION')
enchantorium_seller = boto3.resource('dynamodb', region_name=region_name ).Table('Enchantorium_Sellers')

def lambda_handler(event, context):
    if("parhParameters" in event):
        path = event["pathParameters"]
        seller_id = str(uuid64())

        username = event["username"]
        password = event["password"]
        email = event["email"]
        



def response(code, body):
    return {
        "statusCode": code,
        "headers": {
            "Content-Type": "application/json"
            },
        "body": json.dumps(body),
        "isBase64Encoded": False
    }