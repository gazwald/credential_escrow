#!/usr/bin/env python3
import requests


def main():
    url = 'https://mr3gvzju4l.execute-api.ap-southeast-2.amazonaws.com/prod/escrow'
    values = {
        'group_name': 'steam',
        'region': 'ap-southeast-2',
        'credentials': [
            {'Key': 'username', 'Value': 'my_username', 'Description': ''},
            {'Key': 'password', 'Value': 'my_password', 'Description': 'Password!'},
        ]
    }

    r = requests.put(
        url,
        json=values
    )

    print(r.status_code)
    print(r.json())

if __name__ == '__main__':
    main()
