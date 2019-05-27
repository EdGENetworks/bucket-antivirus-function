import boto3
from uuid import uuid4
dynamodb = boto3.resource('dynamodb')
import os
TABLE_NAME = os.getenv("AV_DEFINITION_DYNAMO_TABLE")
table = dynamodb.Table(TABLE_NAME)



def insert_data(data):
    """
    this method is used to insert new data in to DynamoDb
    """
    doc_id = str(uuid4())
    data["id"] = doc_id
    table.put_item(Item=data)
    return doc_id

def get_data(query):
    """
    the method is used to search data 
    """
    response = table.get_item(Key=query)
    item = response['Item']
    print(item)
    return item

def update_data(query, data):
    """
    this method is used to update the exiting table data 
    """
    update_expression = 'SET'
    expression_att = {}
    value_key = ":val"
    counter = 0
    for key,value in data.iteritems():
        counter += 1
        val_key = value_key + str(counter)
        expression_att[val_key] = value
        if "=" in update_expression:
            update_expression += ", " + key + " = " + val_key
        else:
            update_expression += " " + key + " = " + val_key
    table.update_item(
    Key=query,
    UpdateExpression=update_expression,
    ExpressionAttributeValues=expression_att
)