import boto3
from boto3.dynamodb.conditions import Key
from os import getenv
from uuid import uuid4
import json
import jwt

SECRET_KEY = "Ravioli"

#working in test console
region_name = getenv('APP_REGION')
enchantorium_users = boto3.resource('dynamodb', region_name=region_name).Table('Enchantorium_Users')


def middleware_handler(event, context):
    # Check if the Authorization header is present
    if "headers" not in event or "Authorization" not in event["headers"]:
        return response(401, "Unauthorized")

    auth_header = event["headers"]["Authorization"]
    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        # Check if the user has the admin role
        if payload.get("role") == "ADMIN":
            return lambda_handler(event, context)
        else:
            return response(403, "Forbidden")
    except jwt.ExpiredSignatureError:
        return response(401, "Token has expired")
    except jwt.InvalidTokenError:
        return response(401, "Invalid token")


def lambda_handler(event, context):
    if "pathParameters" not in event:
        return response(400, {"error": "no path params"})
    path = event["pathParameters"]
    if path is None or "ID" not in path:
        return response(400, "No ID found")
    id = path["ID"]

    # Proceed with deletion
    output = enchantorium_users.delete_item(Key={"ID": id})
    return response(200, output)


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
