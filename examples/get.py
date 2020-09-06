#!/usr/bin/env python3
import requests


def main():
    otp = 'NpwynLtGGjzsQCDtxVRESMWJmcyKdhNp'
    uuid = 'd490d32a-6af6-44f8-af14-e91846850dc4'

    base_url = 'https://f3qo7g8tf8.execute-api.ap-southeast-2.amazonaws.com/prod/'
    url = '/'.join([base_url, 'escrow', 'get'])

    values = {
        'region': 'ap-southeast-2',
        'otp': {'Key': f'/steam/{uuid}/otp',
                'Value': otp,
        },
        'parameters': [
            f'/steam/{uuid}/username',
            f'/steam/{uuid}/password'
        ]
    }

    r = requests.post(
        url,
        json=values
    )

    print(r.status_code)
    print(r.json())

if __name__ == '__main__':
    main()
