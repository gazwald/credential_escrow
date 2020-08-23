#!/usr/bin/env python3
import random
import string
import json
import uuid

import boto3
from botocore.config import Config

def generate_character_set():
    return string.ascii_lowercase + string.ascii_uppercase + string.digits


def generate_otp(length=32):
    characters = generate_character_set()
    return ''.join(random.choices(characters, k=length))


def generate_parameter_name(prefix: str,
                            group_name: str,
                            subgroup: str,
                            parameter_name: str):
    parameter_name_list = [prefix, group_name, subgroup, parameter_name]
    return '/'.join(parameter_name_list).replace('//', '/')
                            

def create_client(region: str = 'ap-southeast-2'):
    config = Config(
        region_name = region,
        signature_version = 'v4',
        retries = {
            'max_attempts': 10,
            'mode': 'standard'
        }
    )
    return boto3.client('ssm', config=config)


def create_parameter(client,
                     parameter_name: str,
                     parameter_value: str,
                     parameter_desc: str = '',
                     parameter_type: str = 'String',
                     parameter_tier: str = 'Standard',
                     parameter_tags: list = [],
                     parameter_overwrite: bool = True):

    response = client.put_parameter(
        Name=parameter_name,
        Description=parameter_desc,
        Value=parameter_value,
        Type=parameter_type,
        Overwrite=parameter_overwrite,
        Tags=parameter_tags,
        Tier=parameter_tier
    )
    return response

def create_otp_parameter(client, parameter_name: str):
    parameter_value = generate_otp()

    result = create_parameter(client,
                              parameter_name,
                              parameter_value,
                              'One time password')
    return parameter_value

def status(code, body):
    return {
        'statusCode': code,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(body)
    }

def handler(event, context):
    data = json.loads(event.get('body', None))
    client = create_client(data.get('region', 'ap-southeast-2'))
    prefix = data.get('prefix', '')
    group_name = data.get('group_name', None)
    if not group_name:
        return status(400, '')

    parameter_uuid = str(uuid.uuid4())
    
    otp_parameter_name = generate_parameter_name(prefix, group_name, parameter_uuid, 'otp')
    otp_parameter_value = create_otp_parameter(client, otp_parameter_name)

    parameters = []
    credentials = data.get('credentials', None)
    for parameter in credentials:
        parameter_name = generate_parameter_name(prefix, group_name, parameter_uuid, parameter.get('Key', None))
        parameter_value = parameter.get('Value')
        parameter_desc = ''
        result = create_parameter(client,
                                  parameter_name,
                                  parameter_value,
                                  parameter_desc)
        parameters.append(parameter_name)

    return status(200, {'uuid': parameter_uuid, 'otp': otp_parameter_value, 'parameters': parameters})



if __name__ == '__main__':
    data = {'group_name': 'steam',
            'region': 'us-west-2',
            'credentials': [
                {'Key': 'username', 'Value': 'my_username', 'Description': ''},
                {'Key': 'password', 'Value': 'my_password', 'Description': 'Password!'},
            ]
    }
    print(handler(data, None))
