import json


def handler(event, context):
    print("Hello Cloud World!")
    
    return {
        "statusCode": 200,
        "body": json.dumps("Hello Cloud World!")
    }