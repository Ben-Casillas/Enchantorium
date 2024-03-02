import boto3
from boto3.dynamodb.conditions import Key
from os import getenv
from uuid import uuid4
import json

#WORKING
region_name = getenv('APP_REGION')
enchantorium_users = boto3.resource('dynamodb', region_name=region_name ).Table('Enchantorium_Users')

def lambda_handler(event, context):
    if "body" in event and event["body"] is not None:
        event = json.loads(event["body"])

    user_id = str(uuid4())
    username = event["username"]
    password = event["password"]
    email = event["email"]
    addresses = event["addresses"]
    banking = event["banking"]
    title = event["title"]

    db_insert(user_id, username, password, email, addresses, banking, title)
    return response(200, {"ID": user_id, "Status": "User added, welcome in"})


def db_insert(user_id, username, password, email, addresses, banking, title):
    enchantorium_users.put_item(Item={
        "ID": user_id,
        "username": username,
        "password": password,
        "email": email,
        "addresses": addresses,
        "banking": banking,
        "title": title
    })


def response(code, body):
    return {
        "statusCode": code,
        "headers": {
            "Content-Type": "application/json"
            },
        "body": json.dumps(body),
        "isBase64Encoded": False
    }