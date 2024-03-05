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
    if( ("body" in event ) ):
        event = json.loads(event["body"])
        
    auth_header = event["headers"]["Authorization"]
    token = auth_header.split(" ")[1]
    trinket_id = str(uuid4())
    seller_ID = get_user_id(token)
    name = event["name"]
    trinket_type = event["trinket_type"] # so like knife, gun, "AOE" which is a friggin bomb, misc, so like ways to administer their secondary effect
    AOE_index = event["AOE_index"] #so like global, regional, local threat
    location = event ["location"]
    
    insert(trinket_id, name, trinket_type, AOE_index, seller_ID, location)
    return response(200, {"ID": trinket_id})


# make one to sort by index
def insert(trinket_id, name, trinket_type, AOE_index, seller_ID, location):
    enchantorium_weapons.put_item(Item={
        "ID": trinket_id,
        "name": name,
        "trinket_type": trinket_type,
        "AOE_index": AOE_index,
        "seller_ID":  seller_ID,
        "location": location
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

def get_user_id(token):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded_token["user_ID"]
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expiered")
    except (jwt.InvalidTokenError, KeyError):
        return "SOMETHING BAD HAPPENED"