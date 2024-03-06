import boto3
from boto3.dynamodb.conditions import Key
from os import getenv
import json

#working in test console
region_name = getenv('APP_REGION')
enchantorium_creatures = boto3.resource('dynamodb', region_name=region_name).Table('Enchantorium_Creatures')
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    if "body" in event and event["body"] is not None:
        event = json.loads(event["body"])

    id = event.get("ID")
    if not id:
        return response(400, "ID is required")

    creature = enchantorium_creatures.get_item(Key={"ID": id}).get("Item")
    if not creature:
        return response(404, "No such creature found")

    # Update creature attributes if provided
    creature.update({
        "name": event.get("name", creature.get("name")),
        "age": event.get("age", creature.get("age")),
        "weight": event.get("weight", creature.get("weight")),
        "ship_from": event.get("ship_from", creature.get("ship_from")),
        "description": event.get("description", creature.get("description")),
        "type": event.get("type", creature.get("type")),
        "price": event.get("price", creature.get("price")),
        "quantity": event.get("quantity", creature.get("quantity"))
    })

    # Update image if provided
    if "image" in event:
        image = event["image"]
        image_key = upload_image_to_s3(id, image)
        creature["image_key"] = image_key

    enchantorium_creatures.put_item(Item=creature)
    return response(200, creature)

def upload_image_to_s3(creature_id, image):
    bucket_name = 'your-s3-bucket-name'
    image_key = f'images/{creature_id}.jpg'  # Assuming JPEG format, adjust if needed
    s3_client.put_object(Bucket=bucket_name, Key=image_key, Body=image)
    return image_key

def response(code, body):
    return {
        "statusCode": code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
    }
