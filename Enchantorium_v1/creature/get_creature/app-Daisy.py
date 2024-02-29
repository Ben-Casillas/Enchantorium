import boto3
from boto3.dynamodb.conditions import Key
from os import getenv
from uuid import uuid4
import json
from decimal import Decimal

#WORKING
region_name = getenv('APP_REGION')
enchantorium_creatures = boto3.resource('dynamodb', region_name=region_name).Table('Enchantorium_Creatures')

def lambda_handler(event, context):
    if "pathParameters" in event:
        path = event["pathParameters"]
        if path is None or "ID" not in path:
            items = enchantorium_creatures.scan()["Items"]
            serialized_items = serialize_decimals(items)
            return response(200, serialized_items)
        if path is not None and "ID" in path:
            id = path["ID"]
            output = enchantorium_creatures.get_item(Key={"ID": id})["Item"]
            serialized_output = serialize_decimals(output)
            return response(200, serialized_output)
    items = enchantorium_creatures.scan()["Items"]
    serialized_items = serialize_decimals(items)
    return response(200, serialized_items)

def serialize_decimals(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, list):
        return [serialize_decimals(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: serialize_decimals(value) for key, value in obj.items()}
    return obj

def response(code, body):
    return {
        "statusCode": code,
        "headers": {
            "Content-Type": "application/json"
            },
        "body": json.dumps(body),
    }