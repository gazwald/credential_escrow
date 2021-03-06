#!/usr/bin/env python3
import requests


def main():
    base_url = 'https://f3qo7g8tf8.execute-api.ap-southeast-2.amazonaws.com/prod/'
    url = '/'.join([base_url, 'escrow', 'set'])
    values = {
        'group_name': 'steam',
        'region': 'ap-southeast-2',
        'credentials': [
            {'Key': 'username', 'Value': 'my_username', 'Description': ''},
            {'Key': 'password', 'Value': 'my_password', 'Description': 'Password!'},
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
