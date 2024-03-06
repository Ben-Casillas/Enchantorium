import boto3
import json

# working in test console
dynamodb = boto3.resource('dynamodb')
enchantorium_weapons = dynamodb.Table('Enchantorium_Weapons')

def lambda_handler(event, context):
    query_params = event.get("queryStringParameters", {})
    name = query_params.get("name")
    max_price = query_params.get("price")

    filter_expression = None
    expression_att_values = {}

    if name:
        filter_expression = 'contains(#name, :name)'
        expression_att_values[':name'] = name
    if max_price:
        if filter_expression:
            filter_expression += ' AND '
        else:
            filter_expression = ''
        filter_expression += '#price < :max_price'  # Change from '=' to '<'
        expression_att_values[':max_price'] = int(max_price)  # Convert max_price to int

    if filter_expression:
        response = enchantorium_weapons.scan(
            FilterExpression=filter_expression,
            ExpressionAttributeNames={'#name': 'name', '#price': 'price'},
            ExpressionAttributeValues=expression_att_values
        )
    else:
        response = enchantorium_weapons.scan()

    return {
        'statusCode': 200,
        'body': json.dumps(response['Items'])
    }
