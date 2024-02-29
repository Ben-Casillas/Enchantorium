import boto3
from boto3.dynamodb.conditions import Key
from os import getenv
from uuid import uuid4
import json

#DONE
region_name = getenv('APP_REGION')
enchantorium_weapons = boto3.resource('dynamodb', region_name=region_name ).Table('Enchantorium_Weapons')

def lambda_handler(event, context):
    if("parhParameters" in event):
        path = event["pathParameters"]
        trinket_id = str(uuid4())
        name = event["name"]
        trinket_type = event["type"] # so like knife, gun, "AOE" which is a friggin bomb, misc, so like ways to administer their secondary effect
        secondary_effect = event["secondary_effect"] # the "ebola" part to the "ebola knife"
        regional_area = event["regional"] #so like global, regional, local threat
        
        insert(trinket_id, name, trinket_type, secondary_effect, regional_area)
        return response(200, {"ID": trinket_id})


def insert(trinket_id, name, trinket_type, secondary_effect, regional_area):
    enchantorium_weapons.put_item(Item={
        "ID": trinket_id,
        "name": name,
        "trinkey_type": trinket_type,
        "secondary_effect": secondary_effect,
        "regional_area": regional_area
    })

def response(code, body):
    return {
        "statusCode": code,
        "headers": {
            "Content-Type": "application/json"
            },
        "body": json.dumps(body),
        "isBase64Encoded": False
    }