import boto3
import jwt
import json
from datetime import datetime, timedelta

#working in test console
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Enchantorium_Users')
SECRET_KEY = "Ravioli"
TOKEN_EXPIRE_TIME = 3600  # Token expiration time in seconds (1 hour)

def lambda_handler(event, context):
    username = event["username"]
    password = event["password"]
    response = table.scan(
        FilterExpression=boto3.dynamodb.conditions.Attr('username').eq(username)
    )
    items = response['Items']
    user = items[0]

    if user["password"] == password:
        expire_time = datetime.utcnow() + timedelta(seconds=TOKEN_EXPIRE_TIME)
        payload = {
            "user_ID": user["ID"],
            "username": username,
            "password": user["password"],
            "title": user["title"],
            "exp": expire_time
        }
        token = jwt.encode(
            payload, SECRET_KEY, algorithm="HS256",
        )
        return httpResponse(200, token)

    return httpResponse(404, "Invalid Username or Password")


def httpResponse(code, body):
    response_data = {
        "statusCode": code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
    }
    return response_data