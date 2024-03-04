import boto3
from boto3.dynamodb.conditions import Key
from os import getenv
from uuid import uuid4
import json
import jwt

SECRET_KEY = "Ravioli"

#WORKING
region_name = getenv('APP_REGION')
enchantorium_users = boto3.resource('dynamodb', region_name=region_name ).Table('Enchantorium_Users')


def lambda_handler(event, context):
    if "pathParameters" not in event:    
        return response(400, {"error": "no path params"})
    path = event["pathParameters"]
    if path is None or "ID" not in path:
        return response(400, "No ID found")
    id = path["ID"]
    user_role = get_user_role(event)
    if user_role != "ADMIN":
        return response(418, "")
    
    output = enchantorium_users.delete_item(Key={"ID":id})
    return response(200, output)


def get_user_role(event):
    auth_header = event.get("headers",{}).get("Authorization")
    if not auth_header:
        return None
    
    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=["HS256"])
        return payload.get("role")
    except jwt.ExpieredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def response(code, body):
    return {
        "statusCode": code,
        "headers": {
            "Content-Type": "application/json"
            },
        "body": json.dumps(body),
    }