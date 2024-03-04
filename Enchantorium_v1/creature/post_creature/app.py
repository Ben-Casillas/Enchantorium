import boto3
from boto3.dynamodb.conditions import Key
from os import getenv
from uuid import uuid4
import json

#WORKING
region_name = getenv('APP_REGION')
enchantorium_creatures = boto3.resource('dynamodb', region_name=region_name ).Table('Enchantorium_Creatures')
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    if "body" in event and event["body"] is not None:
        event = json.loads(event["body"])

    creature_id = str(uuid4())
    #seller id potentially not sure how to handle that just yet
    name = event["name"]
    age = event["age"]
    weight = event["weight"]
    ship_from = event["ship_from"]
    description = event["description"]
    type = event["type"] #mounts, "slaves"(helpers), guards (SS), livestock, #mounts, "slaves"(helpers), guards (SS), livestock
    price = event["price"]
    quantity = event["quantity"]
    image = event["image"]

    image_key = upload_image_to_s3(creature_id, image)

    insert(creature_id, name, age, weight, ship_from, description, type, price, quantity, image_key)
    return response(200, {"ID": creature_id})


def insert(creature_id, name, age, weight, ship_from, description, type, price, quantity, image_key):
    formatted_price = '{:.2f}'.format(float(price))
    enchantorium_creatures.put_item(Item ={
        "ID": creature_id,
        "name": name,
        "age": age,
        "weight": weight,
        "ship_from": ship_from,
        "description": description,
        "type": type,
        "price": formatted_price,
        "quantity": quantity,
        "image_key": image_key
    })

def upload_image_to_s3(creature_id, image):
    bucket_name = "creature-bucket"
    image_key = f'images/{creature_id}.jpg'
    s3.client.put_object(Bucket=bucket_name, Key=image_key, Body=image)
    return image_key

def response(code, body):
    return{
        "statusCode": code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
    }