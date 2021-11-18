import boto3
from time import sleep
from botocore.vendored import requests


def lambda_handler(event, context):
    client = boto3.client('cloudtrail')
    response = client.lookup_events(
        LookupAttributes=[
            {
                'AttributeKey': 'EventName',
                'AttributeValue': 'StartInstance'
            },
        ],
        MaxResults=1,
    )
    output = (response['Events'])
    userName = (output[0]['Username'])
    eventTime = (output[0]['EventTime'])
    EventName = (output[0]['EventName'])
    resources = (output[0]['Resources'])
    instanceId = (resources[0]['ResourceName'])

    def check(value):
        if(value == None):
            return ""
        else:
            return value

    my_file = open("ec2.txt","w+")
    my_file.write("Action done by" + ":" + check(userName) + "\n")
    my_file.write("eventTime" + ":" +  check(eventTime) +'\n')
    my_file.write("State" + ":" +  check(EventName) +'\n')
    my_file.write("instanceId" + ":" +  check(instanceId) +'\n') 

    s3 = boto3.resource('s3')
    object = s3.Object('specify_bucket_name', 'ec2.txt')
