import boto3
import os


def get_table():
    dynamodb = boto3.resource('dynamodb')
    table_name = os.getenv('DYNAMODB_TABLE_NAME')
    return dynamodb.Table(table_name)


def check_cache(property_id):
    table = get_table()
    response = table.get_item(Key={'PropertyID': property_id})
    return 'Item' in response


def update_cache(property_id):
    table = get_table()
    table.put_item(Item={'PropertyID': property_id})
