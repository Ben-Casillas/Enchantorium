import boto3
from boto3.dynamodb.conditions import Key
from os import getenv
from uuid import uuid4
import json

#WORKING
region_name = getenv('APP_REGION')
enchantorium_users = boto3.resource('dynamodb', region_name=region_name ).Table('Enchantorium_Users')

def lambda_handler(event, context):
    if ( ("pathParameters" in event) ):
        path = event["pathParameters"]
        if path is None or "ID" not in path:
            return response(200, enchantorium_users.scan()["Items"])
        if path is not None and "ID" in path:
            id = path["ID"]
            output = enchantorium_users.get_item(Key={"ID":id})["Item"]
            return response(200, output)
    return response(200, enchantorium_users.scan()["Items"])


def response(code, body):
    return {
        "statusCode": code,
        "headers": {
            "Content-Type": "application/json"
            },
        "body": json.dumps(body),
    }