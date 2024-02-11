import boto3
from boto3.dynamodb.conditions import Key
from os import getenv
from uuid import uuid4
import json

region_name = getenv('APP_REGION')
enchantorium_creates = boto3.resource('dynamodb', region_name=region_name ).Table('Enchantorium_Creatures')


def lambda_handler(event, context):
    if( ("body" in event ) ):
        event = json.loads(event["body"])
    creature_id = str(uuid64())
    name = event["name"]
    age = event["age"]
    weight = event["weight"]
    loc_found = event["loc_found"]
    achievements = event["achievements"]
    price = event["price"]
    


def insert(creature_id, name, age, weight, loc_found, achievements, price):
    return "balls"

def response(code, body):
    return{
        "statusCode": code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
    }