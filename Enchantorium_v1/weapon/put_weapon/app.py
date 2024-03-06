import boto3
from boto3.dynamodb.conditions import Key
from os import getenv
from uuid import uuid4
import json

#WORKING
region_name = getenv('APP_REGION')
enchantorium_weapons = boto3.resource('dynamodb', region_name=region_name ).Table('Enchantorium_Weapons')


def lambda_handler(event, context):
    if(("body" in event)):
        event = json.loads(event["body"])
    id = event["ID"]
    name = event["name"]
    price = event["price"]
    trinket_type = event["trinket_type"] 
    AOE_index = event["AOE_index"]
    seller_ID = event["seller_ID"]
    location = event ["location"]

    if "ID" is not event or id is None:
        response(400, "ID is required")

    weapon = enchantorium_weapons.get_item(Key= {"ID":id})["Item"]

    if weapon is None:
        response(404, "No such trinket found")
    if name is not None:
        weapon["name"] = name
    if price is not None:
        weapon["price"] = price
    if trinket_type is not None:
        weapon["trinket_type"] = trinket_type
    if AOE_index is not None:
        weapon["AOE_index"] = AOE_index
    if seller_ID is not None:
        weapon["seller_ID"] = seller_ID
    if location is not None:
        weapon["location"] = location

    enchantorium_weapons.put_item(Item=weapon)
    return response(200, weapon)

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