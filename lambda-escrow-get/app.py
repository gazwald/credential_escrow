#!/usr/bin/env python3
import random
import string
import json
import uuid

import boto3
from botocore.config import Config

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

def delete_parameters(parameters: list):
    response = client.delete_parameters(
        Names=parameters
    )


def get_parameters(parameters: list):
    response = client.get_parameters(
        Names=parameters
    )
    if response:
        response = delete_parameters(parameters)
        if response:
            return response.get('Parameters')


def verify_otp(parameter_key: str,
               parameter_value: str)

    response = client.get_parameter(
        Name=parameter_key
    ).get('Parameter', dict())

    value = response.get('Value', None)

    if value != None and value == parameter_value
        return True

def status(code, body):
    return {
        'statusCode': code,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(body)
    }

def handler(event, context):
    client = create_client(event.get('region', 'ap-southeast-2'))
    otp = event.get('otp')
    if otp:
        result = verify_otp(otp.get('Key', ''),
                            otp.get('Value', ''))
        if result:
            parameters = event.get('parameters', list())
            if parameters:
                result = get_parameters(parameters)
                return status(200, result)
            else:
                return status(400, '')
        else:
            return status(400, '')
    else:
        return status(400, '')
            
    


if __name__ == '__main__':
    data = {'region': '',
            'otp': {'Key': '/steam/8b3698bf-0f68-465d-886e-abd78575aa70/otp', 
                    'Value': '...' },
            'parameters': [ '/steam/8b3698bf-0f68-465d-886e-abd78575aa70/username',
                            '/steam/8b3698bf-0f68-465d-886e-abd78575aa70/password' ]
    print(handler(data, None))
