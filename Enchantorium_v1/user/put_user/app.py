import boto3
from boto3.dynamodb.conditions import Key
from os import getenv
from uuid import uuid4
import json

#WORKING
region_name = getenv('APP_REGION')
enchantorium_users = boto3.resource('dynamodb', region_name=region_name ).Table('Enchantorium_Users')

def lambda_handler(event, context):
    if(("body" in event)):
        event = json.loads(event["body"])
    id = event["ID"]
    username = event["username"]
    password = event["password"]
    email = event["email"]
    addresses = event["addresses"] 
    banking = event["banking"]
    title = event["title"]

    if "ID" not in event or id is None:
        response(400, "ID is required")

    user = enchantorium_users.get_item(Key={"ID":id})["Item"]

    if user is None:
        response(404, "No such user found")
    if username is not None:
        user["username"] = username
    if password is not None:
        user["password"] = password
    if email is not None:
        user["email"] = email
    if addresses is not None:
        user["addresses"] = addresses
    if banking is not None:
        user["banking"] = banking
    if title is not None:
        user["title"] = title

    enchantorium_users.put_item(Item=user)
    return response(200, user)


def response(code, body):
    return {
        "statusCode": code,
        "headers": {
            "Content-Type": "application/json"
            },
        "body": json.dumps(body)
    }