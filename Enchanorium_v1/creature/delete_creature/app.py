import boto3
from boto3.dynamodb.conditions import Key
from os import getenv
from uuid import uuid4
import json

region_name = getenv('APP_REGION')
enchantorium_creatures = boto3.resource('dynamodb', region_name=region_name ).Table('Enchantorium_Creatures')

def lambda_handler(event, context):
    if "pathParameters" not in event:
        return response(400, {"Error": "no creature specified"})
    path = event["pathParameters"]
    if path is None or "ID" not in path:
        return response(400, "no such creature found")
    id = path["ID"]
    output = enchantorium_creatures.delete_item(Key={"Id":id})
    return response(200, output)



def response(code, body):
    return {
        "statusCode": code,
        "headers": {
            "Content-Type": "application/json"
            },
        "body": json.dumps(body),
    }