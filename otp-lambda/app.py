#!/usr/bin/env python3
import random
import string
import json

def generate_character_set():
    return string.ascii_lowercase + string.ascii_uppercase + string.digits

def generate_otp(length=32):
    characters = generate_character_set()

    otp = ''.join(random.choices(characters, k=length))

    return otp

def handler(event, context):
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({'otp': generate_otp()})
    }

if __name__ == '__main__':
    print(handler(None, None))
