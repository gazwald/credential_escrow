#!/usr/bin/env python3
import requests


def main():
    url = 'https://mr3gvzju4l.execute-api.ap-southeast-2.amazonaws.com/prod/escrow'
    values = {
        'region': 'ap-southeast-2',
        'otp': {'Key': 'm8P2geCCb3leq5essg6PCUp3Z7etovsN',
                'Value': '/steam/ed496ac3-974d-4de3-b43a-6d0b7d2838f0/otp',
        },
        'parameters': [
            '/steam/ed496ac3-974d-4de3-b43a-6d0b7d2838f0/username',
            '/steam/ed496ac3-974d-4de3-b43a-6d0b7d2838f0/password'
        ]
    }

    r = requests.post(
        url,
        params=values
    )

    print(r.status_code)
    print(r.json())

if __name__ == '__main__':
    main()
