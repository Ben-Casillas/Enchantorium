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
        weapon_id = str(uuid64())

        name = event["name"]
        type = event["type"] #so like explosive, gun, melee
        threat_level = event["threat"] #so like scope (national, global, local threat ???)
        



def response(code, body):
    return {
        "statusCode": code,
        "headers": {
            "Content-Type": "application/json"
            },
        "body": json.dumps(body),
        "isBase64Encoded": False
    }