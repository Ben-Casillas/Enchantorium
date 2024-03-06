import boto3
import json
from decimal import Decimal

# working in test console
dynamodb = boto3.resource('dynamodb')
enchantorium_weapons = dynamodb.Table('Enchantorium_Creatures')

def lambda_handler(event, context):
    query_params = event.get("queryStringParameters", {})
    name = query_params.get("name")
    type = query_params.get("type")


    price_param = query_params.get("price")
    max_price = Decimal(price_param) if price_param is not None else None

    filtered_items = [
        item for item in enchantorium_weapons.scan()["Items"]
        if (not name or name.lower() in item.get("name", "").lower()) and 
        (type is None or type.lower() == item.get("type", "").lower()) and 
        (max_price is None or Decimal(item.get("price", 0)) <= max_price)
    ]
    return response(200, filtered_items, serialize_decimals)

def response(code, body, serialize_func=None):
    if serialize_func:
        body = serialize_func(body)
    return {
        "statusCode": code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
    }

def serialize_decimals(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, list):
        return [serialize_decimals(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: serialize_decimals(value) for key, value in obj.items()}
    return obj
