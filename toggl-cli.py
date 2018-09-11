#!/usr/bin/env python3
import os
import configparser
import requests
import sys
import datetime
import urllib
import json

user_home_path = os.path.expanduser('~')
config_path = os.path.join(user_home_path, '.tcli/config')

config = configparser.ConfigParser()
config.read(config_path)

user = config['Account']['user']
password = config['Account']['password']
auth = requests.auth.HTTPBasicAuth(user, password)

command = sys.argv[1] if len(sys.argv) > 1 else 'start'

if command == 'start':
    entries = requests.get('https://www.toggl.com/api/v8/time_entries?{}'.format(
        urllib.parse.urlencode({
            'start_date': '{}+00:00'.format((datetime.datetime.now() - datetime.timedelta(days=365)).isoformat().split('.')[0]),
            'end_date': '{}+00:00'.format(datetime.datetime.now().isoformat().split('.')[0])
        })
    ), auth=auth).json()

    unique_tasks = []

    for entry in entries:
        unique_tasks.append((entry['pid'], entry['description']))

    unique_tasks = set(unique_tasks)
    unique_tasks = sorted(unique_tasks, key=lambda x: (x[0], x[1]))
    unique_projects = set([t[0] for t in unique_tasks])
    project_id_to_project_name = {}

    for project_id in unique_projects:
        project_id_to_project_name[project_id] = requests.get('https://www.toggl.com/api/v8/projects/{}'.format(project_id), auth=auth).json()['data']['name']

    for i, task in enumerate(unique_tasks):
        print('{} \033[1m{}\033[0m: {}'.format(i + 1, project_id_to_project_name[task[0]], task[1]))

    print('\nWhich task to start? ', end='')
    choice = unique_tasks[int(input()) -1]

    requests.post('https://www.toggl.com/api/v8/time_entries/start', data=json.dumps({
        'time_entry': {
            'description': choice[1],
            'pid': choice[0],
            'created_with': 'cli'
        }
    }), auth=auth)

    print('\n{}: {} \033[1mstarted\033[0m.'.format(project_id_to_project_name[choice[0]], choice[1]))
elif command == 'stop':
    running = requests.get('https://www.toggl.com/api/v8/time_entries/current', auth=auth).json()


    requests.put('https://www.toggl.com/api/v8/time_entries/{}/stop'.format(running['data']['id']), auth=auth)

    print('\033[1mStopped\033[0m.')

exit(0)
