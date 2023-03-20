import json
import cloudlog_commons


print(cloudlog_commons.__version__)

def handler(event, context):
    print("Hello Cloud World!")
    return {
        "statusCode": 200,
        "body": json.dumps("Hello Cloud World!")
    }