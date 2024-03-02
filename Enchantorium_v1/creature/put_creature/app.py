import boto3
from boto3.dynamodb.conditions import Key
from os import getenv
from uuid import uuid4
import json

#WORKING
region_name = getenv('APP_REGION')
enchantorium_creatures = boto3.resource('dynamodb', region_name=region_name ).Table('Enchantorium_Creatures')

def lambda_handler(event, context):
    if "body" in event and event["body"] is not None:
        event = json.loads(event["body"])

    id = event["ID"]
    name = event["name"]
    age = event["age"]
    weight = event["weight"]
    ship_from = event["ship_from"]
    description = event["description"]
    type = event["type"]
    price = event["price"]
    quantity = event["quantity"]

    if "ID" is not event or id is None:
        response(400, "ID is required")

    creature = enchantorium_creatures.get_item(Key= {"ID":id})["Item"]

    if creature is None:
        response(404, "No such creature found")
    if name is not None:
        creature["name"] = name
    if age is not None:
        creature["age"] = age
    if weight is not None:
        creature["weight"] = weight
    if ship_from is not None:
        creature["ship_from"] = ship_from
    if description is not None:
        creature["description"] = description
    if type is not None:
        creature["type"] = type
    if price is not None:
        creature["price"] = price
    if quantity is not None:
        creature["quantity"] = quantity
    
    enchantorium_creatures.put_item(Item=creature)
    return response(200, creature)

def response(code, body):
    return {
        "statusCode": code,
        "headers": {
            "Content-Type": "application/json"
            },
        "body": json.dumps(body)
    }