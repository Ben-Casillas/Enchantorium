import boto3
from boto3.dynamodb.conditions import Key
from os import getenv
from uuid import uuid4
import json
import jwt

#working in test console
region_name = getenv('APP_REGION')
enchantorium_weapons = boto3.resource('dynamodb', region_name=region_name ).Table('Enchantorium_Weapons')
SECRET_KEY = "Ravioli"

def lambda_handler(event, context):
    if "pathParameters" not in event:    
        return response(400, {"error": "no path params"})
    path = event["pathParameters"]
    if path is None or "ID" not in path:
        return response(400, "no ID found")
    id = path["ID"]
    auth_header = event["headers"]["Authorization"]
    token = auth_header.split(" ")[1]
    payload_seller = get_user_id(token)
    weapon_item = enchantorium_weapons.get_item(Key={"ID": id}).get("Item")
    if payload_seller == weapon_item["seller_ID"]:
        output = enchantorium_weapons.delete_item(Key={"ID":id})
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
        "body": json.dumps(body),
        "isBase64Encoded": False
    }

def get_user_id(token):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded_token["user_ID"]
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expiered")
    except (jwt.InvalidTokenError, KeyError):
        return "Thats not yours to delete"