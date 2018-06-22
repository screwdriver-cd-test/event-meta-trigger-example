import os
import sys
import requests

api_url = 'https://api.screwdriver.cd/v4/';

def get_JWT():
    url = api_url + 'auth/token?api_token=' + os.environ['API_TOKEN']

    response = requests.get(url)
    if response.status_code != 200:
        print('[ERROR] Error accessing Screwdriver API, got status code {0}'.format(response.status_code))
        sys.exit(1)

    return response.json()['token'];

def post_event(jwt):
    url = api_url + 'events';
    header = {'Authorization': jwt};
    payload = {
        'pipelineId': 1131,
        'startFrom': '~commit',
        'meta': {
            'foo': 'bar',
            'one': 1
        }
    };

    response = requests.post(url, headers=header, json=payload);

    if response.status_code != 201:
        print('[ERROR] Failed to create event, got status code {0}'.format(response.status_code))
        sys.exit(1)

    return response.status_code

if __name__ == '__main__':
    jwt = get_JWT();
    status_code = post_event(jwt);

    print ('OK', status_code);
