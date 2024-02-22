import boto3
from boto3.dynamodb.conditions import Key
from os import getenv
from uuid import uuid4
import json

#DONE
region_name = getenv('APP_REGION')
enchantorium_weapons = boto3.resource('dynamodb', region_name=region_name ).Table('Enchantorium_Weapons')


def lambda_handler(event, context):
    if(("body" in event)):
        event = json.loads(event["body"])
    id = event["ID"]
    name = event["name"]
    trinket_type = event["type"]
    secondary_effect = event["secondary_effect"]
    regional_area = event["regional"]

    if "ID" is not event or id is None:
        response(400, "ID is required")

    weapon = enchantorium_weapons.get_item(Key= {"ID":id})["Item"]

    if weapon is None:
        response(404, "No such trinket found")
    if name is not None:
        weapon["name"] = name
    if trinket_type is not None:
        weapon["trinket_type"] = trinket_type
    if secondary_effect is not None:
        weapon["secondary_effect"] = secondary_effect
    if regional_area is not None:
        weapon["regional_area"] = regional_area

    enchantorium_weapons.put_item(Item=weapon)
    return response(200, weapon)

def response(code, body):
    return {
        "statusCode": code,
        "headers": {
            "Content-Type": "application/json"
            },
        "body": json.dumps(body)
    }