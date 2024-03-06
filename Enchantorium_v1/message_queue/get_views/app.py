import boto3
from boto3.dynamodb.conditions import Key
from os import getenv
from uuid import uuid4
import json

#WORKING
region_name = getenv('APP_REGION')
enchantorium_views = boto3.resource('dynamodb', region_name=region_name ).Table('Enchantorium_Views')

def lambda_handler(event, context):
    if ( ("pathParameters" in event) ):
        path = event["pathParameters"]
        if path is not None and "ID" in path:
            id = path["ID"]
            output = enchantorium_views.get_item(Key={"productID":id})['Item']['count']
            return response(200, output)
    return response(401, "Missing pathID.")


def response(code, body):
    return {
            'statusCode': code,
            'headers': {
                "Access-Control-Allow-Headers" : "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Origin": "*", 
                "Access-Control-Allow-Methods": "GET,POST,DELETE,PUT,OPTIONS",
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
    }