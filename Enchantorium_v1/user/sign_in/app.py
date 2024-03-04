import datetime
import boto3
import jwt

# Secret key used to sign and verify JWT tokens
SECRET_KEY = "Ravioli"
dynamodb = boto3.client("dynamodb")

event = {
    "username": "LeBron",
    "password": "James"
}

def lambda_handler(event, context):
    # Define token payload containing user information
    username = event["username"]
    password = event["password"]
    if not username or not password:
        print("failed")
        return {"error": "Missing username or password"}
    user = verify_creds(username, password)
    
    if user:
        print("yea")
        payload = {
            "user_id": user_id,
            "role": user_role,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expiration time
        }
    
        # Generate JWT token
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return token
    else:
        return{"Error": "Invalid username or password"}

def verify_creds(username, password):
    response = dynamodb.query(
        TableName="Enchantorium_Users",
        KeyConditionExpression="username = :u",
        ExpressionAttributeValues={
            ":u": {"S": username}
        }
    )

    if "Items" in response and len(response["Items"]) > 0:
        for user in response["Items"]:
            if "password" in user and user["password"]["S"] == password:
                return {
                    "user_id": user["ID"]["S"],
                    "title": user["title"]["S"]  # Assuming user role is stored in an attribute named 'role'
                }

    return None

result = lambda_handler(event, None)
print(result)