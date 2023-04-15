import pytest
import os
from moto import mock_dynamodb
import boto3

OS_DICT = {
    'DYNAMO_TABLE_NAME': "test_table"
}


@pytest.fixture(autouse=True, scope='package')
def mock_env():
    os.environ.update(OS_DICT)
    
    with mock_dynamodb():
        dynamo = boto3.resource('dynamodb')
        dynamo.create_table(
            TableName=os.environ['DYNAMO_TABLE_NAME'],
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'timestamp',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'timestamp',
                    'AttributeType': 'N'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )
        yield
    
    for key in OS_DICT.keys():
        del os.environ[key]