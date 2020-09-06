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

def delete_parameter(client,
                      parameter: str):
    try:
        response = client.delete_parameter(
            Name=parameter
        )
    except:
        return False
    else:
        return True

def delete_parameters(client,
                      parameters: list):
    try:
        response = client.delete_parameters(
            Names=parameters
        )
    except:
        return False
    else:
        return True


def filter_parameters(parameters: dict):
    keys = ['Name', 'Value']
    result = list()
    for parameter in parameters:
        result.append({k: v for k, v in parameter.items() if k in keys})
    return result


def get_parameters(client,
                   parameters: list):
    response = client.get_parameters(
        Names=parameters
    )
    if response and delete_parameters(client, parameters):
        return filter_parameters(response.get('Parameters', dict()))


def verify_otp(client,
               parameter_key: str,
               parameter_value: str):

    if parameter_key and parameter_value:
        try:
            response = client.get_parameter(
                Name=parameter_key
            ).get('Parameter', dict())
        except client.exceptions.ParameterNotFound as e:
            return False
        except client.exceptions.ParameterVersionNotFound as e:
            return False
        except client.exceptions.InvalidKeyId as e:
            return False
        else:
            value = response.get('Value', None)
            if value != None and value == parameter_value:
                return delete_parameter(client, parameter_key)


def status(code, body):
    return {
        'statusCode': code,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(body)
    }

def handler(event, context):
    data = json.loads(event.get('body'))
    client = create_client(data.get('region', 'ap-southeast-2'))
    otp = data.get('otp')
    if otp:
        result = verify_otp(client,
                            otp.get('Key', None),
                            otp.get('Value', None))
        if result:
            parameters = data.get('parameters', None)
            if parameters:
                result = get_parameters(client, parameters)
                if result:
                    return status(200, result)
                else:
                    return status(200, 'Successfully did nothing; No parameters provided or none found')
            else:
                return status(400, 'No parameters provided or none found')
        else:
            return status(400, 'Unable to verify OTP')
    else:
        return status(400, 'No OTP provided')
            
    


if __name__ == '__main__':
    data = {'region': 'us-west-2',
            'otp': {'Key': '/steam/fa7b38a9-fbb8-4f07-afc9-5e8527974695/otp', 
                    'Value': 'hEVzvasSixBAcjfG34jiLPE5HvkbdcbK'},
            'parameters': [ '/steam/fa7b38a9-fbb8-4f07-afc9-5e8527974695/username',
                            '/steam/fa7b38a9-fbb8-4f07-afc9-5e8527974695/password' ]
    }
    print(handler(data, None))
