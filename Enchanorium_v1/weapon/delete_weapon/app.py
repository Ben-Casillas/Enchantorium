import boto3
from boto3.dynamodb.conditions import Key
from os import getenv
from uuid import uuid4
import json

#DONE
region_name = getenv('APP_REGION')
enchantorium_weapons = boto3.resource('dynamodb', region_name=region_name ).Table('Enchantorium_Weapons')


def lambda_handler(event, context):
    if "pathParameters" not in event:    
        return response(400, {"error": "no path params"})
    path = event["pathParameters"]
    if path is None or "ID" not in path:
        return response(400, "no id found")
    id = path["ID"]
    output = enchantorium_weapons.delete_item(Key={"ID":id})
    return response(200, output)
    

def response(code, body):
    return {
        "statusCode": code,
        "headers": {
            "Content-Type": "application/json"
            },
        "body": json.dumps(body),
        "isBase64Encoded": False
    }