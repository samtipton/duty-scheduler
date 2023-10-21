import json
import os


def load_service_duties():
    service_duties = {}
    for filename in os.listdir("./duties"):
        if filename.endswith(".json"):
            with open(f'./duties/{filename}', "r") as f:
                data = json.load(f)
                service_duties[filename[:-5]] = data
    return service_duties


def load_men():
    men = {}
    for filename in os.listdir("./men"):
        if filename.endswith(".json"):
            with open(f'./men/{filename}', "r") as f:
                data = json.load(f)
                first_and_last_names = filename[:-5].split('-')
                formatted_name = f'{first_and_last_names[0].capitalize()}, {first_and_last_names[1].capitalize()}'
                data['formatted_name'] = formatted_name
                men[formatted_name] = data

    for man in men.values():
        man['duties'] = set(man['duties'])

    return men


"""
    index duties to men that can perform them
"""


def load_duty_index(men, service_duties):
    duty_index = {}

    sorted_men = [man for man in men.values()]
    sorted_men.sort(key=lambda man: man['last_name'])

    duties = [duty for service in service_duties.values()
              for duty in service['duties']]

    # print(men)
    for man in sorted_men:
        for duty in duties:
            if duty['key'] in men[man['formatted_name']]['duties']:
                if duty['key'] in duty_index:
                    duty_index[duty['key']].append(man['formatted_name'])
                else:
                    duty_index[duty['key']] = [man['formatted_name']]

    # print(duty_index)

    return duty_index
